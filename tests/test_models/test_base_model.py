#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


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
        dt = datetime.now()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "174289"
        bm.created_at = bm.updated_at = dt
        bm_str = bm.__str__()
        self.assertIn("[BaseModel] (174289)", bm_str)
        self.assertIn("'id': '174289'", bm_str)
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
