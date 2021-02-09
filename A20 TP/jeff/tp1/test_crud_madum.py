from crud import CRUD
import unittest


class TestCRUDMadum(unittest.TestCase):
    maxDiff = None

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
            "Date_of_first_seen_message": 1605135873,
            "Date_of_last_seen_message": 1605135873,
            "Groups": ["default", "colleagues"],
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

    # Tests rapporteurs
    def test_get_users_data(self):
        crud = CRUD(False)
        crud.modify_users_file(self.users_data)
        self.assertEqual(crud.read_users_file(), self.users_data)

    # Tests constructeurs
    def test_crud_constructor(self):
        crud = CRUD(False)
        self.assertEqual(crud.read_users_file(), {"1": self.user})
        self.assertEqual(crud.read_groups_file(), {})

    # Tests transformateurs
    def test_crud_add_new_user_1(self):
        crud = CRUD(False)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.update_users('2', "Trust", 60)
        crud.remove_user_group('2', 'default')
        crud.remove_user(1)

        modified_user = self.user_2
        modified_user["Groups"].remove('default')
        modified_user["Trust"] = 60
        self.assertEqual(crud.read_users_file(), {'2': modified_user})

    def test_crud_add_new_user_2(self):
        crud = CRUD(False)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.update_users('2', 'Groups', 'friends')
        crud.remove_user(1)
        crud.remove_user_group('2', 'default')

        expected_user = self.user_2
        expected_user["Groups"].append('friends')
        expected_user["Groups"].remove('default')
        print(crud.read_users_file())
        self.assertEqual(crud.read_users_file(), {'2': expected_user})

    def test_crud_add_new_user_3(self):
        crud = CRUD(False)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user(2)
        crud.update_users('1', 'Trust', 75)
        crud.remove_user_group('1', 'default')

        expected_user = self.user
        expected_user["Groups"].remove('default')
        expected_user["Trust"] = 75
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_add_new_user_4(self):
        crud = CRUD(False)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user(2)
        crud.remove_user_group('1', 'default')
        crud.update_users('1', 'Trust', 80)

        expected_user = self.user
        expected_user["Groups"].remove('default')
        expected_user["Trust"] = 80
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_add_new_user_5(self):
        crud = CRUD(False)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user_group('1', 'default')
        crud.update_users('2', 'SpamN', 1)
        crud.remove_user(1)

        expected_user = self.user_2
        expected_user["SpamN"] = 1
        self.assertEqual(crud.read_users_file(), {'2': expected_user})

    def test_crud_add_new_user_6(self):
        crud = CRUD(False)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user_group('1', 'colleagues')
        crud.remove_user(2)
        crud.update_users('1', 'Trust', 40)

        expected_user = self.user
        expected_user["Trust"] = 40
        expected_user["Groups"].remove('colleagues')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_group_1(self):
        crud = CRUD(False)
        crud.remove_user_group('1', 'colleagues')
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.update_users('2', 'Trust', 60)
        crud.remove_user(1)

        expected_user = self.user_2
        expected_user["Trust"] = 60
        self.assertEqual(crud.read_users_file(), {'2': expected_user})

    def test_crud_remove_user_group_2(self):
        crud = CRUD(False)
        crud.remove_user_group('1', 'colleagues')
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user(2)
        crud.update_users('1', 'Trust', 10)

        expected_user = self.user
        expected_user['Trust'] = 10
        expected_user['Groups'].remove('colleagues')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_group_3(self):
        crud = CRUD(False)
        crud.remove_user_group('1', 'colleagues')
        crud.remove_user(1)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.update_users('1', 'Trust', 90)

        expected_user = self.user_2
        expected_user['Trust'] = 90
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_group_4(self):
        crud = CRUD(False)
        crud.remove_user_group('1', 'colleagues')
        crud.remove_user(1)
        crud.update_users('1', 'Trust', 10)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")

        expected_user = self.user_2
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_group_5(self):
        crud = CRUD(False)
        crud.remove_user_group('1', 'default')
        crud.update_users('1', 'HamN', 5)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user(2)

        expected_user = self.user
        expected_user['HamN'] = 5
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_group_6(self):
        crud = CRUD(False)
        crud.remove_user_group('1', 'colleague')
        crud.update_users('1', 'HamN', 5)
        crud.remove_user(1)
        crud.add_new_user('leffersonjam@gmail.com', "2020-11-16")

        self.assertEqual(crud.read_users_file(), {'1': self.user_2})

    def test_crud_remove_user_1(self):
        crud = CRUD(False)
        crud.remove_user(1)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.update_users('1', 'SpamN', 25)
        crud.remove_user_group('1', 'default')

        expected_user = self.user_2
        expected_user['SpamN'] = 25
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_2(self):
        crud = CRUD(False)
        crud.remove_user(1)
        crud.add_new_user("leffersonjam@gmail.com", "2020-11-16")
        crud.remove_user_group('1', 'default')
        crud.update_users('1', 'Trust', 95)

        expected_user = self.user_2
        expected_user['Trust'] = 95
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_3(self):
        crud = CRUD(False)
        crud.remove_user(1)
        crud.remove_user_group('1', 'default')
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')
        crud.update_users('1', 'Trust', 15)

        expected_user = self.user_2
        expected_user['Trust'] = 15
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_4(self):
        crud = CRUD(False)
        crud.remove_user(1)
        crud.remove_user_group('1', 'default')
        crud.update_users('1', 'Trust', 20)
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')

        self.assertEqual(crud.read_users_file(), {'1': self.user_2})

    def test_crud_remove_user_5(self):
        crud = CRUD(False)
        crud.remove_user(1)
        crud.update_users('1', 'Trust', 15)
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')
        crud.remove_user_group('1', 'default')

        expected_user = self.user_2
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_remove_user_6(self):
        crud = CRUD(False)
        crud.remove_user(1)
        crud.update_users('1', 'Trust', 30)
        crud.remove_user_group('1', 'default')
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')

        self.assertEqual(crud.read_users_file(), {'1': self.user_2})

    def test_crud_update_users_1(self):
        crud = CRUD(False)
        crud.update_users('1', 'Date_of_first_seen_message', 123123123)
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')
        crud.remove_user(2)
        crud.remove_user_group('1', 'default')

        expected_user = self.user
        expected_user['Date_of_first_seen_message'] = 123123123
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_update_users_2(self):
        crud = CRUD(False)
        crud.update_users('1', 'Date_of_last_seen_message', 1605762353)
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')
        crud.remove_user_group('1', 'default')
        crud.remove_user(2)

        expected_user = self.user
        expected_user['Date_of_last_seen_message'] = 1605762353
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_update_users_3(self):
        crud = CRUD(False)
        crud.update_users('1', 'Trust', 15)
        crud.remove_user_group('1', 'colleague')
        crud.remove_user(1)
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')

        self.assertEqual(crud.read_users_file(), {'1': self.user_2})

    def test_crud_update_users_4(self):
        crud = CRUD(False)
        crud.update_users('1', 'Trust', 20)
        crud.remove_user_group('1', 'colleagues')
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')
        crud.remove_user(2)

        expected_user = self.user
        expected_user['Trust'] = 20
        expected_user['Groups'].remove('colleagues')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_update_users_5(self):
        crud = CRUD(False)
        crud.update_users('1', 'HamN', 2)
        crud.remove_user(1)
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')
        crud.remove_user_group('1', 'default')

        expected_user = self.user_2
        expected_user['Groups'].remove('default')
        self.assertEqual(crud.read_users_file(), {'1': expected_user})

    def test_crud_update_users_6(self):
        crud = CRUD(False)
        crud.update_users('1', 'SpamN', 5)
        crud.remove_user(1)
        crud.remove_user_group('1', 'default')
        crud.add_new_user('leffersonjam@gmail.com', '2020-11-16')

        self.assertEqual(crud.read_users_file(), {'1': self.user_2})
