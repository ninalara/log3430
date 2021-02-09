from crud import CRUD
import unittest
from unittest.mock import patch


class TestCRUDConditionsF(unittest.TestCase):
    def setUp(self):
        self.users_data = {
            "1": {
                "name": "heebangsyang@outlook.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605135873,
                "Date_of_last_seen_message": 1605135873,
                "Groups": ["default", "colleagues"]
            },
        }

    def tearDown(self):
        pass

    # (#, update_users, F)
    def test_crud_constructor_update_users(self):
        crud = CRUD(True)
        self.assertEqual(crud.update_users(1, 'Trust', 100), False)
        self.assertRaises(Exception, crud.update_users, [1, 'Trust'])

    # (#, get_user_data, F)
    def test_crud_constructor_get_user_data(self):
        crud = CRUD(True)
        self.assertRaises(Exception, crud.get_user_data, [1, 'Trust'])

    # (#, remove_user, F)
    def test_crud_constructor_remove_user(self):
        crud = CRUD(True)
        self.assertEqual(crud.remove_user(1), False)
        self.assertRaises(Exception, crud.remove_user(1))

    # (#, remove_user_group, F)
    def test_crud_constructor_remove_user_group(self):
        crud = CRUD(True)
        self.assertEqual(crud.remove_user_group(1, 'default'), False)
        self.assertRaises(Exception, crud.remove_user_group(1, 'default'))

    # (remove_user, remove_user, F)
    def test_cred_remove_user_remove_user(self):
        crud = CRUD(False)
        crud.remove_user(1)
        self.assertEqual(crud.remove_user_group(1, 'default'), False)

    # (remove_user, update_users, F)
    def test_crud_remove_user_update_users(self):
        crud = CRUD(False)
        crud.remove_user(1)
        self.assertEqual(crud.update_users(1, 'Trust', 100), False)

    # (remove_user, get_user_data, F)
    def test_crud_remove_user_get_user_data(self):
        crud = CRUD(False)
        crud.remove_user(1)
        self.assertRaises(Exception, crud.get_user_data, [1, 'Trust'])

    # (remove_user, remove_user_group, F)
    def test_crud_remove_user_remove_user_group(self):
        crud = CRUD(False)
        crud.remove_user(1)
        self.assertEqual(crud.remove_user_group(1, 'default'), False)

    # (remove_user_group, remove_user_group, F)
    def test_crud_remove_user_group_remove_user_group(self):
        crud = CRUD(False)
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.remove_user_group(1, 'default'), False)



