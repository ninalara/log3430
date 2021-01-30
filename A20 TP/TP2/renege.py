import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer
from datetime import date
import time

class RENEGE:
    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "800-mails.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def calculate_user_trust(self, user_id):
        #extracting json data
        date_of_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        date_of_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")
        n_ham = self.crud.get_user_data(user_id, "HamN")
        n_spam = self.crud.get_user_data(user_id, "SpamN")
        groups = self.crud.get_user_data(user_id, "Groups")

        #calculate the sum of trust values of all groups
        sum_trust = 0
        for group in groups :
            group_id = self.crud.get_group_id(group)
            sum_trust += self.crud.get_group_data(group_id, 'Trust')

        #now that we have all the needed vars, calculate trust1, trust2 and trust
        trust1 = (date_of_last_seen_message * n_ham) / (date_of_first_seen_message * (n_ham + n_spam))
        trust2 = sum_trust / len(groups)

        trust = (trust1 + trust2) / 2

        if trust2 < 50:
            trust = trust2
        if trust1 > 100:
            trust = 100

        #before returning a value, check if trust is between 0 and 100
        if trust < 0:
            trust = 0
        elif trust > 100:
            trust = 100
            
        return trust


    def classify_emails(self):
        '''
        fonction deja implemente
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            self.process_email(self.get_email())
            return True
        except Exception as e:
            raise Exception
            return False

    def process_email(self, new_emails):
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionare. Elle gere l'ajout des nouveux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        print(type(new_emails))
        emails = new_emails["dataset"]
        for email in emails:
            email_adr = email['mail']['From']
            date = email['mail']['Date']
            spam = email['mail']['Spam']
            spam = spam == 'true' and True or False

            if self.crud.get_user_id(email_adr):
                self.update_user_info(email_adr, date, spam)
            else:
                self.add_user_info(email_adr, date)

        return True

    def update_user_info(self, new_user_email, new_user_date, new_email_spam):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        numero de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        users_dict = self.crud.read_users_file()

        for key in users_dict:
            user = users_dict.get(key)
            if user.get("name") == new_user_email:
                self.crud.update_users(key, 'Date_of_first_seen_message', new_user_date)

                if new_email_spam:
                    spamN = user.get('SpamN')
                    spamN += 1
                    trust = user.get('Trust')
                    if trust > 0:
                        trust -= 1
                    self.crud.update_users(key, 'SpamN', spamN)
                    self.crud.update_users(key, 'Trust', trust)
                else:
                    hamN = user.get('HamN')
                    hamN += 1
                    trust = user.get('Trust')
                    if trust < 100:
                        trust += 1
                    self.crud.update_users(key, 'HamN', hamN)
                    self.crud.update_users(key, 'HamN', trust)
                break

        return True

    def add_user_info(self, user_email, user_date):
        self.crud.add_new_user(user_email, user_date)

    def update_group_info(self, user_group_list):
        '''
        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisater est present (trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        groups = self.crud.read_groups_file()

        for group in groups:
            if group['List_of_members'] == user_group_list:
                group['Trust'] = self.crud.get_user_data(user_group_list[1], 'Trust')
                return True

        return False

    def get_user_email_list(self):
        '''
        Description: fonction pour creer le liste des e-mails (noms) 
        des utilisateurs uniques.
        Sortie: liste des uniques e-mails des utilisateurs
        '''
        emails = self.get_email()
        list_of_email_addresses = []
        for mail in emails['dataset']:
            list_of_email_addresses.append((mail['mail']['From']))

        return list_of_email_addresses

    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''

        with open(self.email_file) as file:
            emails = json.load(file)

        return emails
