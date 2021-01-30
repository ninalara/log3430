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
        try:
            with open(self.train_set, "r") as read_file:
                emails = json.load(read_file)
        except:
            print("ERROR IN READING FILE")
            raise Exception

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

        #ajout des sujets et des corps des emails de 800-mails.json dans le tableau respectif
        for email in emails["dataset"]:
            if email["mail"]["Spam"] == "true":
                spamSubjects.extend(self.cleaning.clean_text(email["mail"]["Subject"]))
                spamBodies.extend(self.cleaning.clean_text(email["mail"]["Body"]))
            else:
                hamSubjects.extend(self.cleaning.clean_text(email["mail"]["Subject"]))
                hamBodies.extend(self.cleaning.clean_text(email["mail"]["Body"]))

        spam_sub = list(dict.fromkeys(spamSubjects))
        ham_sub = list(dict.fromkeys(hamSubjects))
        spam_body = list(dict.fromkeys(spamBodies))
        ham_body = list(dict.fromkeys(hamBodies))

            #calcul des probabilites spam et ham pour chaque mots
        for word in spam_sub:
            vocabulary["spam_sub"][word] = spamSubjects.count(word) / len(spamSubjects)
        for word in ham_sub:
            vocabulary["ham_sub"][word] = hamSubjects.count(word) / len(hamSubjects)
        for word in spam_body:
            vocabulary["spam_body"][word] = spamBodies.count(word) / len(spamBodies)
        for word in ham_body:
            vocabulary["ham_body"][word] = hamBodies.count(word) / len(hamBodies)

        try:
            with open(self.vocabulary, "w") as write_file:
                json.dump(vocabulary, write_file, indent = 1)
            return True
        except:
            return False

    #fonction qui retourne le nombre de courriel spam
    def count_spam(self):

        with open(self.train_set) as read_file:
            emails = json.load(read_file)

        nSpams = 0
        for email in emails["dataset"]:
            if email["mail"]["Spam"] == "true":
                nSpams += 1
        return nSpams

    #fonction qui retourne le nombre de courriel   
    def count_emails(self):
        with open(self.train_set) as read_file:
            emails = json.load(read_file)
        
        return len(emails["dataset"])

    #fonction qui retourne le nombre de courriel ham
    def count_ham(self):
        nHams = self.count_spam() - self.count_emails()
        return nHams