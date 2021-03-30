
import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer


class RENEGE:


    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "train_set.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def calculate_user_trust(self, user_id):
        #json data
        date_of_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        date_of_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")
        n_ham = self.crud.get_user_data(user_id, "HamN")
        n_spam = self.crud.get_user_data(user_id, "SpamN")
        user_name = self.crud.get_user_data(user_id, "name")
        groups = self.crud.read_groups_file()

        sum_trust = 0
        n_groups = 0
        
        # find nb of groups to which user belongs
        for group in groups.values() :
            if user_name in group["List_of_members"]:
                sum_trust += group["Trust"]
                n_groups += 1

        trust1 = (date_of_last_seen_message * n_ham) / (date_of_first_seen_message * (n_ham + n_spam))
        trust2 = 0
        # to avoid 'division by zero' error 
        if n_groups != 0:
            trust2 = sum_trust / n_groups
        
        trust = (trust1 + trust2) / 2

        if trust2 < 50:
            trust = trust2
        if trust1 > 100:
            trust = 100

        if trust > 100:
            trust = 100
        elif trust < 0:
            trust = 0
            
        return trust

    def classify_emails(self, mode):
        '''
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            self.process_email(self.get_email(), mode)
            return True
        except Exception as e:
            print("Error!", e.__class__, "occurred.")
            raise e
            return False


    def process_email(self, new_emails, mode):
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionare. Elle gere l'ajout des nouveux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes. 
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        emails = self.get_email()
        print("Processing emails")
        i = 0
        email_count = len(emails["dataset"])
        # Load emails
        for email in emails["dataset"]:    
            i += 1
            print("\rEmail " + str(i) + "/" + str(email_count), end="")

            data    = email["mail"]
            subject = data["Subject"]
            name    = data["From"]
            date    = data["Date"]            
            body    = data["Body"]
            is_spam = data["Spam"]

            # Get registered data
            user_id = -1
            try:
                user_id = self.crud.get_user_id(name)
            except RuntimeError:
                # Create the user
                if not self.crud.add_new_user(name, date):
                    return False

                user_id = self.crud.get_user_id(name)

            if mode == 1:
                is_spam = self.is_spam1(email)
            elif mode == 2:
                is_spam = self.is_spam2(email)

            # Update user's emails info
            if is_spam == "true":
                if not self.update_user_info(user_id, date, 1, 0):
                    return False
            else:
                if not self.update_user_info(user_id, date, 0, 1):
                    return False
            

            # Update groups data
            groups = self.crud.get_user_data(user_id, "Groups")
            for group_name in groups:
                try:
                    group_id = self.crud.get_group_id(group_name)
                    if not self.update_group_info(group_id, user_id):
                        return False

                except RuntimeError:
                    return False
        
        print("\n")

        return True

    def is_spam1(self, email):

        user_id = self.crud.get_user_id(email["mail"]["From"])
        trust = self.crud.get_user_data(user_id, "Trust")
        first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")

        p = email["mail"]["Spam"] == "true"
        h = (float(last_seen_message - first_seen_message)) / (60 * 60 * 24) > 31
        t1 = trust < 60
        t2 = trust < 70
        t3 = trust > 75

        return (p and ((h and t1) or t2)) or (h and t2 and not t3)

    def is_spam2(self, email):
        user_id = self.crud.get_user_id(email["mail"]["From"])
        trust = self.crud.get_user_data(user_id, "Trust")

        p = email["mail"]["Spam"] == "true"
        t2 = trust < 70
        t3 = trust > 75

        return p or (2 and not t3 and t2)


    def update_user_info(self, user_id, new_user_date, new_email_spam, new_email_ham):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        numero de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        # Update last / first seen date 
        new_date = self.crud.convert_to_unix(new_user_date)
        if new_date > self.crud.get_user_data(user_id, "Date_of_last_seen_message"):
            if not self.crud.update_users(user_id, "Date_of_last_seen_message", new_user_date):
                return False
        elif new_date < self.crud.get_user_data(user_id, "Date_of_first_seen_message"):
            if not self.crud.update_users(user_id, "Date_of_first_seen_message", new_user_date):
                return False

        # Update trust score 
        spam_n = self.crud.get_user_data(user_id, "SpamN") + new_email_spam
        ham_n  = self.crud.get_user_data(user_id, "HamN") + new_email_ham

        trust_lvl = 50
        if (spam_n + ham_n) != 0:
            trust_lvl = ham_n / (spam_n + ham_n) * 100
            if trust_lvl > 100:
                trust_lvl = 100

        if not self.crud.update_users(user_id, "SpamN", spam_n):
            return False

        if not self.crud.update_users(user_id, "HamN", ham_n):
            return False

        return self.crud.update_users(user_id, "Trust", trust_lvl)

    def update_group_info(self, group_id, user_id):
        '''
        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisater est present (trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''        
        try:
            # Get list of users and update it
            users_list = self.crud.get_groups_data(group_id, "List_of_members")
            user_name  = self.crud.get_user_data(user_id, "name")
            if user_name not in users_list:
                users_list.append(user_name)

            # Get data for trust update
            user_count = len(users_list)
            trust_lvl  = 0      

            # Compute group's trust
            for user in users_list:
                curr_user_id = self.crud.get_user_id(user)
                trust_lvl   += self.crud.get_user_data(curr_user_id, "Trust")

            if(trust_lvl > 100):
                trust_lvl = 100 
            
            # Update the group with the new trust level and the new member list
            if self.crud.update_groups(group_id, "Trust", trust_lvl):     
                return self.crud.update_groups(group_id, 'List_of_members', users_list)

            return False
        except RuntimeError:
            return False


    def get_user_email_list(self):
        '''
        Description: fonction pour creer le liste des e-mails (noms) 
        des utilisateurs uniques.
        Sortie: liste des uniques e-mails des utilisateurs
        '''
        emails = []
        for user in self.crud.users_data:
            emails.append(user["name"])
        return emails

    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''
        with open(self.email_file) as email_file:
            return json.load(email_file)
