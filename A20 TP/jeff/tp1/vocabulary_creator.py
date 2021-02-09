import json
import os
from text_cleaner import TextCleaning


class VocabularyCreator:
    """Class for creating vocabulary of spam and non-spam messages"""

    def __init__(self):
        self.train_set = "1000-mails.json"
        self.cleaning = TextCleaning()
        self.vocabulary = "vocabulary.json"

    def load_dict(self, file): # pragma: no cover
        with open(file) as json_data:
            data_dict = json.load(json_data)
        return data_dict

    def write_data_to_vocab_file(self, vocab): # pragma: no cover
        try:
            with open(self.vocabulary, "w") as outfile:
                json.dump(vocab, outfile)
                print("Vocabulary created...")
                return True
        except:
            return False

    def clean_text(self, text, option):  # pragma: no cover
        return self.cleaning.clean_text(text, option)

    def total_words_spam_ham_section(self, file, section, cleaning_option):
        '''
        Description: fonction pour calculer le nombre de mots dans les
        e-mails spam et ham, et pour recueillir les mots de chaque type 
        de e-mail.
        Sortie: int, int, list, list; les deux premières pour le nombre
        de mots dans chaque type de courriel, les deux dernières retou-
        rnent une liste de mots regroupée pour chaque type.
        '''

        spam_section_words = []
        ham_section_words = []

        input_file = self.load_dict(file)

        for email in input_file["dataset"]:
            individual_email = email["mail"]
            spam_bool = individual_email["Spam"]
            clean_subject = self.cleaning.clean_text((individual_email[section]), cleaning_option)
        
            if spam_bool == "true": spam_section_words += clean_subject
            else: ham_section_words += clean_subject
        
        return len(spam_section_words), len(ham_section_words), spam_section_words, ham_section_words

    def probability_email_type_section_words(self, file, section, email_type, word_frequency, cleaning_option):
        '''
        Description: fonction pour calculer la probabilite de chaque mot
        d'une certaine section du courriel (subject ou body) d'un certain 
        type de courriel (spam ou ham). En d'autres mots, cette fonction 
        a pour populer les quatre types de vocabulaire (spam_sub, ham_sub, ...) 
        dans vocabullary.json
        Sortie: dictionnaire de mots
        '''

        word_probability_dict = {}

        email_type_section_information = self.total_words_spam_ham_section(file, section, cleaning_option)

        if email_type == "Spam":
            total_words_email_type_section = email_type_section_information[0]
            list_words_email_type_section = email_type_section_information[2]
        else:
            total_words_email_type_section = email_type_section_information[1]
            list_words_email_type_section = email_type_section_information[3]

        for word in list_words_email_type_section:
            same_word_counter = sum(word == analyzed_word for analyzed_word in list_words_email_type_section)
            word_probability = same_word_counter/total_words_email_type_section
            if same_word_counter >= word_frequency:
                word_probability_dict[word] = round(word_probability, 4)

        return word_probability_dict

    def create_vocab(self, word_frequency, cleaning_option):
        '''
        Description: fonction pour creer le vocabulaire des mots presents
        dans les e-mails spam et ham et le sauvegarder dans le fichier
        vocabulary.json selon le format specifie dans la description de lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        try:
            if word_frequency < 1 or word_frequency > 4:
                return False

            vocab_dict = {}

            vocab_dict["spam_sub"] = self.probability_email_type_section_words(self.train_set, "Subject", "Spam", word_frequency, cleaning_option)
            vocab_dict["ham_sub"] = self.probability_email_type_section_words(self.train_set, "Subject", "Ham", word_frequency, cleaning_option)
            vocab_dict["spam_body"] = self.probability_email_type_section_words(self.train_set, "Body", "Spam", word_frequency, cleaning_option)
            vocab_dict["ham_body"] = self.probability_email_type_section_words(self.train_set, "Body", "Ham", word_frequency, cleaning_option)

            self.write_data_to_vocab_file(vocab_dict)

            return vocab_dict

        except FileNotFoundError as e:
            print("Error!", e.__class__, "occurred.")
            print("File", e.filename, "was not found")
            return False

