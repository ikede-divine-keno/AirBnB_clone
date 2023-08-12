#!/usr/bin/python3

"""
    Defines a class FileStorage.
"""

import json
import models
from models.base_model import BaseModel


class FileStorage:
    """Represent a FileStorage"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all the objects saved in the file"""
        """self.objects is same as FileStorage.objects"""
        return self.__objects

    def new(self, obj):
        """ Update (add new objects) dictionary """
        new_obj = obj.__class__.__name__ + "." + obj.id
        self.__objects.update({new_obj: obj})

    def save(self):
        """Save object representation of JSON to a file"""

        with open(self.__file_path, mode='w', encoding='UTF-8') as f:
            json_obj = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(json_obj, f)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        try:
            with open(self.__file_path) as f:
                dictn = json.load(f)
                key = {k: eval(v["__class__"])(**v) for k, v in dic.items()}
                FileStorage.__objects = key
        except:
            pass
