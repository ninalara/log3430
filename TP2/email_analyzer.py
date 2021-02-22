import json
import math

from text_cleaner import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab    = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.voc_data = {}

    def is_spam(self, subject_orig, body_orig, is_log_estimation, is_log_combination, clean_text_mode):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        
        if is_log_estimation:
            prob_message_subject = self.subject_spam_ham_prob_log(subject_orig, clean_text_mode)
            prob_message_body = self.body_spam_ham_prob_log(subject_orig, clean_text_mode)
            subject_spam = math.pow(prob_message_subject[0], 10)
            body_spam = math.pow(prob_message_body[0], 10)
            subject_ham = math.pow(prob_message_subject[1], 10)
            body_ham = math.pow(prob_message_body[1], 10)
        else:
            prob_message_subject = self.subject_spam_ham_prob(subject_orig, clean_text_mode)
            prob_message_body = self.body_spam_ham_prob(body_orig, clean_text_mode)
            subject_spam = prob_message_subject[0]
            body_spam = prob_message_body[0]
            subject_ham = prob_message_subject[1]
            body_ham = prob_message_body[1]

        if is_log_combination:
            # il faut traiter les cas ou x dans log(x) est egal a 0 ou tres petit
            if not subject_spam <= 0:
                if not body_spam <= 0:
                    prob_message_spam = k*math.log10(subject_spam) + (1-k)*math.log10(body_spam)
                else:
                    prob_message_spam = k * math.log10(subject_spam) + (1 - k) * body_spam
            elif not body_spam <= 0:
                prob_message_spam = k*subject_spam + (1 - k) * math.log10(body_spam)
            else:
                prob_message_spam = k * subject_spam + (1 - k) * body_spam

            if not subject_ham <= 0:
                if not body_ham <= 0:
                    prob_message_ham = k * math.log10(subject_ham) + (1 - k) * math.log10(body_ham)
                else:
                    prob_message_ham = math.log10(subject_ham) + (1 - k) * body_ham
            elif body_ham <= 0:
                prob_message_ham = k * subject_ham + (1 - k) * math.log10(body_ham)
            else:
                prob_message_ham = subject_ham + (1 - k) * body_ham
        else:
            prob_message_spam = k*subject_spam + (1-k)*body_spam
            prob_message_ham = k*subject_ham + (1-k)*body_ham

        max_prob = max(prob_message_spam, prob_message_ham)

        return True if max_prob == prob_message_spam else False

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

        body_spam_prob = 1
        body_ham_prob = 1
        probability_spam_ham = self.calculate_pspam_pham('train-emails.json')

        prob_spam = probability_spam_ham[0]
        prob_ham = probability_spam_ham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        # clean_body = self.cleaning.clean_text(body)
        clean_body = self.clean_text(body, clean_text_mode)

        num_words_spam_body = len(input_file["spam_body"])
        num_words_ham_body = len(input_file["ham_body"])

        for body_word in clean_body:
            if body_word in input_file["spam_body"]:
                body_spam_prob *= input_file["spam_body"][body_word]
            elif body_word in input_file["ham_body"] or body_word in input_file["ham_sub"] or body_word in input_file["spam_sub"]:
                body_spam_prob *= 1 / (num_words_spam_body + 1)

            if body_word in input_file["ham_body"]:
                body_ham_prob *= input_file["ham_body"][body_word]
            elif body_word in input_file["spam_body"] or body_word in input_file["ham_sub"] or body_word in input_file["spam_sub"]:
                body_ham_prob *= 1 / (num_words_ham_body + 1)
            '''
            for word in input_file["spam_body"]:
                if body_word == word:
                    body_spam_prob *= input_file["spam_body"][word]
            for word in input_file["ham_body"]:
                if body_word == word:
                    body_ham_prob *= input_file["ham_body"][word]
            '''

        return prob_spam * body_spam_prob, prob_ham * body_ham_prob

    def body_spam_ham_prob_log(self, body, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''

        body_spam_prob = 0
        body_ham_prob = 0
        probability_spam_ham = self.calculate_pspam_pham('train-emails.json')

        if probability_spam_ham[0] > 0:
            prob_spam = math.log10(probability_spam_ham[0])
        else:
            prob_spam = probability_spam_ham[0]

        if probability_spam_ham[1] > 0:
            prob_ham = math.log10(probability_spam_ham[1])
        else:
            prob_ham = probability_spam_ham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        # clean_body = self.cleaning.clean_text(body)
        clean_body = self.clean_text(body, clean_text_mode)

        num_words_spam_body = len(input_file["spam_body"])
        num_words_ham_body = len(input_file["ham_body"])

        for body_word in clean_body:
            if body_word in input_file["spam_body"]:
                if input_file["spam_body"][body_word] > 0:
                    # pas certaine de comment modifier cette partie, pour l'instant += math.log10()()
                    body_spam_prob += math.log10(input_file["spam_body"][body_word])
                else:
                    body_spam_prob += input_file["spam_body"][body_word]

            elif body_word in input_file["ham_body"] or body_word in input_file["ham_sub"] or body_word in input_file["spam_sub"]:
                body_spam_prob += math.log10(1 / (num_words_spam_body + 1))

            if body_word in input_file["ham_body"]:
                if input_file["ham_body"][body_word] > 0:
                    body_ham_prob += math.log10(input_file["ham_body"][body_word])
                else:
                    body_ham_prob += input_file["ham_body"][body_word]

            elif body_word in input_file["spam_body"] or body_word in input_file["ham_sub"] or body_word in input_file["spam_sub"]:
                #pareil
                body_ham_prob += math.log10(1 / (num_words_ham_body + 1))
            '''
            for word in input_file["spam_body"]:
                if body_word == word:
                    body_spam_prob *= input_file["spam_body"][word]
            for word in input_file["ham_body"]:
                if body_word == word:
                    body_ham_prob *= input_file["ham_body"][word]
            '''

        return prob_spam + body_spam_prob, prob_ham + body_ham_prob

    def subject_spam_ham_prob(self, subject, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''

        subject_spam_prob = 1
        subject_ham_prob = 1

        probability_spam_ham = self.calculate_pspam_pham('train-emails.json')

        prob_spam = probability_spam_ham[0]
        prob_ham = probability_spam_ham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        # clean_body = self.cleaning.clean_text(body)
        clean_sub = self.clean_text(subject, clean_text_mode)

        n_words_spam_sub = len(input_file["spam_sub"])
        n_words_ham_sub = len(input_file["ham_sub"])

        for word in clean_sub:
            if word in input_file["spam_sub"]:
                subject_spam_prob *= input_file["spam_sub"][word]
            elif word in input_file["spam_body"] or word in input_file["ham_sub"] or word in input_file["spam_sub"]:
                subject_spam_prob *= 1 / (n_words_spam_sub + 1)

            if word in input_file["ham_sub"]:
                subject_ham_prob *= input_file["ham_sub"][word]
            elif word in input_file["spam_body"] or word in input_file["ham_body"] or word in input_file["spam_sub"]:
                subject_ham_prob *= 1 / (n_words_ham_sub + 1)
            '''
            for word in input_file["spam_sub"]:
                if word == word:
                    subject_spam_prob *= input_file["spam_sub"][word]
            for word in input_file["ham_sub"]:
                if word == word:
                    subject_ham_prob *= input_file["ham_sub"][word]
            '''

        return prob_spam * subject_spam_prob, prob_ham * subject_ham_prob


    def subject_spam_ham_prob_log(self, subject, clean_text_mode):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''

        subject_spam_prob = 0
        subject_ham_prob = 0

        pspam_pham = self.calculate_pspam_pham('train-set.json')

        p_spam = math.log10(pspam_pham[0])
        p_ham = math.log10(pspam_pham[1])

        with open(self.vocab) as f:
            input_file = json.load(f)

        cleaned_sub = self.clean_text(subject, clean_text_mode)

        n_words_spam_sub = len(input_file["spam_sub"])
        n_words_ham_sub = len(input_file["ham_sub"])

        for word in cleaned_sub:
            if word in input_file["spam_sub"]:
                if input_file["spam_sub"][word] > 0:
                    subject_spam_prob += math.log10(input_file["spam_sub"][word])
                else:
                    subject_spam_prob += (input_file["spam_sub"][word])

            elif word in input_file["spam_body"] or word in input_file["ham_sub"] or word in input_file["spam_sub"]:
                subject_spam_prob += math.log10(1 / (n_words_spam_sub + 1))

            if word in input_file["ham_sub"]:
                if input_file["ham_sub"][word] > 0:
                    subject_ham_prob += math.log10(input_file["ham_sub"][word])
                else:
                    subject_ham_prob += input_file["ham_sub"][word]

            elif word in input_file["spam_body"] or word in input_file["ham_body"] or word in input_file["spam_sub"]:
                subject_ham_prob += math.log10(1 / (n_words_ham_sub + 1))

        return p_spam + subject_spam_prob, p_ham + subject_ham_prob
    
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