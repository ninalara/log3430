import unittest
from email_analyzer_tp4 import EmailAnalyzer
import json
import random

class TestMain(unittest.TestCase):

    def evaluate(self, vocab_file, test_file):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        total = 0
        analyzer = EmailAnalyzer(vocab_file)
        with open(test_file) as email_file:
            new_emails = json.load(email_file)

        i = 0
        email_count = len(new_emails["dataset"])

        print("Evaluating emails ")
        for e_mail in new_emails["dataset"]:
            i += 1
            print("\rEmail " + str(i) + "/" + str(email_count), end="")

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
        
        print("")
        print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
        print("Precision: ", round(tp / (tp + fp), 2))
        print("Recall: ", round(tp / (tp + fn), 2))
        return (tp + tn) / (tp + tn + fp + fn)
    
    def setUp(self):
        self.baseAccuracy=self.evaluate('vocabulary.json', 'train_set.json')

    def test_permutate_emails_train(self):
        print("changement de l’ordre des e-mails dans le train dataset\n")
        with open("train_set.json") as email_file:
            new_emails = json.load(email_file)
        new_emails = random.shuffle(list(new_emails.get("mail")))
        with open("train700_mails.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'train700_mails.json')
        difference = abs(newAccuracy - self.baseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)

    def test_permutate_emails_test(self):
        print("changement de l’ordre des e-mails dans le test dataset\n")
        with open("test_set.json") as email_file:
            new_emails = json.load(email_file)
        new_emails = random.shuffle(list(new_emails.get("mail")))
        with open("test300_mails.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'test300_mails.json')
        difference = abs(newAccuracy - self.baseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)

    # def test_permutate_words_train(self):
    #    print("changement de l’ordre des mots dans le train dataset\n")
    #     with open("test_set.json") as email_file:
    #         new_emails = json.load(email_file)
    #     for e_mail in new_emails["dataset"]:
    #        subject = random.shuffle((e_mail.get("Subject")).split(" "))
    #        body = random.shuffle((e_mail.get("Body")).split(" "))
    #        e_mail['Subject'] = subject
    #        e_mail['Body'] = body
    #     with open("train700_words.json", "w") as outfile:
    #         json.dump(new_emails, outfile)
    #     newAccuracy = self.evaluate('vocabulary.json', 'train700_words.json')
    #     difference = abs(newAccuracy - self.baseAccuracy)
    #     print("difference: ", difference)
    #     print("\n")
    #     self.assertLessEqual(difference, 0.03)

    # def test_permutate_words_test(self):
    #     print("changement de l’ordre des mots dans le train dataset\n")
    #     with open("test_set.json") as email_file:
    #         new_emails = json.load(email_file)
    #     for e_mail in new_emails["dataset"]:
    #         subject = random.shuffle(str(e_mail.get("Subject")).split(" "))
    #         body = random.shuffle(str(e_mail.get("Body")).split(" "))
    #         e_mail['Subject'] = subject
    #         e_mail['Body'] = body
    #     with open("test300_words.json", "w") as outfile:
    #         json.dump(new_emails, outfile)
    #     newAccuracy = self.evaluate('vocabulary.json', 'test300_words.json')
    #     difference = abs(newAccuracy - self.baseAccuracy)
    #     print("difference: ", difference)
    #     print("\n")
    #     self.assertLessEqual(difference, 0.03)


    # def test_double_email_test(self):
    #     print("ajout des memes e-mails dans le test dataset\n")
    #     with open("test_set.json") as email_file:
    #         new_emails = json.load(email_file)
        
    #     for k, v in new_emails.items():
    #         new_emails[k].extend(v)
            
    #     with open("test300x2.json", "w") as outfile:
    #         json.dump(new_emails, outfile)
    #     newAccuracy = self.evaluate('vocabulary.json', 'test300x2.json')
    #     difference = abs(newAccuracy - self.baseAccuracy)
    #     print("difference: ", difference)
    #     print("\n")
    #     self.assertLessEqual(difference, 0.03)

    def test_double_email_train(self):
        print("ajout des memes e-mails dans le train dataset\n")
        with open("train_set.json") as email_file:
            new_emails = json.load(email_file)
        
        for k, v in new_emails.items():
            new_emails[k].extend(v)
            
        with open("train700x2.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'train700x2.json')
        difference = abs(newAccuracy - self.baseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)

    #def test_noise_train(self):
        # ajout du ”bruit” dans le ”train dataset”
        
    #def test_noise_test(self):
        # ajout du ”bruit” dans le ”test dataset”

    