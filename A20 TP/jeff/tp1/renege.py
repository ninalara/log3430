import json
import sys
import time
import datetime
from crud import CRUD
from email_analyzer import EmailAnalyzer


class RENEGE:

    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "1000-mails.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def calculate_user_trust(self, user_id):
        '''
        Description: fonction a implementer pour la deuxieme partie du
        deuxieme travail pratique. Permet de calculer le trust d'un
        utilisateur specifique

        Sortie: int; Retourne la valeur du trust de l'utilisateur
        '''
        # calculation for Trust1
        nb_spam = self.crud.get_user_data(user_id, "SpamN")
        nb_ham = self.crud.get_user_data(user_id, "HamN")

        time_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        time_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")

        if (time_first_seen_message * (nb_ham + nb_spam)) == 0:
            print("trust1 not possible, division by zero")
            return

        trust1 = ((time_last_seen_message * nb_ham)/(time_first_seen_message * (nb_ham + nb_spam)))

        # calculation for Trust2
        group_list = self.crud.read_groups_file()

        # in order to determine if user is part of a group, we need their email
        user_email = self.crud.get_user_data(user_id, "name")

        # number of groups that the user is in
        nb_group = 0
        user_trust_total = 0

        for group in group_list.values():
            if user_email in group["List_of_members"]:
                nb_group += 1
                user_trust_total += group["Trust"]

        trust2 = user_trust_total / nb_group

        # determining user's final trust value
        if trust2 < 50:
            return trust2
        elif trust1 > 100:
            return 100

        final_trust = (trust1 + trust2) / 2

        if final_trust < 0:
            final_trust = 0
        elif final_trust > 100:
            final_trust = 100

        return final_trust

    def classify_emails(self, spam_definition_mode):
        '''
        fonction deja implemente
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            self.process_email(self.get_email(), spam_definition_mode)
            return True
        except Exception as e:
            print("Error!", e.__class__, "occurred.")
            return False

    def process_email(self, new_emails, mode):
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionare. Elle gere l'ajout des nouveux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes. 
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        list_of_email_addresses = self.get_user_email_list()

        for user in list_of_email_addresses:
            # date de defaut est l'epoch linux
            self.crud.add_new_user(user, "1970-01-01")

        self.crud.add_new_group('default', 50, list_of_email_addresses)

        is_spam = ''

        for email in new_emails["dataset"]:
            individual_email = email["mail"]
            email_address = individual_email["From"]       
            date = time.mktime(datetime.datetime.strptime(individual_email["Date"], "%Y-%m-%d").timetuple())

            if mode == 0:
                is_spam = individual_email["Spam"]
            elif mode == 1:
                is_spam = self.is_spam1(email)
            elif mode == 2:
                is_spam = self.is_spam2(email)

            self.update_user_info(email_address, date, is_spam)

        self.update_group_info(list_of_email_addresses, 'default')

    def is_spam1(self, email):
        '''
        Description: fonction qui calcule la probabilité de spam selon l'équation 1 de
        l'énoncé, soit S = P ∗ (H ∗ T1 + T2) + H ∗ T2 ∗ ¬T3
        '''
        user_id = self.crud.get_user_id(email["From"])
        trust = self.crud.get_user_data(user_id, "Trust")
        first = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        last = self.crud.get_user_data(user_id, "Date_of_last_seen_message")

        p = email["Spam"] == "true"
        h = (float(last) - float(first)) / (60 * 60 * 24) > 31
        t1 = trust < 60
        t2 = trust < 70
        t3 = trust > 75

        return (p and ((h and t1) or t2)) or (h and t2 and not t3)

    def is_spam2(self, email):
        '''
        Description: fonction qui calcule la probabilité de spam selon l'équation 2 de
        l'énoncé, soit S = P + ¬T3 ∗ T2
        '''

        user_id = self.crud.get_user_id(email["From"])
        trust = self.crud.get_user_data(user_id, "Trust")

        p = email["Spam"] == "true"
        t2 = trust < 70
        t3 = trust > 75

        return p or (not t3 and t2)

    def update_user_info(self, new_user_email, new_user_date, new_email_spam):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        numero de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        user_id = self.crud.get_user_id(new_user_email)

        date_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        date_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")

        try: 
            if new_user_date < date_first_seen_message:
                self.crud.update_users(user_id, "Date_of_first_seen_message", new_user_date)
            elif new_user_date > date_last_seen_message:
                self.crud.update_users(user_id, "Date_of_last_seen_message", new_user_date)

            # Mise a jour des spamN/hamN et trust des utilisateurs 
            user_spamN = self.crud.get_user_data(user_id, "SpamN")
            user_hamN = self.crud.get_user_data(user_id, "HamN")
            if new_email_spam == "true":
                user_spamN = user_spamN + 1
                self.crud.update_users(user_id, "SpamN", user_spamN)
            else:
                user_hamN = user_hamN + 1
                self.crud.update_users(user_id, "HamN", user_hamN)

            total_msg = user_spamN + user_hamN 
            self.crud.update_users(user_id, "Trust", (user_hamN / total_msg) * 100)
            return True
        except:
            return False

    def update_group_info(self, user_group_list, group_name):
        '''
        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisater est present (trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            trust_sum = 0
            for user in user_group_list:
                user_id = self.crud.get_user_id(user)
                trust_sum += self.crud.get_user_data(user_id, "Trust")

            # Calcul de la nouvelle moyenne de trust des membres
            group_trust = round(trust_sum / len(user_group_list), 0)
            group_id = self.crud.get_group_id(group_name)
            self.crud.update_groups(group_id, "Trust", group_trust)
            return True
        except:
            return False

    def get_user_email_list(self):
        '''
        Description: fonction pour creer le liste des e-mails (noms) 
        des utilisateurs uniques.
        Sortie: liste des uniques e-mails des utilisateurs
        '''
        email_dict = self.get_email()
        existing_email_address = set()
        unique_emails = []

        for email in email_dict["dataset"]:
            individual_email = email["mail"]
            email_address = individual_email["From"]

            if email_address in existing_email_address:
                continue
            
            existing_email_address.add(email_address)
            unique_emails.append(email_address)

        return unique_emails

    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''
        with open(self.email_file) as email_file:
            return json.load(email_file) 

