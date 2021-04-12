import unittest
from email_analyzer_tp4 import EmailAnalyzer
import json
import random

class TestMain(unittest.TestCase):

    def init_evaluate(self, vocab_file, test_file):
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

        # print("Evaluating emails ")
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
        
        print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
        # print("Precision: ", round(tp / (tp + fp), 2))
        # print("Recall: ", round(tp / (tp + fn), 2))
        return (tp + tn) / (tp + tn + fp + fn)
    
    def evaluate(self, vocab_file, test_file, is_test):
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

        # print("Evaluating emails ")
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
        
        if(is_test):
            print("\nInitial Accuracy: ",self.testbaseAccuracy)
        else:
            print("\nInitial Accuracy: ",self.trainbaseAccuracy)
        print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
        # print("Precision: ", round(tp / (tp + fp), 2))
        # print("Recall: ", round(tp / (tp + fn), 2))
        return (tp + tn) / (tp + tn + fp + fn)
    
    def setUp(self):
        self.trainbaseAccuracy=self.init_evaluate('vocabulary.json', 'train_set.json')
        self.testbaseAccuracy=self.init_evaluate('vocabulary.json', 'test_set.json')

    def test_permutate_emails_train(self):
        print("\nchangement de l’ordre des e-mails dans le train dataset\n")
        with open("train_set.json") as email_file:
            new_emails = json.load(email_file)
        random.shuffle(new_emails["dataset"])
        with open("train700_mails.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'train700_mails.json', False)
        difference = abs(newAccuracy - self.trainbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)
    
    def test_permutate_emails_test(self):
        print("\nchangement de l’ordre des e-mails dans le test dataset\n")
        with open("test_set.json") as email_file:
            new_emails = json.load(email_file)
        random.shuffle(new_emails["dataset"])
        with open("test300_mails.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'test300_mails.json', True)
        difference = abs(newAccuracy - self.testbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)
    
    def test_permutate_words_train(self):
        print("\nchangement de l’ordre des mots dans le train dataset\n")
        with open("train_set.json") as email_file:
            new_emails = json.load(email_file)
        for e_mail in new_emails["dataset"]:
            subject = e_mail["mail"]["Subject"]
            body = e_mail["mail"]["Body"]
            s = subject.split(" ")
            b = body.split(" ")
            random.shuffle(s)
            random.shuffle(b)
            sub = " ".join(s)
            bod = " ".join(b)
            e_mail["mail"]["Subject"] = sub
            e_mail["mail"]["Body"] = bod
        with open("train700_words.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'train700_words.json', False)
        difference = abs(newAccuracy - self.trainbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)

    def test_permutate_words_test(self):
        print("\nchangement de l’ordre des mots dans le test dataset\n")
        with open("test_set.json") as email_file:
            new_emails = json.load(email_file)
        for e_mail in new_emails["dataset"]:
            subject = e_mail["mail"]["Subject"]
            body = e_mail["mail"]["Body"]
            s = subject.split(" ")
            b = body.split(" ")
            random.shuffle(s)
            random.shuffle(b)
            sub = " ".join(s)
            bod = " ".join(b)
            e_mail["mail"]["Subject"] = sub
            e_mail["mail"]["Body"] = bod
        with open("test300_words.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'test300_words.json', True)
        difference = abs(newAccuracy - self.testbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)


    def test_double_email_test(self):
         print("\najout des memes e-mails dans le test dataset\n")
         with open("test_set.json") as email_file:
             new_emails = json.load(email_file)
        
         for k, v in new_emails.items():
            new_emails[k].extend(v)
            
         with open("test300x2.json", "w") as outfile:
             json.dump(new_emails, outfile)
         newAccuracy = self.evaluate('vocabulary.json', 'test300x2.json', False)
         difference = abs(newAccuracy - self.testbaseAccuracy)
         print("difference: ", difference)
         print("\n")
         self.assertLessEqual(difference, 0.03)

    def test_double_email_train(self):
        print("\najout des memes e-mails dans le train dataset\n")
        with open("train_set.json") as email_file:
            new_emails = json.load(email_file)
        
        for k, v in new_emails.items():
            new_emails[k].extend(v)
            
        with open("train700x2.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'train700x2.json', True)
        difference = abs(newAccuracy - self.trainbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)
    
    def get_all_words(self):
        with open("words.txt", "r") as file:
            allWords = file.read()
            allWords = allWords.replace('[\'','')
            allWords = allWords.replace('\']','')
            allWords = allWords.replace('\n','')
            allWords = allWords.split("', '")
        return allWords

    def test_noise_train(self):
        print("\najout du ”bruit” dans le ”train dataset”\n")
        with open("train_set.json") as email_file:
            new_emails = json.load(email_file)
        words = self.get_all_words()
        for e_mail in new_emails["dataset"]:
            new_email = e_mail["mail"]
            body = new_email["Body"]
            if(len(body)>10):
                nbAjoutes=round(len(body)/10)
                for i in range (0,nbAjoutes):
                    body += random.choice(words)
                    body += " "
            e_mail["Body"] = body
        with open("train700_noise.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'train700_noise.json', True)
        difference = abs(newAccuracy - self.trainbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)
        
        
    def test_noise_test(self):
        print("\najout du ”bruit” dans le ”test dataset”\n")
        with open("test_set.json") as email_file:
            new_emails = json.load(email_file)
        words = self.get_all_words()
        for e_mail in new_emails["dataset"]:
            new_email = e_mail["mail"]
            body = new_email["Body"]
            if(len(body)>10):
                nbAjoutes=round(len(body)/10)
                for i in range (0,nbAjoutes):
                    body += random.choice(words)
                    body += " "
            e_mail["Body"] = body
        with open("test300_noise.json", "w") as outfile:
            json.dump(new_emails, outfile)
        newAccuracy = self.evaluate('vocabulary.json', 'test300_noise.json', False)
        difference = abs(newAccuracy - self.testbaseAccuracy)
        print("difference: ", difference)
        print("\n")
        self.assertLessEqual(difference, 0.03)

    