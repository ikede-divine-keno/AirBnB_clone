#!/usr/bin/python3
"""Define the HBNBCommand class."""
import cmd
from models.base_model import BaseModel
from models import storage
from shlex import split
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
    ===========
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def tokenize(args_txt):
    """Parse all argurments for the console"""
    return split(args_txt)

    def arg_finder(argt):
    """ Get argument inside of ' ( arg) ' """
    p = argt.find('(')
    return argt[p + 1: -1]

    def typeCast(val_txt):
    """Cast in int or float a value"""
    if val_txt.isnumeric():
        return int(val_txt)
    else:
        try:
            return float(val_txt)
        except Exception as e:
            return val_txt

    def for_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def if_EOF(self, arg):
        """Exit with 'EOF' signal.
        """
        print("")
        return True

    def if_emptyline(self):
        """Ignore an empty line.
        """
        pass

if __name__ == "__main__":
    HBNBCommand().cmdloop()
