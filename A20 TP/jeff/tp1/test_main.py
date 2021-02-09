import json
import unittest
from email_analyzer_tp1 import EmailAnalyzer

class TestMain(unittest.TestCase):

    def evaluate(self, vocab, test_file):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        total = 0

        # Mettre le vocabulary qu'on veut utiliser
        analyzer = EmailAnalyzer(vocab)

        # Mettre le bon fichier test
        with open(test_file) as email_file:
            new_emails = json.load(email_file)

        for e_mail in new_emails["dataset"]:
            #print('loading')
            new_email = e_mail["mail"]
            subject = new_email["Subject"]
            body = new_email["Body"]
            spam = new_email["Spam"]

            if ((analyzer.is_spam(subject, body))) and (spam == "true"):
                tp += 1
            if (not (analyzer.is_spam(subject, body))) and (spam == "false"):
                tn += 1
            if ((analyzer.is_spam(subject, body))) and (spam == "false"):
                fp += 1
            if (not (analyzer.is_spam(subject, body))) and (spam == "true"):
                fn += 1
            total += 1
        print("Accuracy: ", (tp + tn) / (tp + tn + fp + fn))
        print("Precision: ", tp / (tp + fp))
        print("Recall: ", tp / (tp + fn))
        return (tp + tn) / (tp + tn + fp + fn)

    def setUp(self):
        print('Accuracy initiale')
        self.baseAccuracy = self.evaluate('vocabulary_train700.json', 'test300.json')

    def test_permutative_emails_train(self):
        """
        test pour apres changement de l'ordre
        des e-mails dans le 'train dataset'
        """
        print("Property: permutative test")
        diff = abs(self.evaluate('vocabulary_train700_mails.json', 'test300.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_permutative_emails_test(self):
        """
        test pour apres changement de l'ordre
        des e-mails dans le 'test dataset'
        """
        print("Après changement de l'ordre des e-mails dans le train dataset")
        diff = abs(self.evaluate('vocabulary_train700.json', 'test300_mails.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_permutative_words_train(self):
        """
        test pour apres changement de l'ordre
        des mots dans le 'train dataset'
        """
        print("Après changement de l'ordre des mots dans le train dataset")
        diff = abs(self.evaluate('vocabulary_train700_words.json', 'test300.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_permutative_words_test(self):
        """
        test pur apres changement de l'ordre
        des mots dans le 'test dataset'
        """
        print("Après changement de l'ordre des mots dans le test dataset")
        diff = abs(self.evaluate('vocabulary_train700.json', 'test300_words.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_multiplicative_emails_train(self):
        """
        test pour apres l'ajout des memes e-mails
        dans le 'train dataset'
        """
        print("Après l'ajout des mêmes emails dans le train dataset")
        diff = abs(self.evaluate('vocabulary_train700x2.json', 'test300.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_multiplicative_emails_test(self):
        """
        test pour apres l'ajout des memes e-mails
        dans le 'test dataset'
        """
        print("Après l'ajout des mêmes emails dans le test dataset")
        diff = abs(self.evaluate('vocabulary_train700.json', 'test300x2.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_inclusive_words_train(self):
        """
        test pour pres l'ajout du 'bruit' dans
        le 'train dataset'
        """
        print("Après l'ajout du bruit dans le train dataset")
        diff = abs(self.evaluate('vocabulary_train700_noise.json', 'test300.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)

    def test_inclusive_words_test(self):
        """
        test pour apres l'ajout du 'bruit' dans
        le 'test dataset'
        """
        print("Après l'ajout du bruit dans le test dataset")
        diff = abs(self.evaluate('vocabulary_train700.json', 'test300_noise.json') - self.baseAccuracy)
        print('différence: ', diff)
        self.assertLessEqual(diff, 0.03)
