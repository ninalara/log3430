import json
from email_analyzer import EmailAnalyzer
import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = EmailAnalyzer()
        self.subject_true = " no more outdated software ! upgrade !"
        self.body_true = "we get you the best deal ! skip the retail box and save !\namazing special # 1 :\nadobe - photoshop 7 premiere 7 illustrator 10 = only $ 120\namazing special # 2 :\nwindows xp professional + microsoft office xp professional = only $ 80\namazing special # 3 :\nadobe photoshop cs + adobe illustrator cs + adobe indesign cs\namazing special # 4 :\n"
        self.clean_subject_true = ['more', 'oudat', 'software', 'upgrade']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_true = ['get', 'best', 'deal', 'skip', 'retail', 'box', 'sav', 'amaz', 'special', 'adobe', 'photoshop', 'premiere', 'illustrator', 'only', 'windows', 'xp', 'professional', 'microsoft', 'office', 'cs', 'indesign']  # données pour mocker "return_value" du "clean_text"
        self.subject_false = "re :"
        self.body_false = "we are using it for other things . mary joyce and robert have discussed with mcmahon and bowen .\n- - - - - original message - - - - -\nfrom : kitchen louise\nsent : monday december 10 2001 8 : 26 am\nto : oxley david\nsubject :\nwhat happens to the money in wachovia ?\nlouise kitchen\nchief operating \n"
        self.clean_subject_false = ['re']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_false = ['us', 'other', 'thing', 'mary', 'joyce', 'robert', 'discuss', 'mcmahon', 'bowen', 'original', 'message', 'kitchen', 'louise', 'sent', 'monday', "december", 'oxley', 'david', 'subject', 'happen', 'money', 'wachovia'] 
        self.spam_ham_body_prob_true = (
            1,
            (1/6),
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.subject_spam_ham_prob_true = (
            (2/3),
            (1/6),
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            (1/4),
            (2/6),
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.subject_spam_ham_prob_false = (
            0,
            (1/2),
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
            {
                "p_sub_spam": {
                    "upgrade" : 1/3,
                    "software" : 1/3
                },
                "p_sub_ham": {
                    "re" : 1/2,
                    "annoucement" : 1/6,
                    "more" : 1/6
                },
                "p_body_spam": {
                    "best" : 1/4,
                    "deal" : 1/4,
                    "skip" : 1/4,
                    "special" : 1/4,
                    "money" : 1/4
                },
                "p_body_ham": {
                    "today": 1/6,
                    "professional" : 1/6,
                    "meet" : 1/6,
                    "discuss" : 1/6,
                    "sent" : 1/6
                }
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        # valeurs de la probabilité attendus : (0.5925*1/(256*pow(6,17))), (0.4075*1/pow(6,21)) 
        self.spam_ham_body_prob_expected = (1.3673419333309543e-16, 1.8575963755415577e-17)  
        # valeurs de la probabilité attendus : (0.5925*1/81, 0.4075*1/6*1/4*1/4*1/4)  
        self.subject_spam_ham_prob_expected = (0.007314814814814815, 0.0010611979166666665)  

    def tearDown(self):
        pass

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_subject_spam_ham_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        mock_subject_spam_ham_prob.return_value =  self.subject_spam_ham_prob_true
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_true
        return_val = self.analyzer.is_spam(self.subject_true,self.body_true)
        self.assertTrue(return_val)
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_subject_spam_ham_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        mock_subject_spam_ham_prob.return_value = self.subject_spam_ham_prob_false
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_false
        return_val = self.analyzer.is_spam(self.subject_false,self.body_false)
        self.assertFalse(return_val)
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam  probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        self.assertEqual(self.analyzer.spam_ham_body_prob(self.clean_body_true), self.spam_ham_body_prob_expected)
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement donné le "body" à l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        self.assertEqual(self.analyzer.spam_ham_subject_prob(self.clean_subject_true), self.subject_spam_ham_prob_expected)
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement donné le "sujet" a l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """


#if __name__ == "__main__":

    #unittest.main()
