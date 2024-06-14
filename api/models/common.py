"""
Model module defining models related to images
"""

from typing import Optional
from fastapi import Query
from pydantic import BaseModel


class ImageGenerationInput(BaseModel):
    """
    The input format for image generation
    """

    content_url: str
    dpi: Optional[int] = Query(None, ge=10, le=600)
