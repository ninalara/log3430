import json
import os
from text_cleaner import TextCleaning


class VocabularyCreator:
    """Class for creating vocabulary of spam and non-spam messages"""

    def __init__(self):
        self.train_set = "800-mails.json"
        self.cleaning = TextCleaning()
        self.vocabulary = "vocabulary.json"

    def create_vocab(self):
        '''
        Description: fonction pour creer le vocabulaire des mots presents
        dans les e-mails spam et ham et le sauvegarder dans le fichier
        vocabulary.json selon le format specifie dans la description de lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        emails = self.load_dict()

        spamSubjects = []
        hamSubjects = []
        spamBodies = []
        hamBodies = []
        vocabulary = {
            "spam_sub": {},
            "ham_sub": {},
            "spam_body": {},
            "ham_body": {}
        }

        # ajout des sujets et des corps des emails de 800-mails.json dans le tableau respectif
        for email in emails["dataset"]:
            if email["mail"]["Spam"] == "true":
                spamSubjects.extend(self.clean_text(email["mail"]["Subject"]))
                spamBodies.extend(self.clean_text(email["mail"]["Body"]))
            else:
                hamSubjects.extend(self.clean_text(email["mail"]["Subject"]))
                hamBodies.extend(self.clean_text(email["mail"]["Body"]))

        spam_sub = list(dict.fromkeys(spamSubjects))
        ham_sub = list(dict.fromkeys(hamSubjects))
        spam_body = list(dict.fromkeys(spamBodies))
        ham_body = list(dict.fromkeys(hamBodies))

        # calcul des probabilites spam et ham pour chaque mots
        for word in spam_sub:
            vocabulary["spam_sub"][word] = spamSubjects.count(word) / len(spamSubjects)
        for word in ham_sub:
            vocabulary["ham_sub"][word] = hamSubjects.count(word) / len(hamSubjects)
        for word in spam_body:
            vocabulary["spam_body"][word] = spamBodies.count(word) / len(spamBodies)
        for word in ham_body:
            vocabulary["ham_body"][word] = hamBodies.count(word) / len(hamBodies)

        self.write_data_to_vocab_file(vocabulary)
        return vocabulary

    # fonction qui retourne le nombre de courriel spam
    def count_spam(self):

        emails = self.load_dict()

        nSpams = 0
        for email in emails["dataset"]:
            if email["mail"]["Spam"] == "true":
                nSpams += 1
        return nSpams

    # fonction qui retourne le nombre de courriel
    def count_emails(self):
        emails = self.load_dict()

        return len(emails["dataset"])

    # fonction qui retourne le nombre de courriel ham
    def count_ham(self):
        nHams = self.count_emails() - self.count_spam()
        return nHams

    def load_dict(self):  # pragma: no cover
        with open(self.train_set) as json_data:
            data_dict = json.load(json_data)
        return data_dict

    def write_data_to_vocab_file(self, vocab):  # pragma: no cover
        try:
            with open(self.vocabulary, 'w') as outfile:
                json.dump(vocab, outfile)
                print('vocabulary created......')
                return True
        except:
            return False

    def clean_text(self, text):  # pragma: no cover
        return self.cleaning.clean_text(text)
