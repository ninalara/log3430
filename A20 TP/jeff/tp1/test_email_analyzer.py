from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject_true = " best deals on c ia . lis around here ."
        self.subject_false = " important video announcement"
        self.body_true = "top of the morning to you ! : )\nsick of feeling left out ? want\nto try that\nawesome\nfeeling of being a man again ?\nuse ci 4 lis instead of\nvlagra . it is : - longer -\nguarantees about 36 hour lasting - safer . -\nharder erections\n"
        self.body_false = "i have a very important video announcement about the future of our company . please go to to access the video . thank you \n"

        self.clean_subject_true = ['best', 'deal', 'li', 'around']  # données pour mocker "return_value" du "clean_text"
        self.clean_body_true = ['top', 'morn', 'sick', 'feel', 'left', 'want', 'tri', 'awesom', 'feel', 'man', 'use', 'li', 'instead', 'vlagra', 'longer', 'guarante', 'hour', 'last', 'safer', 'harder', 'erect']  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_false = ['carnegi', 'mellon', 'resum', 'pre', 'select', 'list']
        self.clean_body_false = ['hello', 'everyon', 'time', 'spring', 'recruit', 'season', 'begin', 'select', 'candid', 'would', 'like', 'pre', 'select', 'list', 'coordin', 'hand', 'resum', 'book', 'morn', 'pleas', 'call', 'alys', 'extens', 'locat', 'sure', 'get', 'resum', 'book', 'pleas', 'email', 'top', 'pick', 'noon', 'friday', 'januari', 'thank']
        self.body_spam_ham_prob_true = (
            2.4529329450226196e-76,
            4.620187635424194e-78
        )  # données pour mocker "return_value" du "body_spam_ham_prob"
        self.subject_spam_ham_prob_true = (
            1.1267778086216149e-11,
            5.632188962559908e-12,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.body_spam_ham_prob_false = (
            8.326714930230154e-28,
            7.309503972510971e-30
        )  # données pour mocker "return_value" du "body_spam_ham_prob"
        self.subject_spam_ham_prob_false = (
            1.7061001894880694e-10,
            3.380045493598245e-10
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
            {
                "best": 0.008917197452229299,
                "best": 0.0013782480035672302,
                "deal": 0.0006688556487899793,
                "li": 0.0012738853503184713,
                "around": 0.00024322023592362885,
                "top": 0.00040364313806665286,
                "morn": 0.0007555371558683503,
                "sick": 0.00010134176496817869,
                "feel": 0.0005877822368154364,
                "left": 0.00012161011796181443,
                "want": 0.001666321672531567,
                "tri": 0.0012738853503184713,
                "awesom": 0.0006369426751592356,
                "feel": 0.0005877822368154364,
                "man": 0.0005877822368154364,
                "use": 0.0019043676257503622,
                "instead": 8.107341197454295e-05,
                "vlagra": 8.107341197454295e-05,
                "longer": 0.0001552473607948665,
                "guarante": 0.0001552473607948665,
                "hour": 0.014106583072100314,
                "last": 0.0010449320794148381,
                "safer": 2.026835299363574e-05,
                "harder": 2.026835299363574e-05,
                "erect": 0.0012738853503184713,
                "uncl": 0.0006369426751592356,
                "rummi": 0.0006369426751592356,
                "hangov": 0.0006369426751592356,
                "pill": 0.001910828025477707,
                "absolut": 0.0006369426751592356,
                "new": 0.006369426751592357,
                "naeyc": 0.0006369426751592356,
                "receiv": 0.0006369426751592356,
                "greet": 0.0006369426751592356,
                "famili": 0.0006369426751592356,
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_vocab"
        self.body_spam_ham_prob_expected = 2.4529329450226196e-76, 4.620187635424194e-78  # valeurs de la probabilité attendus
        self.subject_spam_ham_prob_expected = 1.1267778086216149e-11, 5.632188962559908e-12  # valeurs de la probabilité attendus

    def tearDown(self):
        pass

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.body_spam_ham_prob")
    @patch("email_analyzer.EmailAnalyzer.subject_spam_ham_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_subject_spam_ham_prob, mock_body_spam_ham_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_clean_text.return_value = self.clean_subject_true
        mock_subject_spam_ham_prob.return_value = self.subject_spam_ham_prob_true

        mock_clean_text.return_value = self.clean_body_true
        mock_body_spam_ham_prob.return_value = self.body_spam_ham_prob_true

        email_analyzer = EmailAnalyzer()
        self.assertEqual(email_analyzer.is_spam(self.subject_true, self.body_true), True)

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.body_spam_ham_prob")
    @patch("email_analyzer.EmailAnalyzer.subject_spam_ham_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_subject_spam_ham_prob, mock_body_spam_ham_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam  probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_clean_text.return_value = self.clean_subject_false
        mock_subject_spam_ham_prob.return_value = self.subject_spam_ham_prob_false

        mock_clean_text.return_value = self.clean_body_false
        mock_body_spam_ham_prob.return_value = self.body_spam_ham_prob_false

        email_analyzer = EmailAnalyzer()
        self.assertEqual(email_analyzer.body_spam_ham_prob(self.body_false), self.body_spam_ham_prob_false)
        self.assertEqual(email_analyzer.subject_spam_ham_prob(self.subject_false), self.subject_spam_ham_prob_false)
        self.assertEqual(email_analyzer.is_spam(self.subject_false, self.body_false), False)

    @patch("email_analyzer.EmailAnalyzer.load_vocab")
    def test_body_spam_ham_prob_Returns_expected_probability(self, mock_load_vocab):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement donné le "body" à l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        email_analyzer = EmailAnalyzer()
        mock_load_vocab.return_value = self.vocab
        self.assertEqual(email_analyzer.body_spam_ham_prob(self.body_true), self.body_spam_ham_prob_expected)

    @patch("email_analyzer.EmailAnalyzer.load_vocab")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_vocab):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement donné le "sujet" a l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        email_analyzer = EmailAnalyzer()
        mock_load_vocab.return_value = self.vocab
        self.assertEqual(email_analyzer.subject_spam_ham_prob(self.subject_true), self.subject_spam_ham_prob_expected)



# if __name__ == "__main__":
#
#     unittest.main()
