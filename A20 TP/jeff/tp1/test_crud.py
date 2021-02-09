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

        #données mock pour "return value" de modify_users_file


    def tearDown(self):
        pass


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_users_file, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud.add_new_user("bonjour@email.com", "2020-10-24")
        mock_modify_users_file.assert_called_once_with(self.users_data)

        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file", "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour l'utilisateur a étée formée correctement par la fonction, e.g.
        self.modify_users_file(data) -> "data" doit avoir un format et contenu expectee
        il faut utiliser ".assert_called_once_with(expected_data)"
        """

    #Test ajouté pour augmenter le coverage, en atteignant le except: dans add_new_user
    @patch("crud.CRUD.read_users_file")
    def test_add_new_user_Exception_raised_to_modify_users_file(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = None
        self.assertFalse(crud.add_new_user("bonjour@email.com", "2020-10-24"))


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        crud.add_new_group("test", "50", ["test"])
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a étée formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """

    #Test ajouté pour augmenter le coverage, en atteignant l'exception dans add_new_group()
    @patch("crud.CRUD.read_groups_file")
    def test_add_new_group_Exception_Raised_to_modify_groups_file(
            self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = None
        self.assertFalse(crud.add_new_group("test", "50", ["test"]))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_data("3", "name"))
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si ID non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_data(1, 'INVALIDE'))
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si champ non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data("1", "name"), "alex@gmail.com")
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ est id valide sont utilisee
        il faut utiliser ".assertEqual()"
        """

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """"""

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_group_data('3', "name"))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.get_group_data('1', 'INVALID'))
        """"""
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertEqual(crud.get_group_data('1', 'name'), 'default')
        """"""
        pass

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        self.assertFalse(crud.get_user_id('INVALID'))
        pass

    #Test ajouté pour augmenter notre coverage, en atteignant l'exception dans get_user_id()
    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Exception_raised_for_valid_user_name(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = None
        self.assertFalse(crud.get_user_id('1'))
        pass

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        self.assertEqual(crud.get_user_id('alex@gmail.com'), "1")
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.get_group_id('INVALID'))
        pass

    #Test ajouté pour augmenter notre coverage, en atteignant l'exception dans get_group_id()
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Exception_raised_for_valid_group_name(self, mock_read_groups_file):
        crud = CRUD()
        mock_read_groups_file.return_value = None
        self.assertFalse(crud.get_group_id("default"))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertEqual(crud.get_group_id("default"), "1")
        pass

    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_id(
            self, mock_read_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.update_users(10, "name", "12@gmail.com"), False)
        pass

    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_field(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        self.assertFalse(crud.update_users("1", "INVALID", "DATA"))
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """


        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        crud.update_users('1', "name", "NEW")
        mock_modify_users_file.return_value = True
        mock_modify_users_file.assert_called_once_with(self.users_data)

        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        pass

    #Test ajouté pour augmenter notre coverage, en atteignant l'exception dans update_users()
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Exception_raised_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = None
        self.assertFalse(crud.update_users('1', "name", "NEW"))

        pass

    #Test ajouté pour augmenter notre coverage, en testant une condition if dans notre fonction update_users()
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_groups_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        crud.update_users('1', "Groups", "New Group")
        mock_modify_users_file.return_value = True
        mock_modify_users_file.assert_called_once_with(self.users_data)
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.update_groups('10', 'name', 'TEST'))
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.update_groups('1', 'INVALID', 'TEST'))
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        pass


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        crud.update_groups('1', 'name', 'NEW')
        mock_modify_groups_file.return_value = True
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        pass

    #Test ajouté pour augmenter notre coverage, en atteignant l'exception dans update_groups()
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Exception_raised_to_modify_groups_file(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = None
        self.assertFalse(crud.update_groups('1', 'name', 'NEW'))
        pass

    #Test ajouté pour augmenter notre coverage, en atteignant un if condition dans update_groups()
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_list_of_members_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        crud.update_groups('1', 'List_of_members', 'New Member')
        mock_modify_groups_file.return_value = True
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

        pass

    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        self.assertFalse(crud.remove_user('10'))
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        crud.remove_user(1)
        mock_modify_users_file.assert_called_once_with(self.users_data)
        pass

    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        self.assertFalse(crud.remove_user_group('10', 'default'))
        pass

    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_group(
        self, mock_read_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        self.assertFalse(crud.remove_user_group('1', 'INVALID'))
        pass

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        crud = CRUD()
        mock_read_users_file.return_value = self.users_data
        crud.remove_user_group('1', 'default')
        mock_modify_users_file.return_value = True
        mock_modify_users_file.assert_called_once_with(self.users_data)
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.remove_group(10))
        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        crud.remove_group('1')
        mock_modify_groups_file.return_value = True
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        pass

    #Test ajouté poug augmenter notre coverage, en atteignant l'exception de remove_group()
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Exception_raised_to_modify_groups_file(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = None
        self.assertFalse(crud.remove_group('1'))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.remove_group_member('10', 'alex@gmail.com'))
        pass

    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_read_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        self.assertFalse(crud.remove_group_member('1', 'INVALID'))
        pass

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        crud = CRUD()
        mock_read_groups_file.return_value = self.groups_data
        crud.remove_group_member('1', 'alex@gmail.com')
        mock_modify_groups_file.return_value = True
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
        pass


#if __name__ == "__main__":

    #unittest.main()
