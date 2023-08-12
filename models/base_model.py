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
            #models.storage.new(self)
        else:
            for key, values in kwargs.items():
                if key != '__class__':
                    if key == "created_at" or key == "updated_at":
                        formt = "%Y-%m-%dT%H:%M:%S.%f"
                        setattr(self, key, datetime.strptime(values, formt))
                    else:
                        setattr(self, key, values)

    def __str__(self):
        """ String method"""
        return ("[{:s}] ({:s}) {:s}"
                .format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        """ Save Method """
        self.updated_at = datetime.now()
        #models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        reprt = {
            "__class__": self.__class__.__name__,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

        dic_cpy = self.__dict__.copy()
        dic_cpy.update(reprt)
        return dic_cpy    
