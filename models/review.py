#!/usr/bin/python3

"""
    Defines a class Review.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a Review class."""
    place_id = ""
    user_id = ""
    text = ""
