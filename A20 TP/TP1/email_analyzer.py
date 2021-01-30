import json
from text_cleaner import TextCleaning
from vocabulary_creator import VocabularyCreator


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.words = VocabularyCreator()

    def is_spam(self, subject_orig, body_orig):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''

        pSpamSubject, pHamSubject = self.subject_spam_ham_prob(subject_orig)
        pSpamBody, pHamBody = self.spam_ham_body_prob(body_orig)

        #calcul de pSpam et pHam en faisant la moyenne
        pSpam = (pSpamSubject + pSpamBody)/2
        pHam = (pHamSubject + pHamBody)/2

        return pSpam > pHam


    def spam_ham_body_prob(self, body):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        with open(self.vocab) as file:
            vocabulary = json.load(file)

        #nombre de mots spam ou ham / nombre de mots total dans les emails
        pSpam = self.words.count_spam() / self.words.count_emails()
        pHam = self.words.count_ham() / self.words.count_emails()

        pSpamBody = pSpam
        pHamBody = pHam

        #calcul de probabilite de spam ou ham dans le body
        body = self.cleaning.clean_text(body)
        for word in body:
            if word in dict(vocabulary['spam_body']):
                pSpamBody *= dict(vocabulary['spam_body'])[word]
            if word in dict(vocabulary['ham_body']):
                pHamBody *= dict(vocabulary['ham_body'])[word]

        if pSpam == pSpamBody:
            pSpamBody = 0
        elif pHam == pHamBody:
            pHamBody = 0

        return pSpamBody, pHamBody


    def subject_spam_ham_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''

        with open(self.vocab) as file:
            vocabulary = json.load(file)

        #nombre de mots spam ou ham / nombre de mots total dans les emails
        pSpam = self.words.count_spam() / self.words.count_emails()
        pHam = self.words.count_ham() / self.words.count_emails()

        pSpamSubject = pSpam
        pHamSubject = pHam

        #calcul de probabilite de spam ou ham dans le sujet
        subject = self.cleaning.clean_text(subject)
        spam_dict = dict(vocabulary['spam_sub'])
        ham_dict =  dict(vocabulary['ham_sub'])
        for word in subject:
            if word in spam_dict:
                pSpamSubject *= spam_dict[word]
            if word in ham_dict:
                pHamSubject *= ham_dict[word]

        if pSpam == pSpamSubject:
            pSpamSubject = 0
        elif pHam == pHamSubject:
            pHamSubject = 0

        return pSpamSubject, pHamSubject

