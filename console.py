#!/usr/bin/python3
"""Define the HBNBCommand class."""
import cmd
import json
import re
from models.base_model import BaseModel
from models import storage
from shlex import split
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


def tokenize(args):
    token = re.search(r"\{(.*?)\}", args)
    key = re.search(r"\[(.*?)\]", args)
    if token is None:
        if key is None:
            return [a.strip(",") for a in split(args)]
        else:
            tok = split(args[:key.span()[0]])
            retl = [a.strip(",") for a in tok]
            retl.append(key.group())
            return retl
    else:
        tok = split(args[:token.span()[0]])
        ken = [a.strip(",") for a in tok]
        ken.append(token.group())
        return ken


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    __commands = {
        "show",
        "count",
        "all",
        "destroy",
        "update"
    }

    """
    def arg_finder(argt):
        #Get argument inside of ' ( arg) '

        p = argt.find('(')
        return argt[p + 1: -1]

    def typeCast(val_txt):
        #Cast in int or float a value
        if val_txt.isnumeric():
            return int(val_txt)
        else:
            try:
                return float(val_txt)
            except Exception as e:
                return val_txt
    """

    def for_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def help_quit(self):
        """Help command for quit"""
        print("Quit command to exit the program\n")

    def if_EOF(self, arg):
        """Exit with 'EOF' signal.
        """
        print("")
        return True

    def help_EOF(self):
        """Help command for EOF"""
        print("EOF command to exit the program\n")

    def if_emptyline(self):
        """Ignore an empty line.
        """
        pass

    def base(self, args):
        """Default behavior for cmd module when input is invalid or incompatible"""
        arg_dic = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        sm = re.search(r"\.", args)
        if sm is not None:
            arg_sm = [args[:sm.span()[0]], args[sm.span()[1]:]]
            sm = re.search(r"\((.*?)\)", arg_sm[1])
            if sm is not None:
                cmnd = [arg_sm[1][:sm.span()[0]], sm.group()[1:-1]]
                if cmnd[0] in arg_dic.keys():
                    fnt = "{} {}".format(arg_sm[0], cmnd[1])
                    return arg_dic[cmnd[0]](fnt)
        print("*** Unknown syntax: {}".format(args))
        return False

    def do_create(self, args):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        arg_t = tokenize(args)
        if len(arg_t) == 0:
            print("** class name missing **")
        elif arg_t[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_t[0])().id)
            storage.save()

    def help_create(self):
        """Help command for create"""
        print("Create a BaseModel and save the json in a file\n")

    def do_show(self, args):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_t = tokenize(args)
        ob_dic = storage.all()
        if len(arg_t) == 0:
            print("** class name missing **")
        elif arg_t[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_t) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_t[0], arg_t[1]) not in ob_dic:
            print("** no instance found **")
        else:
            print(ob_dic["{}.{}".format(arg_t[0], arg_t[1])])

    def help_show(self):
        """Help command for show"""

        mesge = "Prints the string representation of an instance "
        mesge += "based on the class name and id\n"
        print(mesge)

    def do_destroy(self, args):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_t = tokenize(args)
        ob_dic = storage.all()
        if len(arg_t) == 0:
            print("** class name missing **")
        elif arg_t[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_t) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_t[0], arg_t[1]) not in ob_dic.keys():
            print("** no instance found **")
        else:
            del ob_dic["{}.{}".format(arg_t[0], arg_t[1])]
            storage.save()

    def help_destroy(self):
        """Help command for destroy"""
        print("Deletes an instance based on the class name and id\n")

    def do_all(self, args):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argt = tokenize(args)
        if len(argt) > 0 and argt[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obt = []
            for ob in storage.all().values():
                if len(argt) > 0 and argt[0] == ob.__class__.__name__:
                    obt.append(ob.__str__())
                elif len(argt) == 0:
                    obt.append(ob.__str__())
            print(obt)

    def help_all(self):
        """Help command for all"""

        msg = "Prints all string representation of all instances "
        msg += "based or not on the class name\n"
        print(msg)

    def do_count(self, args):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argt = tokenize(args)
        cnt = 0
        for ob in storage.all().values():
            if argt[0] == ob.__class__.__name__:
                cnt += 1
        print(cnt)

    def help_count(self):
        """Help command for count"""

        msg = "Count how much instances have a given class\n"
        print(msg)

    def do_update(self, args):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argt = tokenize(args)
        ob_dic = storage.all()

        if len(argt) == 0:
            print("** class name missing **")
            return False
        if argt[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argt) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argt[0], argt[1]) not in ob_dic.keys():
            print("** no instance found **")
            return False
        if len(argt) == 2:
            print("** attribute name missing **")
            return False
        if len(argt) == 3:
            try:
                type(eval(argt[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argt) == 4:
            ob = ob_dic["{}.{}".format(argt[0], argt[1])]
            if argt[2] in ob.__class__.__dict__.keys():
                val_typ = type(ob.__class__.__dict__[argt[2]])
                ob.__dict__[argt[2]] = val_typ(argt[3])
            else:
                ob.__dict__[argt[2]] = argt[3]
        elif type(eval(argt[2])) == dict:
            ob = ob_dic["{}.{}".format(argt[0], argt[1])]
            for k, v in eval(argt[2]).items():
                if (k in ob.__class__.__dict__.keys() and
                        type(ob.__class__.__dict__[k]) in {str, int, float}):
                    val_typ = type(ob.__class__.__dict__[k])
                    ob.__dict__[k] = val_typ(v)
                else:
                    ob.__dict__[k] = v
        storage.save()

    def help_update(self):
        """Help command for update"""

        msg = "Updates an instance based on the class "
        msg += "name and id by adding or updating attribute\n"
        msg += "Usage: update <class name> <id> <attribute name>  "
        msg += "\"<attribute value>\"\n"
        print(msg)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
