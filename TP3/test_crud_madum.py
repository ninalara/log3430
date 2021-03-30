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
            "0": {
                "name": "wow@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1612828800.0,
                "Date_of_last_seen_message": 1612828800.0,
                "Groups": ["default"],
            },
        }

        self.test_user_2= {
            "0": {
                "name": "wow@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1612828800.0,
                "Date_of_last_seen_message": 1612828800.0,
                "Groups": ["friends"],
                
            },
            "1" : {
                "name": "mark@mail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1612828800.0,
                "Date_of_last_seen_message": 1612828800.0,
                "Groups": ["default"],
            }
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
        crud.add_new_user("alex@gmail.com", "2021-02-10")
        crud.update_users(0,"name","wow@gmail.com")
        user_data = crud.remove_user(1)
        self.assertEqual(user_data,self.test_user)
        

    def test_remove_user_group_1(self):
        crud = CRUD()        
        crud.add_new_user("alex@gmail.com", "2021-02-09")
        crud.add_new_user("mark@mail.com", "2021-02-09")
        crud.add_new_group("default", 50, ["alex@gmail.com", "mark@mail.com"],)
        crud.add_new_group("friends",90, ["alex@gmail.com"],)        
        crud.update_users(0,"name","wow@gmail.com")
        user_data = crud.remove_user_group("0", "default")
        self.assertEqual(user_data,self.test_user_2)

        
        



    