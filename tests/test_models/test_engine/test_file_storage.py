#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_init(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_init_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_init_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_priv_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_priv_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_init(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_meth(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def testall_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bm = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(bm)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + u.id, models.storage.all().keys())
        self.assertIn(u, models.storage.all().values())
        self.assertIn("State." + s.id, models.storage.all().keys())
        self.assertIn(s, models.storage.all().values())
        self.assertIn("Place." + p.id, models.storage.all().keys())
        self.assertIn(p, models.storage.all().values())
        self.assertIn("City." + c.id, models.storage.all().keys())
        self.assertIn(c, models.storage.all().values())
        self.assertIn("Amenity." + a.id, models.storage.all().keys())
        self.assertIn(a, models.storage.all().values())
        self.assertIn("Review." + r.id, models.storage.all().keys())
        self.assertIn(r, models.storage.all().values())

    def testnew_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def testsave(self):
        bm = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(bm)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + u.id, save_text)
            self.assertIn("State." + s.id, save_text)
            self.assertIn("Place." + p.id, save_text)
            self.assertIn("City." + c.id, save_text)
            self.assertIn("Amenity." + a.id, save_text)
            self.assertIn("Review." + r.id, save_text)

    def test_save_witharg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def testreload(self):
        bm = BaseModel()
        u = User()
        s = State()
        p = Place()
        c = City()
        a = Amenity()
        r = Review()
        models.storage.new(bm)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(p)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(r)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + u.id, objs)
        self.assertIn("State." + s.id, objs)
        self.assertIn("Place." + p.id, objs)
        self.assertIn("City." + c.id, objs)
        self.assertIn("Amenity." + a.id, objs)
        self.assertIn("Review." + r.id, objs)

    def test_reload_witharg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
