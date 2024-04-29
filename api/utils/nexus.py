"""
Module: nexus.py

This module wraps functionality for the Nexus Delta API.
"""

import os
import httpx
from fastapi import HTTPException
import dotenv

dotenv.load_dotenv()


API_ENDPOINT = os.getenv("NEXUS_DELTA_API", "http://localhost:8080")


# Nexus Delta API client setup
class NexusClient:
    def __init__(self):
        self.client = httpx.Client()

    async def fetch_file(self, org_label, project_label, file_id, rev=None, token=None):
        url = f"{API_ENDPOINT}/{org_label}/{project_label}/{file_id}"

        if rev:
            url += f"?rev={rev}"
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = self.client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch file from Nexus Delta.",
            )
        return response.content, response.headers.get("content-type")
