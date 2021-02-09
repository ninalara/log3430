from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
                "dataset": [
                    {
                    "mail": {
                    "Subject": "best online medicine here",
                    "From": "BG@paris.com",
                    "Date": "2004-11-18",
                    "Body":"colicky westinghouse denote edna covenant\nget any prescription drug you want !\nsimple quick and affordable !\nwe deliver quality medications to your door !\nstop getting brochures here\ncoercive bottle gwen neolithic constipate burnham\n",
                    "Spam": "true",
                    "File": "enronds//enron3/spam/1429.2004-11-18.BG.spam.txt"
                        } 
                    },
                    {
                    "mail": {
                    "Subject": " industrial accounts",
                    "From": "farmer@paris.com",
                    "Date": "2000-01-10",
                    "Body":"i will leave robert to the above accounts . i will refer all contacts on this\nsubject to him for handling .\nit is my personal belief that robert is not yet ready to provide all the\nservices necessary in this area but i also know that full responsibility\noften is a good teacher .\npat as far as i m concerned i m out of the game .\ni will help daren if needed and if not i ll be on my way .\ngood luck to you in your endeavors \n",
                    "Spam": "false",
                    "File": "enronds//enron1/ham/0158.2000-01-10.farmer.ham.txt"
                        }
                    }
                ]
            }  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = [ "best", "onlin", "medicin" ]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = [ "colicki", "westinghous", "denot", "edna", "coven", "get", "prescript", "drug", "want", "simpl",
                "quick", "afford", "deliv", "qualiti", "medic", "door", "stop", "brochur", "coerciv", "bottl", "gwen", 
                "neolith", "constip", "burnham"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = [ "industri", "account" ]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ["leav", "robert", "account", "refer", "contact", "subject", "handl", "person", "belief", 
                "yet", "readi", "provid", "servic", "necessari", "area", "also", "know", "full", "respons", "often", "good",
                "teacher", "pat", "far", "concern", "game", "help", "daren", "need", "way", "luck", "endeavor"]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
                "spam_sub": {
                    "best": 0.3333,
                    "onlin": 0.3333,
                    "medicin": 0.3333
                    },
                "ham_sub": {
                    "industri": 0.5,
                    "account": 0.5
                    },
                "spam_body": {
                    "colicki": 0.0385,
                    "westinghous": 0.0385,
                    "denot": 0.0385,
                    "edna": 0.0385,
                    "coven": 0.0385,
                    "get": 0.0769,
                    "ani": 0.0385,
                    "prescript": 0.0385,
                    "drug": 0.0385,
                    "want": 0.0385,
                    "simpl": 0.0385,
                    "quick": 0.0385,
                    "afford": 0.0385,
                    "deliv": 0.0385,
                    "qualiti": 0.0385,
                    "medic": 0.0385,
                    "door": 0.0385,
                    "stop": 0.0385,
                    "brochur": 0.0385,
                    "coerciv": 0.0385,
                    "bottl": 0.0385,
                    "gwen": 0.0385,
                    "neolith": 0.0385,
                    "constip": 0.0385,
                    "burnham": 0.0385
                    },
                "ham_body": {
                    "leav": 0.027,
                    "robert": 0.0541,
                    "abov": 0.027,
                    "account": 0.027,
                    "refer": 0.027,
                    "contact": 0.027,
                    "thi": 0.0541,
                    "subject": 0.027,
                    "handl": 0.027,
                    "person": 0.027,
                    "belief": 0.027,
                    "yet": 0.027,
                    "readi": 0.027,
                    "provid": 0.027,
                    "servic": 0.027,
                    "necessari": 0.027,
                    "area": 0.027,
                    "also": 0.027,
                    "know": 0.027,
                    "full": 0.027,
                    "respons": 0.027,
                    "often": 0.027,
                    "good": 0.0541,
                    "teacher": 0.027,
                    "pat": 0.027,
                    "far": 0.027,
                    "concern": 0.027,
                    "game": 0.027,
                    "help": 0.027,
                    "daren": 0.027,
                    "need": 0.027,
                    "way": 0.027,
                    "luck": 0.027,
                    "endeavor": 0.027
                    }
        }  # vocabulaire avec les valuers de la probabilité calculées correctement

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
        vocabulary_creator = VocabularyCreator()
        mock_load_dict.return_value = self.mails
        mock_clean_text.side_effect = [ self.clean_subject_spam, self.clean_subject_ham, 
                self.clean_body_spam, self.clean_body_ham ]
        mock_write_data_to_vocab_file.return_value = True
        self.assertEqual(vocabulary_creator.create_vocab(1), self.vocab_expected)
