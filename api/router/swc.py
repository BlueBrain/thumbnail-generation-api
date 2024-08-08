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

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer
from starlette.requests import Request

from api.dependencies import retrieve_user
from api.utils.logger import logger
from api.services.nexus import fetch_file_content

router = APIRouter()
require_bearer = HTTPBearer()


# MARK: Endpoints
@router.post(
    "/process-swc",
    dependencies=[Depends(require_bearer)],
)
async def process_swc(file: UploadFile = File(...)) -> FileResponse:
    """Process the uploaded SWC file and return the generated mesh file."""
    temp_file_path = ""
    try:
        with NamedTemporaryFile(delete=False, suffix=".swc") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        logger.info("Temporary SWC file created at: %s", temp_file_path)

        current_directory = Path(__file__).parent
        output_directory = current_directory.parent.parent / "output"
        meshes_directory = output_directory / "meshes"
        meshes_directory.mkdir(exist_ok=True, parents=True)

        script_path = current_directory.parent.parent / "neuromorphovis.py"
        blender_executable_path = current_directory.parent.parent / "blender/bbp-blender-3.5/blender-bbp/blender"

        logger.info("Running NMV script...")
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
        logger.info("Completed NMV script execution.")

        target_name = Path(temp_file_path).stem

        for mesh in meshes_directory.iterdir():
            logger.debug("Checking mesh file: %s", mesh.name)
            if mesh.suffix == ".glb":
                name = mesh.stem.split("_")[-1]
                if name == target_name:
                    logger.info("Generated mesh file found: %s", mesh.as_posix())
                    break
        else:
            logger.error("OBJ file not found after processing.")
            raise HTTPException(status_code=404, detail="OBJ file not found after processing.")

        return FileResponse(
            path=mesh,
            media_type="model/gltf+json",
            filename=mesh.name,
        )
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info("Temporary file deleted: %s", temp_file_path)


@router.get(
    "/process-nexus-swc",
    dependencies=[Depends(require_bearer)],
)
async def process_soma(
    request: Request,
    content_url: str = Query(..., description="URL of the SWC file to process"),
) -> FileResponse:
    """Process the SWC file fetched from the given URL and return the generated mesh file."""

    logger.info("Fetching SWC file from URL: %s", content_url)
    user = retrieve_user(request)
    file_content = fetch_file_content(user.access_token, content_url)

    temp_file_path = ""
    try:
        with NamedTemporaryFile(delete=False, suffix=".swc") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        logger.info("Temporary SWC file created at: %s", temp_file_path)

        current_directory = Path(__file__).parent
        output_directory = current_directory.parent.parent / "output"
        meshes_directory = output_directory / "meshes"
        meshes_directory.mkdir(exist_ok=True, parents=True)

        script_path = current_directory.parent.parent / "neuromorphovis.py"
        blender_executable_path = current_directory.parent.parent / "blender/bbp-blender-3.5/blender-bbp/blender"

        logger.info("Running NMV script...")
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
        logger.info("Completed NMV script execution.")

        target_name = Path(temp_file_path).stem
        for mesh in meshes_directory.iterdir():
            logger.debug("Checking mesh file: %s", mesh.name)
            if mesh.suffix == ".glb" and mesh.stem.split("_")[-1] == target_name:
                logger.info("Generated mesh file found: %s", mesh.as_posix())
                return FileResponse(
                    path=mesh,
                    media_type="model/gltf+json",
                    filename=mesh.name,
                )

        logger.error("OBJ file not found after processing.")
        raise HTTPException(status_code=404, detail="OBJ file not found after processing.")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info("Temporary file deleted: %s", temp_file_path)
