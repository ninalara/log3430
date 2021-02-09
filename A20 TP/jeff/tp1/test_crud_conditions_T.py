from crud import CRUD
import unittest
from unittest.mock import patch


class TestCRUDConditionsT(unittest.TestCase):
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

        self.user = {
            "name": "heebangsyang@outlook.com",
            "Trust": 50,
            "SpamN": 0,
            "HamN": 0,
            "Date_of_first_seen_message": 1605502800,
            "Date_of_last_seen_message": 1605502800,
            "Groups": ["default"],
        }

        self.user_2 = {
            "name": "leffersonjam@gmail.com",
            "Trust": 50,
            "SpamN": 0,
            "HamN": 0,
            "Date_of_first_seen_message": 1605502800,
            "Date_of_last_seen_message": 1605502800,
            "Groups": ["default"]
        }

    def tearDown(self):
        pass

    # (#, add_new_user, T)
    def test_crud_init_add_new_user(self):
        # _INIT_
        crud = CRUD(True)
        self.assertEqual(crud.read_users_file(), {})

        # add_new_user
        self.assertEqual(crud.add_new_user("leffersonjam@gmail.com", "2020-11-16"), True)
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

    # (add_new_user, add_new_user, T)
    def test_crud_add_new_user_add_new_user(self):

        crud = CRUD(True)

        # add_new_user
        self.assertEqual(crud.add_new_user("leffersonjam@gmail.com", "2020-11-16"), True)
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

        # add_new_user
        self.assertEqual(crud.add_new_user("heebangsyang@outlook.com", "2020-11-16"), True)
        self.assertEqual(crud.read_users_file().get('2'), self.user)

    # (add_new_user, update_users, C1)
    def test_crud_add_new_user_update_users(self):

        crud = CRUD(True)

        # add_new_user
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

        # update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

    # (update_users, update_users, C1)
    def test_crud_update_users_update_users(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

        # update_users
        crud.update_users(1, 'Trust', 100)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 100)

    # (update_users, add_new_user, T)
    def test_crud_update_users_add_new_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

        # add_new_user
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        self.assertEqual(crud.read_users_file().get('3'), None)

    # (add_new_user, get_user_data, C1)
    def test_crud_add_new_user_get_user_data(self):

        crud = CRUD(True)

        # add_new_user
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

    # (get_user_data, get_user_data, C1)
    def test_crud_get_user_data_get_user_data(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

    # (get_user_data, add_new_user, T)
    def test_crud_get_user_data_add_new_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

        # add_new_user
        self.assertEqual(crud.add_new_user("heebangsyang@outlook.com", "2020-11-16"), True)
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

    # (add_new_user, remove_user, C2)
    def test_crud_add_new_user_remove_user(self):

        crud = CRUD(True)

        # add_new_user
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

        # remove_user
        self.assertEqual(crud.remove_user(1), True)
        self.assertEqual(crud.read_users_file(), {})

    # (remove_user, add_new_user, T)
    def test_crud_remove_user_add_new_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # remove_user
        crud.remove_user(1)
        self.assertEqual(crud.read_users_file(), {})

        # add_new_user
        self.assertEqual(crud.add_new_user("leffersonjam@gmail.com", "2020-11-16"), True)
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

    # (add_new_user, remove_user_group, C3)
    def test_crud_add_new_user_remove_user_group(self):

        crud = CRUD(True)

        # add_new_user
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        self.assertEqual(crud.read_users_file().get('1'), self.user_2)

        # remove_user_group
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

    # (remove_user_group, add_new_user, T)
    def test_crud_remove_user_group_add_new_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # remove_user_group
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

        # add_new_user
        self.assertEqual(crud.add_new_user("heebangsyang@outlook.com", "2020-11-16"), True)
        self.assertEqual(crud.read_users_file().get('2'), self.user)

    # (update_users, get_user_data, C1)
    def test_crud_update_users_get_user_data(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 0)

    # (get_user_data, update_users, C1)
    def test_crud_get_user_data_update_users(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

        #update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

    # (update_users, remove_user, C2)
    def test_crud_update_users_remove_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

        # remove_user
        self.assertEqual(crud.remove_user(1), True)
        self.assertEqual(crud.read_users_file(), {})

    # (update_users, remove_user_group, C3)
    def test_crud_update_users_remove_user_group(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

        # remove_user_group
        self.assertEqual(crud.remove_user_group(1, 'default'), True)
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

    # (remove_user_group, update_users, C1)
    def test_crud_remove_user_group_update_users(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # remove_user_group
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

        # update_users
        crud.update_users(1, "Trust", 0)
        self.assertEqual(crud.get_user_data(1, 'Trust'), 0)

    # (get_user_data, remove_user, C2)
    def test_crud_get_user_data_remove_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

        # remove_user
        self.assertEqual(crud.remove_user(1), True)
        self.assertEqual(crud.read_users_file(), {})

    # (get_user_data, remove_user_group, C3)
    def test_crud_get_user_data_remove_user_group(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

        # remove_user_group
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

    # (remove_user_group, get_user_data, C1)
    def test_crud_remove_user_group_get_user_data(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # remove_user_group
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

        # get_user_data
        trust1 = crud.get_user_data(1, 'Trust')
        self.assertEqual(trust1, 50)

    def test_crud_remove_user_group_remove_user(self):

        crud = CRUD(True)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        # remove_user_group
        crud.remove_user_group(1, 'default')
        self.assertEqual(crud.get_user_data(1, 'Groups'), [])

        # remove_user
        self.assertEqual(crud.remove_user(1), True)
        self.assertEqual(crud.read_users_file(), {})

