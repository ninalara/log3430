import json
from text_cleaner_tp1 import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self, vocabulary):
        self.vocab = vocabulary
        self.cleaning = TextCleaning()

    def clean_text(self, text): # pragma: no cover
        return self.cleaning.clean_text(text)

    def load_vocab(self): # pragma: no cover
        with open(self.vocab) as json_data:
            vocab = json.load(json_data)
        return vocab

    def is_spam(self, subject_orig, body_orig):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham,
        donnee le sujet et le texte d'email.
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''

        prob_message_subject = self.subject_spam_ham_prob(subject_orig)
        prob_message_body = self.body_spam_ham_prob(body_orig)

        # equation 7 de l'enonce
        prob_message_spam = (2/10 * prob_message_subject[0]) + (8/10 * prob_message_body[0])
        prob_message_ham = (4/10 * prob_message_subject[1]) + (6/10 * prob_message_body[1])

        #equation 3 de l'enonce
        max_prob = max(prob_message_spam, prob_message_ham)

        return True if max_prob == prob_message_spam else False

    def total_emails(self, file):
        '''
        Description: fonction qui calcule le nombre de courriel
        dans un fichier quelconque.
        Sortie: int; il s'agit du nombre total de messages
        '''

        with open(file) as f:
            input_file = json.load(f)

        email = input_file["dataset"]
        total = len(email)
        return total

    def probability_email_type(self, file):
        '''
        Description: fonction qui calcule la probabilite
        qu'un message soit spam ou ham dans un fichier
        Sortie: int, int: P(spam), P(ham)
        '''

        spam_counter = 0
        ham_counter = 0
        with open(file) as f:
            input_file = json.load(f)

        for email in input_file["dataset"]:
            individual_email = email["mail"]
            spam_bool = individual_email["Spam"]

            if spam_bool == "true":
                spam_counter += 1
            else:
                ham_counter += 1

        total = self.total_emails(file)

        # equation 5: P(spam) = nb de messages spam/nb total de messages
        return spam_counter/total, ham_counter/total

    def body_spam_ham_prob(self, body):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''

        body_spam_prob = 1
        body_ham_prob = 1
        probability_spam_ham = self.probability_email_type('train-emails.json')

        prob_spam = probability_spam_ham[0]
        prob_ham = probability_spam_ham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        clean_body = self.cleaning.clean_text(body)

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

    def subject_spam_ham_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''

        sub_spam_prob = 1
        sub_ham_prob = 1

        probability_spam_ham = self.probability_email_type('train-emails.json')

        prob_spam = probability_spam_ham[0]
        prob_ham = probability_spam_ham[1]

        with open(self.vocab) as f:
            input_file = json.load(f)

        clean_sub = self.cleaning.clean_text(subject)
        num_words_spam_sub = len(input_file["spam_sub"])
        num_words_ham_sub = len(input_file["ham_sub"])

        for subject_word in clean_sub:
            if subject_word in input_file["spam_sub"]:
                sub_spam_prob *= input_file["spam_sub"][subject_word]
            elif subject_word in input_file["spam_body"] or subject_word in input_file["ham_sub"] or subject_word in input_file["spam_sub"]:
                sub_spam_prob *= 1 / (num_words_spam_sub + 1)

            if subject_word in input_file["ham_sub"]:
                sub_ham_prob *= input_file["ham_sub"][subject_word]
            elif subject_word in input_file["spam_body"] or subject_word in input_file["ham_body"] or subject_word in input_file["spam_sub"]:
                sub_ham_prob *= 1 / (num_words_ham_sub + 1)
            '''
            for word in input_file["spam_sub"]:
                if subject_word == word:
                    sub_spam_prob *= input_file["spam_sub"][word]
            for word in input_file["ham_sub"]:
                if subject_word == word:
                    sub_ham_prob *= input_file["ham_sub"][word]
            '''

        return prob_spam * sub_spam_prob, prob_ham * sub_ham_prob
