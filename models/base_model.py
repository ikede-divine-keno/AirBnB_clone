#!/usr/bin/python3

"""
    Defines a class BaseModel.
"""

from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """Represent a BaseModel."""
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for key, values in kwargs.items():
                if key != '__class__':
                    if key == "created_at" or key == "updated_at":
                        formt = "%Y-%m-%dT%H:%M:%S.%f"
                        setattr(self, key, datetime.strptime(values, formt))
                    else:
                        setattr(self, key, values)
