#!/usr/bin/python3

"""
    Defines a class User.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """Represent a User
    Public Attributes:
    -----------------
    - email
    - password
    - first_name
    - last_name."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new User"""

        super().__init__(*args, **kwargs)
