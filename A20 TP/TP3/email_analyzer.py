import json
import math
from text_cleaner import TextCleaning
from vocabulary_creator import VocabularyCreator


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.words = VocabularyCreator()

    @staticmethod
    def is_spam_function_one(is_msg_spam, user_historic_in_days, user_trust, user_group_trust):
        p = is_msg_spam
        h = user_historic_in_days < 30
        t1 = user_trust < 60
        t2 = user_group_trust < 70
        t3 = user_trust > 75
        result = p and (h and t1 or t2) or h and t2 and not t3
        return result

    @staticmethod
    def is_spam_function_two(is_msg_spam, user_trust, user_group_trust):
        p = is_msg_spam
        t2 = user_group_trust < 70
        t3 = user_trust > 75
        result = p or not t3 and t2
        return result

    def is_spam(self, subject_orig, body_orig, isLogEstimation, isLogCombination, k):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        # nombre de mots spam ou ham / nombre de mots total dans les emails
        pSpam = self.calculate_spam_divided_by_email()
        pHam = self.calculate_ham_divided_by_email()

        if (isLogEstimation):
            pSpamSubject, pHamSubject = self.subject_spam_ham_log_prob(subject_orig, pSpam, pHam)
            pSpamBody, pHamBody = self.subject_spam_ham_log_prob(body_orig, pSpam, pHam)
            estimationpSpamSubject = math.log10(pSpam) + pSpamSubject
            estimationpHamSubject = math.log10(pHam) + pHamSubject
            estimationpSpamBody = math.log10(pSpam) + pSpamBody
            estimationpHamBody = math.log10(pHam) + pHamBody
        else:
            pSpamSubject, pHamSubject = self.subject_spam_ham_prob(subject_orig)
            pSpamBody, pHamBody = self.spam_ham_body_prob(body_orig)
            estimationpSpamSubject = pSpam * pSpamSubject
            estimationpHamSubject = pHam * pHamSubject
            estimationpSpamBody = pSpam * pSpamBody
            estimationpHamBody = pHam * pHamBody

        if (isLogCombination):
            # s'assurer que l'estimation est strictement plus grand que 0 afin de pouvoir faire le logarithme
            # seul ceux qui sont strictement positif auront appliquer la fonction math.log10
            if (estimationpSpamSubject > 0):
                estimationpSpamSubject = math.log10(estimationpSpamSubject)
            if (estimationpHamSubject > 0):
                estimationpHamSubject = math.log10(estimationpHamSubject)
            if (estimationpSpamBody > 0):
                estimationpSpamBody = math.log10(estimationpSpamBody)
            if (estimationpHamBody > 0):
                estimationpHamBody = math.log10(estimationpHamBody)

        # s'assurer que la valeur de k est entre 0 et 1
        # si elle est plus grand que 1, le rendre en une valeur entre 0 et 1
        if (k > 1):
            k = k / math.pow(10, len(str(k)))
        elif (k < 0):
            k = 0
        # la formule de combinaison de prob est pareil pour les 2 options
        # a l'exception de la valeur des parametres d'estimation qui auront applique le logarithme si approprie
        combinationpSpam = k * estimationpSpamSubject + (1 - k) * estimationpSpamBody
        combinationpHam = k * estimationpHamSubject + (1 - k) * estimationpHamBody

        return combinationpSpam > combinationpHam

    def subject_spam_ham_log_prob(self, subject, pSpam, pHam):
        vocabulary = self.load_dict()

        pSpamSubject = pSpam
        pHamSubject = pHam

        # calcul de probabilite de spam ou ham dans le body
        subject = self.clean_text(subject)
        for word in subject:
            if word in dict(vocabulary['spam_body']):
                pSpamSubject += dict(vocabulary['spam_body'])[word]
            if word in dict(vocabulary['ham_body']):
                pHamSubject += dict(vocabulary['ham_body'])[word]

        # logarithme de pSpamBody et pHamBody
        pHamSubject = math.log10(pHamSubject)
        pSpamSubject = math.log10(pSpamSubject)

        if pSpam == pSpamSubject:
            pSpamBody = 0
        elif pHam == pHamSubject:
            pHamBody = 0

        return pSpamBody, pHamBody

    def spam_ham_body_log_prob(self, body, pSpam, pHam):
        vocabulary = self.load_dict()

        pSpamBody = pSpam
        pHamBody = pHam

        # calcul de probabilite de spam ou ham dans le body
        body = self.clean_text(body)
        for word in body:
            if word in dict(vocabulary['spam_body']):
                pSpamBody += dict(vocabulary['spam_body'])[word]
            if word in dict(vocabulary['ham_body']):
                pHamBody += dict(vocabulary['ham_body'])[word]

        # logarithme de pSpamBody et pHamBody
        pHamBody = math.log10(pHamBody)
        pSpamBody = math.log10(pSpamBody)

        if pSpam == pSpamBody:
            pSpamBody = 0
        elif pHam == pHamBody:
            pHamBody = 0

        return pSpamBody, pHamBody
    
    def spam_ham_body_prob(self, body):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''

        vocabulary = self.load_dict()

        # nombre de mots spam ou ham / nombre de mots total dans les emails
        pSpam = self.calculate_spam_divided_by_email()
        pHam = self.calculate_ham_divided_by_email()

        pSpamBody = pSpam
        pHamBody = pHam

        # calcul de probabilite de spam ou ham dans le body
        body = self.clean_text(body)
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

        vocabulary = self.load_dict()

        # nombre de mots spam ou ham / nombre de mots total dans les emails
        pSpam = self.calculate_spam_divided_by_email()
        pHam = self.calculate_ham_divided_by_email()

        pSpamSubject = pSpam
        pHamSubject = pHam

        # calcul de probabilite de spam ou ham dans le sujet
        subject = self.clean_text(subject)
        spam_dict = dict(vocabulary['spam_sub'])
        ham_dict = dict(vocabulary['ham_sub'])
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

    def calculate_spam_divided_by_email(self):  # pragma: no cover
        return self.words.count_spam() / self.words.count_emails()

    def calculate_ham_divided_by_email(self):  # pragma: no cover
        return self.words.count_ham() / self.words.count_emails()

    def load_dict(self):  # pragma: no cover
        with open(self.vocab) as file:
            vocabulary = json.load(file)

        return vocabulary

    def clean_text(self, text):  # pragma: no cover
        return self.cleaning.clean_text(text, 0)
