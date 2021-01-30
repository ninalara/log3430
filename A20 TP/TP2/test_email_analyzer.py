import json

from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = "dummySubject"
        self.body = "dummyBody"
        self.analyzer = EmailAnalyzer()
        self.clean_subject = ["best", "quick", "netco"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body = ["prescription", "drug", "overview",
                           "operations"]  # données pour mocker "return_value" du "clean_text"
        self.spam_ham_body_prob_true = (
            0,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.subject_spam_ham_prob_true = (
            0,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            0,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.subject_spam_ham_prob_false = (
            0,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
            {
                "spam_sub": {
                    "best": 1 / 4,
                    "online": 1 / 4,
                    "medicine": 1 / 4,
                    "here": 1 / 4,
                },
                "ham_sub": {
                    "netco": 1 / 3,
                    "due": 1 / 3,
                    "diligence": 1 / 3
                },
                "spam_body": {
                    "prescription": 1 / 5,
                    "drug": 1 / 5,
                    "simple": 1 / 5,
                    "quick": 1 / 5,
                    "affordable": 1 / 5
                },
                "ham_body": {
                    "big": 1 / 6,
                    "pig": 1 / 6,
                    "met": 1 / 6,
                    "today": 1 / 6,
                    "overview": 1 / 6,
                    "operations": 1 / 6
                }
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 0, 0  # valeurs de la probabilité attendus
        self.subject_spam_ham_prob_expected = 0, 0  # valeurs de la probabilité attendus

    def tearDown(self):
        pass

    @patch("email_analyzer.EmailAnalyzer.subject_spam_ham_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
            self, mock_subject_spam_ham_prob, mock_spam_ham_body_prob
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_subject_spam_ham_prob.return_value = (10, 0)
        mock_spam_ham_body_prob.return_value = (10, 0)
        is_spam_return_val = self.analyzer.is_spam("dummySubject", "dummyBody")
        self.assertTrue(is_spam_return_val)

    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.subject_spam_ham_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
            self, mock_subject_spam_ham_prob, mock_spam_ham_body_prob
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam  probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_subject_spam_ham_prob.return_value = (0, 10)
        mock_spam_ham_body_prob.return_value = (0, 10)
        is_spam_return_val = self.analyzer.is_spam("dummySubject", "dummyBody")
        self.assertFalse(is_spam_return_val)

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.calculate_ham_divided_by_email")
    @patch("email_analyzer.EmailAnalyzer.calculate_spam_divided_by_email")
    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict, mock_calculate_spam_divided_by_email,
                                                             mock_calculate_ham_divided_by_email, mock_clean_text):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement donné le "body" à l'entrée
        (ces probabilites devront etre calcule selon l'enonce dans le TP1 )
        """
        mock_load_dict.return_value = self.vocab
        mock_calculate_ham_divided_by_email.return_value = 1 / 2
        mock_calculate_spam_divided_by_email.return_value = 1 / 2
        mock_clean_text.return_value = self.clean_body
        expected_return_value = ((0.5 * 0.2 * 0.2), (1 / 2 * 1 / 6 * 1 / 6))
        self.assertEqual(self.analyzer.spam_ham_body_prob(self.body), expected_return_value)

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.calculate_ham_divided_by_email")
    @patch("email_analyzer.EmailAnalyzer.calculate_spam_divided_by_email")
    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict,
                                                                mock_calculate_spam_divided_by_email,
                                                                mock_calculate_ham_divided_by_email, mock_clean_text):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement donné le "sujet" a l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_load_dict.return_value = self.vocab
        mock_calculate_ham_divided_by_email.return_value = 1 / 2
        mock_calculate_spam_divided_by_email.return_value = 1 / 2
        mock_clean_text.return_value = self.clean_subject
        expected_return_value = ((0.5 * 0.25), (0.5*1/3))
        self.assertEqual(self.analyzer.subject_spam_ham_prob(self.subject), expected_return_value)

# if __name__ == "__main__":

# unittest.main()
