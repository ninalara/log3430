from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
            {
                "mail": {
                "Subject": " software taking a bite out of your budget ? try oem !",
                "From": "SA_and_HP@paris.com",
                "Date": "2005-07-17",
                "Body":"can t draw a straight line ? well . . . now you can !\nthey have computers and they may have other weapons of mass destruction .\nhe who limps still walks \n",
                "Spam": "true",
                "File": "enronds//enron2/spam/4907.2005-07-17.SA_and_HP.spam.txt"
                }
            },
            {
                "mail": {
                "Subject": " i m assuming the nymex desk will get 12 million of var .",
                "From": "kitchen@paris.com",
                "Date": "2002-01-29",
                "Body":"if you allocate out about 50 million and gas gets 30 million of that 12 seems reasonable .\nwhat do you think \n",
                "Spam": "false",
                "File": "enronds//enron3/ham/5322.2002-01-29.kitchen.ham.txt"
                }
            }]
        }  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = ['softwar', 'take', 'bite', 'budget', 'tri', 'oem']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ['draw', 'straight', 'line', 'well', 'comput', 'may', 'weapon', 'mass', 'destruct', 'limp', 'still', 'walk']  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ['assum', 'nymex', 'desk', 'get', 'million', 'var']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ['alloc', 'million', 'ga', 'get', 'million', 'seem', 'reason', 'think']  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            "spam_sub": {
                "softwar": 1/6,
                "take": 1/6,
                "bite": 1/6,
                "budget": 1/6,
                "tri": 1/6,
                "oem": 1/6
            },
            "ham_sub": {
                "assum": 1/6,
                "nymex": 1/6,
                "desk": 1/6,
                "get": 1/6,
                "million": 1/6,
                "var": 1/6
            },
            "spam_body": {
                "draw": 1/12,
                "straight": 1/12,
                "line": 1/12,
                "well": 1/12,
                "comput": 1/12,
                "may": 1/12,
                "weapon": 1/12,
                "mass": 1/12,
                "destruct": 1/12,
                "limp": 1/12,
                "still": 1/12,
                "walk": 1/12,
            },
            "ham_body": {
                "alloc": 1/8,
                "million": 2/8,
                "ga": 1/8,
                "get": 1/8,
                "seem": 1/8,
                "reason": 1/8,
                "think": 1/8
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
        mock_load_dict.return_value = self.mails
        mock_clean_text.side_effect = [ self.clean_subject_spam, self.clean_subject_ham, self.clean_body_spam, self.clean_body_ham ]
        mock_write_data_to_vocab_file.return_value = True
        vocabulary_creator = VocabularyCreator()
        self.assertEqual(vocabulary_creator.create_vocab(), True)

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


#if __name__ == "__main__":

  #  unittest.main()
