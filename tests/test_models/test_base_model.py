#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModel_init
    TestBaseModel_str
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
from models import storage


class TestBaseModel_init(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_init(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_obj(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_a_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_diff_ids(self):
        bm_1 = BaseModel()
        bm_2 = BaseModel()
        self.assertNotEqual(bm_1.id, bm_2.id)

    def test_two_models_diff_created_at(self):
        bm_1 = BaseModel()
        sleep(0.03)
        bm_2 = BaseModel()
        self.assertLess(bm_1.created_at, bm_2.created_at)

    def test_two_models_diff_updated_at(self):
        bm_1 = BaseModel()
        sleep(0.03)
        bm_2 = BaseModel()
        self.assertLess(bm_1.updated_at, bm_2.updated_at)

    def test_str_repr(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "12345"
        bm.created_at = bm.updated_at = dt
        bm_str = bm.__str__()
        self.assertIn("[BaseModel] (12345)", bm_str)
        self.assertIn("'id': '12345'", bm_str)
        self.assertIn("'created_at': " + dt_repr, bm_str)
        self.assertIn("'updated_at': " + dt_repr, bm_str)

    def test_args_not_used(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_init_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="8633", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "8633")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_init_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_init_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("67", id="8633", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "8633")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    # Testing new attributes creation
    def test_new_attr(self):
        bm = BaseModel()
        bm.name = "Alx"
        bm.my_number = 6
        self.assertTrue(hasattr(bm, "name") and hasattr(bm, "my_number"))

    # Test update storage variable
    def test_bm_updated_storage(self):
        bm = BaseModel()
        bm_key = "BaseModel." + bm.id
        keys = storage.all().keys()
        self.assertTrue(bm_key in keys)


class TestBaseModel_str(unittest.TestCase):
    """Test __str__ method of BaseModel class"""

    """
    def test_empty_input_str(self):
        bm = BaseModel()
        bm_str = str(bm)

        a = "[BaseModel] ("
        len_a = len(a) + len(bm.id) + 2
        val1 = bm_str[: len_a]
        con1 = a + bm.id + ") "
        self.assertEqual(con1, val1)

        val2 = eval(bm_str[len_a:])
        con2 = bm.__dict__
        self.assertEqual(con2, val2)

    def test_new_attr_str(self):
        bm = BaseModel()
        bm.name = "Alx"
        bm.my_number = 6
        bm_str = str(bm)

        a = "[BaseModel] ("
        len_a = len(a) + len(bm.id) + 2
        val1 = bm_str[: len_a]
        con1 = a + bm.id + ") "
        self.assertEqual(con1, val1)

        val2 = eval(bm_str[len_a:])
        con2 = bm.__dict__
        self.assertEqual(con2, val2)
        """

    def test_string_return(self):
        """tests the string method to make sure it returns
            the proper string
        """
        bm = BaseModel()
        bm_str = str(bm)
        id_test = "[BaseModel] ({})".format(bm.id)
        boln = id_test in bm_str
        self.assertEqual(True, boln)
        boln = "updated_at" in bm_str
        self.assertEqual(True, boln)
        boln = "created_at" in bm_str
        self.assertEqual(True, boln)
        boln = "datetime.datetime" in bm_str
        self.assertEqual(True, boln)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

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

    def test_save_once(self):
        bm = BaseModel()
        sleep(0.03)
        updated_at1 = bm.updated_at
        bm.save()
        self.assertLess(updated_at1, bm.updated_at)

    def test_save_twice(self):
        bm = BaseModel()
        sleep(0.03)
        updated_at1 = bm.updated_at
        bm.save()
        updated_at2 = bm.updated_at
        self.assertLess(updated_at1, updated_at2)
        sleep(0.03)
        bm.save()
        self.assertLess(updated_at2, bm.updated_at)

    def test_save_with_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_update_file(self):
        bm = BaseModel()
        bm.save()
        bm_id = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bm_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_type_to_dict(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_right_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attr(self):
        bm = BaseModel()
        bm.name = "ALX"
        bm.my_number = 6
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dic = bm.to_dict()
        self.assertEqual(str, type(bm_dic["created_at"]))
        self.assertEqual(str, type(bm_dic["updated_at"]))

    def test_output_to_dict(self):
        dt = datetime.today()
        bm = BaseModel()
        bm.id = "16482"
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '16482',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
