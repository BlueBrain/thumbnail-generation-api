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

import requests
from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()


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

        blender_executable_path = current_directory.parent.parent / "blender/bbp-blender-3.5/blender-bbp/blender"

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
            raise HTTPException(status_code=404, detail="OBJ file not found after processing.")

        print("generated_obj_path: ", mesh.as_posix())

        return FileResponse(
            path=mesh,
            media_type="model/gltf+json",
            filename=mesh.name,
        )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


class ProcessSomaRequest(BaseModel):
    """Request model for processing SWC from a content URL."""

    content_url: str


def get_file_content(authorization: str, content_url: str) -> bytes:
    """Fetch the file content from the provided content URL."""
    headers = {"Authorization": authorization}
    timeout = 10  # Timeout in seconds
    try:
        response = requests.get(content_url, headers=headers, timeout=timeout)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        # Re-raising the exception with 'raise from' to maintain traceback
        raise HTTPException(status_code=500, detail="An error occurred while fetching file: " + str(e)) from e

    return response.content


@router.post("/process-nexus-swc")
async def process_soma(request: ProcessSomaRequest, authorization: str = Header(None)) -> FileResponse:
    """Process a SWC file from a content URL and return the processed soma mesh."""
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")

    file_content = get_file_content(authorization, request.content_url)

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
        blender_executable_path = current_directory.parent.parent / "blender/bbp-blender-3.5/blender-bbp/blender"

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

        raise HTTPException(status_code=404, detail="OBJ file not found after processing.")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
