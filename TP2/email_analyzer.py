import json
import math

from text_cleaner import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab    = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.voc_data = {}



    def is_spam(self, subject_orig, body_orig, is_log_estimation, is_log_combination, clean_text_mode, k):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        
        if is_log_estimation:
            p_subject = self.log_p_spam_ham_subject(subject_orig, clean_text_mode)
            p_body = self.log_p_spam_ham_body(subject_orig, clean_text_mode)
            p_spam_subject = math.pow(p_subject[0], 10)
            p_spam_body = math.pow(p_body[0], 10)
            p_ham_subject = math.pow(p_subject[1], 10)
            p_ham_body = math.pow(p_body[1], 10)
        else:
            p_subject = self.subject_spam_ham_prob(subject_orig, clean_text_mode)
            p_body = self.body_spam_ham_prob(body_orig, clean_text_mode)
            p_spam_subject = p_subject[0]
            p_spam_body = p_body[0]
            p_ham_subject = p_subject[1]
            p_ham_body = p_body[1]

        if is_log_combination:
            if p_spam_subject > 0:
                if p_spam_body > 0:     #case where pspam_subject and pspam_body are both positive
                    p_spam = k * math.log10(p_spam_subject) + (1 - k) * math.log10(p_spam_body)
                else:                   #case where pspam_subject is positive and pspam_body is negative
                    p_spam = k * math.log10(p_spam_subject) + (1 - k) * p_spam_body
            elif p_spam_body > 0:       #case where pspam_subject is negative and pspam_body is positive
                p_spam = k*p_spam_subject + (1 - k) * math.log10(p_spam_body)
            else:                       #case where pspam_subject and pspam_body are both negative
                p_spam = k * p_spam_subject + (1 - k) * p_spam_body

            if p_ham_subject > 0:
                if p_ham_body > 0:
                    p_ham = k * math.log10(p_ham_subject) + (1 - k) * math.log10(p_ham_body)
                else:
                    p_ham = math.log10(p_ham_subject) + (1 - k) * p_ham_body
            elif p_ham_body <= 0:
                p_ham = k * p_ham_subject + (1 - k) * math.log10(p_ham_body)
            else:
                p_ham = p_ham_subject + (1 - k) * p_ham_body
        else:
            p_spam = k * p_spam_subject + (1 - k) * p_spam_body
            p_ham = k * p_ham_subject + (1 - k) * p_ham_body

        if p_spam > p_ham:
            return True
        
        return False

    # def is_spam(self, subject_orig, body_orig):
    #     '''
    #     Description: fonction pour verifier si e-mail est spam ou ham,
    #     en calculant les probabilites d'etre spam et ham, 
    #     donnee le sujet et le texte d'email. 
    #     Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
    #     '''
    #     # Clean email's subject and body
    #     email_subject = self.clean_text(subject_orig)
    #     email_body    = self.clean_text(body_orig)

    #     # Get the spam/ham probabilities
    #     p_subject_spam, p_subject_ham = self.spam_ham_subject_prob(email_subject)
    #     p_body_spam,    p_body_ham    = self.spam_ham_body_prob(email_body)

    #     # Compute the merged probabilities
    #     p_spam = 0.5 * (p_subject_spam + p_body_spam)
    #     p_ham  = 0.5 * (p_subject_ham  + p_body_ham)      

    #     # Decide is the email is spam or ham
    #     if p_spam > p_ham:
    #         return True 
    #     else:
    #         return False

    def spam_ham_body_prob(self, body):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        p_spam = 1.0
        p_ham  = 1.0

        voc_data = self.load_dict()


        # Walk the text to compute the probability
        for word in body:
            # Check the spam probability
            if word in voc_data["p_body_spam"]:
                p_spam *= voc_data["p_body_spam"][word]
            else:
                p_spam *= 1.0 / (len(voc_data["p_body_spam"]) + 1.0)
            
            # Check the ham probability
            if word in voc_data["p_body_ham"]:
                p_ham *= voc_data["p_body_ham"][word]
            else:
                p_ham *= 1.0 / (len(voc_data["p_body_ham"]) + 1.0)

        p_spam *= 0.5925
        p_ham  *= 0.4075

        return (p_spam, p_ham)

    def spam_ham_subject_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        p_spam = 1.0
        p_ham  = 1.0

        voc_data = self.load_dict()

        # Walk the text to compute the probability
        for word in subject:
            # Check the spam probability
            if word in voc_data["p_sub_spam"]:
                p_spam *= voc_data["p_sub_spam"][word]
            else:
                p_spam *= 1.0 / (len(voc_data["p_sub_spam"]) + 1.0)
            
            # Check the ham probability
            if word in voc_data["p_sub_ham"]:
                p_ham *= voc_data["p_sub_ham"][word]
            else:
                p_ham *= 1.0 / (len(voc_data["p_sub_ham"]) + 1.0)

        p_spam *= 0.5925
        p_ham  *= 0.4075

        return (p_spam, p_ham)

    def body_spam_ham_prob(self, body, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''

        p_spam_body = 1
        p_ham_body = 1
        pspam_pham = self.calculate_pspam_pham('train-emails.json')

        p_spam = pspam_pham[0]
        p_ham = pspam_pham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        # body = self.cleaning.clean_text(body)
        body = self.clean_text(body, clean_text_mode)

        n_spam_words = len(input_file["spam_body"])
        n_ham_words = len(input_file["ham_body"])

        for word in body:
            if word in input_file["spam_body"]:
                p_spam_body *= input_file["spam_body"][word]
            elif word in input_file["ham_body"] or word in input_file["ham_sub"] or word in input_file["spam_sub"]:
                p_spam_body *= 1 / (n_spam_words + 1)

            if word in input_file["ham_body"]:
                p_ham_body *= input_file["ham_body"][word]
            elif word in input_file["spam_body"] or word in input_file["ham_sub"] or word in input_file["spam_sub"]:
                p_ham_body *= 1 / (n_ham_words + 1)
            '''
            for word in input_file["spam_body"]:
                if word == word:
                    p_spam_body *= input_file["spam_body"][word]
            for word in input_file["ham_body"]:
                if word == word:
                    p_ham_body *= input_file["ham_body"][word]
            '''

        return p_spam * p_spam_body, p_ham * p_ham_body

    def log_p_spam_ham_body(self, body, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''

        p_spam_body = 0
        p_ham_body = 0

        pspam_pham = self.calculate_pspam_pham('train-emails.json')

        if pspam_pham[0] > 0:
            p_spam = math.log10(pspam_pham[0])
        else:
            p_spam = pspam_pham[0]

        if pspam_pham[1] > 0:
            p_ham = math.log10(pspam_pham[1])
        else:
            p_ham = pspam_pham[1]

        with open(self.vocab) as inputfile:
            input_file = json.load(inputfile)

        body = self.clean_text(body, clean_text_mode)

        n_spam_words = len(input_file["spam_body"])
        n_ham_words = len(input_file["ham_body"])

        for word in body:
            if word in input_file["spam_body"]:
                if input_file["spam_body"][word] > 0:
                    p_spam_body += math.log10(input_file["spam_body"][word])
                else:
                    p_spam_body += input_file["spam_body"][word]

            elif word in input_file["spam_sub"] or word in input_file["spam_body"] or word in input_file["ham_sub"]:
                p_spam_body += math.log10(1 / (n_spam_words + 1))

            if word in input_file["ham_body"]:
                if input_file["ham_body"][word] > 0:
                    p_ham_body += math.log10(input_file["ham_body"][word])
                else:
                    p_ham_body += input_file["ham_body"][word]

            elif word in input_file["spam_sub"] or word in input_file["spam_body"] or word in input_file["ham_body"]:
                p_ham_body += math.log10(1 / (n_spam_words + 1))

        return p_spam + p_spam_body, p_ham + p_ham_body

    def subject_spam_ham_prob(self, subject, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''

        p_spam_subject = 1
        p_ham_subject = 1

        pspam_pham = self.calculate_pspam_pham('train-emails.json')

        p_spam = pspam_pham[0]
        p_ham = pspam_pham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        # body = self.cleaning.clean_text(body)
        clean_sub = self.clean_text(subject, clean_text_mode)

        n_spam_words = len(input_file["spam_sub"])
        n_ham_words = len(input_file["ham_sub"])

        for word in clean_sub:
            if word in input_file["spam_sub"]:
                p_spam_subject *= input_file["spam_sub"][word]
            elif word in input_file["spam_body"] or word in input_file["ham_sub"] or word in input_file["spam_sub"]:
                p_spam_subject *= 1 / (n_spam_words + 1)

            if word in input_file["ham_sub"]:
                p_ham_subject *= input_file["ham_sub"][word]
            elif word in input_file["spam_body"] or word in input_file["ham_body"] or word in input_file["spam_sub"]:
                p_ham_subject *= 1 / (n_ham_words + 1)
            '''
            for word in input_file["spam_sub"]:
                if word == word:
                    p_spam_subject *= input_file["spam_sub"][word]
            for word in input_file["ham_sub"]:
                if word == word:
                    p_ham_subject *= input_file["ham_sub"][word]
            '''

        return p_spam * p_spam_subject, p_ham * p_ham_subject


    def log_p_spam_ham_subject(self, subject, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''

        p_spam_subject = 0
        p_ham_subject = 0

        pspam_pham = self.calculate_pspam_pham('train-set.json')

        if pspam_pham[0] > 0:
            p_spam = math.log10(pspam_pham[0])
        else:
            p_spam = pspam_pham[0]
        
        if pspam_pham[1] > 0:    
            p_ham = math.log10(pspam_pham[1])
        else:
            p_ham = pspam_pham[1]

        with open(self.vocab) as inputfile:
            input_file = json.load(inputfile)

        subject = self.clean_text(subject, clean_text_mode)

        n_spam_words = len(input_file["spam_sub"])
        n_spam_words = len(input_file["ham_sub"])

        for word in subject:
            if word in input_file["spam_sub"]:
                if input_file["spam_sub"][word] > 0:
                    p_spam_subject += math.log10(input_file["spam_sub"][word])
                else:
                    p_spam_subject += (input_file["spam_sub"][word])

            elif word in input_file["spam_sub"] or word in input_file["spam_body"] or word in input_file["ham_sub"]:
                p_spam_subject += math.log10(1 / (n_spam_words + 1))

            if word in input_file["ham_sub"]:
                if input_file["ham_sub"][word] > 0:
                    p_ham_subject += math.log10(input_file["ham_sub"][word])
                else:
                    p_ham_subject += input_file["ham_sub"][word]

            elif word in input_file["spam_sub"] or word in input_file["spam_body"] or word in input_file["ham_body"]:
                p_ham_subject += math.log10(1 / (n_spam_words + 1))
        
        p_spam = p_spam + p_spam_subject
        p_ham = p_ham + p_ham_subject

        return p_spam, p_ham
    
    def calculate_pspam_pham(self, file):
    '''
        Description: fonction qui calcule la probabilite
        qu'un message soit spam ou ham dans un fichier
        Sortie: int, int: P(spam), P(ham)
        '''
        n_spam, n_ham = 0

        with open(file) as data:
            input_file = json.load(data)

        for email in input_file["dataset"]:
            mail = email["mail"]
            is_spam = mail["Spam"]

            if is_spam == "true":
                n_spam += 1
            else:
                n_ham += 1

        # calculer le nombre d'emails
        n_emails = len(input_file["dataset"])

        return n_spam/n_emails, n_ham/n_emails

    def clean_text(self, text, mode):
        return self.cleaning.clean_text(text, mode)

    def load_dict(self):
        # Open vocabulary 
        with open(self.vocab) as json_data:
            vocabu = json.load(json_data)
        
        return vocabu