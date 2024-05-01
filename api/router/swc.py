"""
Module: swc.py

This module takes a SWC file of a neuron morphology and processes its
soma using NeuroMorphoVis simulations. It has two endpoints, one for
processing a SWC file uploaded by the user and another for fetching a
SWC file from Nexus Delta and processing it.
"""

import os
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, HTTPException, UploadFile, File, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel

from api.utils.nexus import NexusClient

router = APIRouter()
nexus_client = NexusClient()


class ProcessSomaRequest(BaseModel):
    """Class for the request body of the process-soma endpoint."""

    org_label: str
    project_label: str
    file_id: str
    rev: str = None  # Making revision optional


@router.post("/process-swc")
async def process_swc(file: UploadFile = File(...)) -> FileResponse:
    """Process a SWC file uploaded by the user and return the processed soma mesh."""
    # Prepare the temporary file
    temp_file_path = ""

    try:
        with NamedTemporaryFile(delete=False, suffix=".swc") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        current_directory = Path(__file__).parent

        print(current_directory)

        output_directory = current_directory.parent.parent / "output"

        # Ensure the meshes subdirectory exists
        meshes_directory = output_directory / "meshes"

        meshes_directory.mkdir(exist_ok=True, parents=True)

        script_path = current_directory.parent.parent / "neuromorphovis.py"

        blender_executable_path = (
            current_directory.parent.parent
            / "blender/bbp-blender-3.5/blender-bbp/blender"
        )

        print("Running NMV script...")

        command = [
            "python",
            script_path.as_posix(),
            f"--blender={blender_executable_path.as_posix()}",
            "--input=file",
            f"--morphology-file={temp_file_path}",
            "--export-soma-mesh-blend",
            "--export-soma-mesh-obj",
            f"--output-directory={output_directory.as_posix()}",
        ]

        subprocess.run(command, check=True)
        print("Done with NMV script.")

        # Example output name: `SOMA_MESH_tmpe3e6xavl.glb`
        # unique identifier for now is the tempfile name which becomes the target
        target_name = Path(temp_file_path).stem

        for mesh in meshes_directory.iterdir():
            print(mesh.as_posix())
            if mesh.suffix == ".glb":
                name = mesh.stem.split("_")[-1]
                if name == target_name:
                    break
        else:
            raise HTTPException(
                status_code=404, detail="OBJ file not found after processing."
            )

        print("generated_obj_path: ", mesh.as_posix())

        return FileResponse(
            path=mesh,
            media_type="model/gltf+json",
            filename=mesh.name,
        )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@router.post("/process-soma")
async def process_soma(request: ProcessSomaRequest, authorization: str = Header(None)):
    """Process a SWC file from Nexus Delta and return the processed soma mesh."""
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Authorization token is missing or invalid"
        )

    token = authorization.split(" ")[1]
    file_content, content_type = await nexus_client.fetch_file(
        request.org_label, request.project_label, request.file_id, request.rev, token
    )

    if not content_type or "application/octet-stream" not in content_type:
        raise HTTPException(
            status_code=400, detail="The fetched file is not in a valid SWC format."
        )

    temp_file_path = ""
    try:
        with NamedTemporaryFile(delete=False, suffix=".swc") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        current_directory = Path(__file__).parent
        output_directory = current_directory.parent.parent / "output"
        meshes_directory = output_directory / "meshes"
        meshes_directory.mkdir(exist_ok=True, parents=True)
        script_path = current_directory.parent.parent / "neuromorphovis.py"
        blender_executable_path = (
            current_directory.parent.parent
            / "blender/bbp-blender-3.5/blender-bbp/blender"
        )

        command = [
            "python",
            script_path.as_posix(),
            f"--blender={blender_executable_path.as_posix()}",
            "--input=file",
            f"--morphology-file={temp_file_path}",
            "--export-soma-mesh-blend",
            "--export-soma-mesh-obj",
            f"--output-directory={output_directory.as_posix()}",
        ]

        subprocess.run(command, check=True)

        target_name = Path(temp_file_path).stem
        for mesh in meshes_directory.iterdir():
            if mesh.suffix == ".glb" and mesh.stem.split("_")[-1] == target_name:
                return FileResponse(
                    path=mesh,
                    media_type="model/gltf+json",
                    filename=mesh.name,
                )

        raise HTTPException(
            status_code=404, detail="OBJ file not found after processing."
        )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
