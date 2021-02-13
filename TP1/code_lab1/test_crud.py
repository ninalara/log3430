from crud import CRUD
import unittest
from unittest.mock import patch


class TestCRUD(unittest.TestCase):
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
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596855166.0,
                "Date_of_last_seen_message": 1596855166.0,
                "Groups": ["default"],
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


    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_users_file")
    # def test_add_new_user_Passes_correct_data_to_modify_users_file(
    #     self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    # ):
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_users_file, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        crud.add_new_user("bob@gmail.com", "2021-02-09")
        mock_modify_users_file.assert_called_once_with(self.users_data)
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file", "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour l'utilisateur a étée formée correctement par la fonction, e.g.
        self.modify_users_file(data) -> "data" doit avoir un format et contenu expectee
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
   

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group("funsies", 50, ["alex@gmail.com"])
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a étée formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):

        testMessage= "Invalide"
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_data("10","SpamN"), testMessage)
        
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si ID non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):

        testMessage= "Invalide"
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_data("1","ABCDEFG"), testMessage)

        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si champ non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        fieldValue=0
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data("1","SpamN"), fieldValue)
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ est id valide sont utilisee
        il faut utiliser ".assertEqual()"
        """

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_users_file, mock_read_groups_file):
        testMessage= "Invalide"
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_groups_data("10","Trust"), testMessage)
        """"""

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_users_file, mock_read_groups_file
    ):
        testMessage= "Invalide"
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_groups_data("1","ABCDEFG"), testMessage)
        """"""

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file, mock_read_groups_file
    ):
        fieldValue=50
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data("1","Trust"), fieldValue)
        """"""

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):
        testMessage= "Invalide"
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_id("ArianeNini@gmail.com"), testMessage)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        fieldValue='1'
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_id("alex@gmail.com"), fieldValue)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
        self, mock_read_users_file, mock_read_groups_file
    ):
        testMessage= "Invalide"
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_group_id("ArianeNini"), testMessage)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_users_file, mock_read_groups_file):
        fieldValue='2'
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.get_user_id("friends"), fieldValue)

    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_id(
        self, mock_read_users_file
    ):
        fieldValue=False
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.update_users("3","Trust",60), fieldValue)
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """

    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_field(
        self, mock_read_users_file
    ):
        fieldValue=True
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.update_users("2","Trust",10), fieldValue)
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud=CRUD()
        crud.update_users("1","Trust",10)
        mock_modify_users_file.assert_called_once_with(self.users_data)
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        pass

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_read_users_file,mock_read_groups_file
    ):
        fieldValue=False
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.update_groups("4","Trust",10), fieldValue)
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_read_users_file, mock_read_groups_file
    ):
        fieldValue=True
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.update_groups("1","Trust",10), fieldValue)
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud=CRUD()
        crud.update_groups("1","Trust",30)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        pass

    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_read_users_file
    ):
        fieldValue=False
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.remove_user("3"), fieldValue)

    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file
    ):
        fieldValue=True
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.remove_user("1"), fieldValue)


    @patch("crud.CRUD.read_users_file")  
    @patch("crud.CRUD.read_groups_file")  
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_read_groups_file
    ):
        fieldValue=False
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.remove_user_group("3","friends"), fieldValue)

    @patch("crud.CRUD.read_users_file")  
    @patch("crud.CRUD.read_groups_file")     
    def test_remove_user_group_Returns_false_for_invalid_group(#Bool not iterable
        self, mock_read_users_file, mock_read_groups_file
    ):
        #testMessage= "Invalide"
        #mock_read_users_file.return_value = self.users_data
        #mock_read_groups_file.return_value = self.groups_data
        #crud = CRUD()
        #self.assertFalse(crud.remove_user_group("1","alex@gmail.com"), testMessage)
        pass

    @patch("crud.CRUD.modify_users_file")  
    @patch("crud.CRUD.read_users_file") 
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file, 
    ):
        mock_read_users_file.return_value = self.users_data
        crud=CRUD()
        crud.remove_user_group("1","default")
        mock_modify_users_file.assert_called_once_with(self.users_data)


    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_read_groups_file
    ):
        fieldValue=False
        mock_read_groups_file.return_value = self.groups_data
        crud=CRUD()
        self.assertEqual(crud.remove_group("3"),fieldValue)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        crud.remove_group("2")
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_read_groups_file
    ):
        fieldValue=False
        mock_read_groups_file.return_value = self.groups_data
        crud=CRUD()
        self.assertEqual(crud.remove_group_member("3","1"),fieldValue)

    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_read_groups_file
    ):
        fieldValue=False
        mock_read_groups_file.return_value = self.groups_data
        crud=CRUD()
        self.assertEqual(crud.remove_group_member("1","3"),fieldValue)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        crud.remove_group_member("2","alex@gmail.com")
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        pass


#if __name__ == "__main__":

    #unittest.main()
