from crud import CRUD
import unittest

class TestCRUDMadum(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["default", "friends"],
            },
        }
        self.test_user= {
            "1": {
                "name": "wow@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["default"],
            },
        }

        self.test_user_2= {
            "1": {
                "name": "wow@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["default", "friends"],
            },
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass

    def test_add_new_user_1(self):
        crud=CRUD()
        crud.add_new_user("bob@gmail.com", "2021-02-09")
        #crud.update_users(1,"name","wow@gmail.com")
        #crud.remove_user(2)
        #crud.remove_user_group('1',"friends")
        print(self.users_data)
        test_user=self.test_user
        self.assertEqual(self.users_data,test_user)
        

    # def test_remove_user_group_1(self):
    #     crud = CRUD()
    #     crud.remove_user_group("1", )
        
        



    