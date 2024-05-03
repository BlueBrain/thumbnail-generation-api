"""Models for the soma API."""

from pydantic import BaseModel


class ProcessSomaRequest(BaseModel):
    """Request model for processing SWC from a content URL."""

    content_url: str
