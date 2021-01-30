from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch


class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
                {
                    "mail": {
                        "Subject": " best online medicine here",
                        "From": "BG@paris.com",
                        "Date": "2004-11-18",
                        "Body": "get any prescription drug you want !\nsimple quick and affordable !",
                        "Spam": "true",
                        "File": "enronds//enron3/spam/1429.2004-11-18.BG.spam.txt"
                    }

                },
                {
                    "mail": {
                        "Subject": " netco due diligence",
                        "From": "kitchen@paris.com",
                        "Date": "2002-01-02",
                        "Body": "big pig :\nmet with them today and gave an overview of operations .\n",
                        "Spam": "false",
                        "File": "enronds//enron3/ham/4774.2002-01-02.kitchen.ham.txt"
                    }

                }
                ]}  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam =  ["best", "online", "medicine", "here"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ["prescription", "drug", "simple", "quick", "affordable"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ["netco", "due", "diligence"] # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham =  ["big", "pig", "met", "today", "overview", "operations"] # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            "spam_sub": {
                "best": 1/4,
                "online": 1/4,
                "medicine": 1/4,
                "here": 1/4,
            },
            "ham_sub": {
                "netco": 1/3,
                "due": 1/3,
                "diligence": 1/3
            },
            "spam_body": {
                "prescription": 1/5,
                "drug": 1/5,
                "simple": 1/5,
                "quick": 1/5,
                "affordable": 1/5
            },
            "ham_body": {
                "big": 1/6,
                "pig": 1/6,
                "met": 1/6,
                "today": 1/6,
                "overview": 1/6,
                "operations": 1/6
            }
        }  # vocabulaire avec les valuers de la probabilité calculées correctement
        self.vocabulary_creator = VocabularyCreator()

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme un return value simulé),"clean text"
         (cette fonction va être appelé quelques fois, pour chaque appel on
         va simuler la return_value different, pour cela il faut utiliser
         side_effect (vois l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appele_a_create_vocab(), self.vocab_expected)
        """
        mock_load_dict.return_value = self.mails
        list_of_values = [self.clean_subject_spam, self.clean_body_spam, self.clean_subject_ham, self.clean_body_ham]

        mock_clean_text.side_effect = list_of_values
        mock_write_data_to_vocab_file.return_value = True
        self.assertEqual(self.vocabulary_creator.create_vocab(), self.vocab_expected)

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    def test_count_spam_should_return_correct_number_of_spam(self, mock_load_dict):
        mock_load_dict.return_value = self.mails
        self.assertEqual(self.vocabulary_creator.count_spam(), 1)

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    def test_count_emails_should_return_correct_number_of_emails(self, mock_load_dict):
        mock_load_dict.return_value = self.mails
        self.assertEqual(self.vocabulary_creator.count_emails(), 2)

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    def test_count_ham_should_return_correct_number_of_hams(self, mock_load_dict):
        mock_load_dict.return_value = self.mails
        self.assertEqual(self.vocabulary_creator.count_ham(), 1)

#if __name__ == "__main__":

  #  unittest.main()
