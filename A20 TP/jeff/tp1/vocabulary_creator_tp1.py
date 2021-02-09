import json
import os
from text_cleaner_tp1 import TextCleaning


class VocabularyCreatorTP1:
    """Class for creating vocabulary of spam and non-spam messages"""

    def __init__(self):
        self.train_set = "train700_noise.json"
        self.cleaning = TextCleaning()
        self.vocabulary = "vocabulary_train700_noise.json"

    def load_dict(self):
        with open(self.train_set) as json_data:
            data_dict = json.load(json_data)
        return data_dict

    def write_data_to_vocab_file(self, vocab):
        try:
            with open(self.vocabulary, "w") as outfile:
                json.dump(vocab, outfile)
                print("Vocabulary created...")
                return True
        except:
            return False

    def clean_text(self, text):
        return self.cleaning.clean_text(text)

    def total_words_spam_ham_section(self, file, section):
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

        with open(file) as f:
            input_file = json.load(f)

        for email in input_file["dataset"]:
            individual_email = email["mail"]
            spam_bool = individual_email["Spam"]
            clean_subject = self.cleaning.clean_text((individual_email[section]))
        
            if spam_bool == "true": spam_section_words += clean_subject
            else: ham_section_words += clean_subject
        
        return len(spam_section_words), len(ham_section_words), spam_section_words, ham_section_words

    def probability_email_type_section_words(self, file, section, email_type):
        '''
        Description: fonction pour calculer la probabilite de chaque mot
        d'une certaine section du courriel (subject ou body) d'un certain 
        type de courriel (spam ou ham). En d'autres mots, cette fonction 
        a pour populer les quatre types de vocabulaire (spam_sub, ham_sub, ...) 
        dans vocabullary.json
        Sortie: dictionnaire de mots
        '''

        word_probability_dict = {}

        email_type_section_information = self.total_words_spam_ham_section(file, section)

        if email_type == "Spam":
            total_words_email_type_section = email_type_section_information[0]
            list_words_email_type_section = email_type_section_information[2]
        else:
            total_words_email_type_section = email_type_section_information[1]
            list_words_email_type_section = email_type_section_information[3]

        for word in list_words_email_type_section:
            same_word_counter = sum(word == analyzed_word for analyzed_word in list_words_email_type_section)
            word_probability = same_word_counter/total_words_email_type_section
            word_probability_dict[word] = word_probability

        return word_probability_dict

    def create_vocab(self):
        '''
        Description: fonction pour creer le vocabulaire des mots presents
        dans les e-mails spam et ham et le sauvegarder dans le fichier
        vocabulary.json selon le format specifie dans la description de lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        try:
            vocab_dict = {}

            with open(self.vocabulary, "w") as output_file:
                vocab_dict["spam_sub"] = self.probability_email_type_section_words(self.train_set, "Subject", "Spam")
                vocab_dict["ham_sub"] = self.probability_email_type_section_words(self.train_set, "Subject", "Ham")
                vocab_dict["spam_body"] = self.probability_email_type_section_words(self.train_set, "Body", "Spam",)
                vocab_dict["ham_body"] = self.probability_email_type_section_words(self.train_set, "Body", "Ham",)
                json.dump(vocab_dict, output_file, indent=4)

            return True

        except FileNotFoundError as e:
            print("Error!", e.__class__, "occurred.")
            print("File", e.filename, "was not found")
            return False
