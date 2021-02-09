import json
import math
import time
import datetime

class CRUD:
    """
    Classe pour realiser la fonctionalite CRUD.
    """

    def __init__(self, empty_users):
        if not empty_users:
            self.users_file = {
                    "1": {
                        "name": "heebangsyang@outlook.com",
                        "Trust": 50,
                        "SpamN": 0,
                        "HamN": 0,
                        "Date_of_first_seen_message": 1605135873,
                        "Date_of_last_seen_message": 1605135873,
                        "Groups": ["default", "colleagues"],

                    }
                }
        else:
            self.users_file = {}
        self.groups_file = {} 

    ##*************CREATE**************


    def add_new_user(self, user_email, date):
        '''
        Description: fonction pour ajouter un nouvel utilisateur 
        dans le fichier 'users.json', selon le format donné dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        try:
            users = self.read_users_file()
            nbUsers = str(len(users) + 1)
            for x in users:
                if users[x]['name'] == user_email:
                    return False
            default_last_seen = math.trunc(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
            default_first_seen = math.trunc(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))
            user_json = {"name": user_email, "Trust": 50, "SpamN": 0, "HamN": 0,
                         "Date_of_first_seen_message": default_first_seen,
                         "Date_of_last_seen_message": default_last_seen, "Groups": ["default"]}
            data = users
            data[nbUsers] = user_json
            self.modify_users_file(data)

        except:
            print("The file is empty")
            return False

        return True

    # def add_new_group(self, name, trust, members_list):
    #     '''
    #     Description: fonction pour ajouter une grouppe
    #     dans le fichier 'groups.json', selon le format donne dans
    #     la description du lab
    #     Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
    #     '''
    #
    #     try:
    #         groups = self.read_groups_file()
    #         nbGroups = len(groups) + 1
    #         for x in groups:
    #             if groups[x]['name'] == name:
    #                 return False
    #         data = groups
    #         group_json = {"name": name, "Trust": trust, "List_of_members": members_list}
    #         data[nbGroups] = group_json
    #         self.modify_groups_file(data)
    #
    #     except:
    #         print("The file is empty")
    #         return False
    #
    #     return True

    ## ***********READ****************
    def read_users_file(self):
        '''
        fonction deja implemente
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les utilisateurs

        with open(self.users_file) as users_file:
            return json.load(users_file)
        '''
        return self.users_file

    def read_groups_file(self):
        '''
        fonction deja implemente
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les groupes
        with open(self.groups_file) as group_file:
            return json.load(group_file)
        '''
        return self.groups_file

    def get_user_data(self, user_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une utilisateur specifie.
        Par example, spam_number = get_user_data(2, "SpamN") va donner le
        numero de messages spam pour utilisateur avec id 2.
        Sortie: la valeur d'information specifie pour utilisateur
        '''
        try:
            users = self.read_users_file()
            return users[str(user_id)][field]
        except:
            print('Enter a valid field.')

    # def get_group_data(self, group_id, field):
    #     '''
    #     Description: fonction qui sorte la valeur d'information specifie
    #     pour une grouppe specifie.
    #     Par example, group_trust_level = get_group_data(2, "Trust") va donner la
    #     valeur de "Trust" pour grouppe avec id 2.
    #     Sortie: la valeur d'information specifie pour le grouppe
    #     '''
    #     try:
    #         groups = self.read_groups_file()
    #         return groups[group_id][field]
    #     except:
    #         print('Error occured when retrieving the group value')
    #
    # def get_user_id(self, name):
    #     '''
    #     Description: fonction sorte l'id d'utilisateur, donne le nom (email d'utilisater)
    #     Sortie: la valeur d'id d'utilisateur
    #     '''
    #     try:
    #         users = self.read_users_file()
    #         for x in users:
    #             if users[x]['name'] == name:
    #                 return x
    #         print('There is no user with that name')
    #     except:
    #         print('There are no users')
    #
    # def get_group_id(self, name):
    #     '''
    #     Description: fonction sorte l'id de grouppe, donne le nom de grouppe
    #     Sortie: la valeur d'id de grouppe
    #     '''
    #     try:
    #         groups = self.read_groups_file()
    #         for x in groups:
    #             if groups[x]['name'] == name:
    #                 return x
    #         print('There is no group with that name')
    #     except:
    #         print('There are no groups')

    ##*******UPDATE******************

    def modify_users_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        d'utilisateurs dans le fichiers 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.

        with open(self.users_file, "w") as outfile:
            json.dump(data, outfile, indent=4)
        return True
        '''
        self.users_file = data
        return True

    # def modify_groups_file(self, data):
    #     '''
    #     Description: fonction qui ecrit le dictionnaire
    #     des grouppes dans le fichiers 'groups.json'
    #     Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
    #
    #     with open(self.groups_file, "w") as outfile:
    #         json.dump(data, outfile, indent=4)
    #     return True
    #     '''
    #     self.groups_file = data
    #     return True

    def update_users(self, user_id, field, data):
        '''
        Description: fonction qui modifie les donnes d'utilisateur
        Par example, update_users(3, "Trust", 60) va changer le valeur de "Trust"
        pour utilisateur avec id 3 au 60.
        update_users(3, "Groups", "friends") va ajouter le grouppe 'friends'
        pour utilisater avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            users = self.read_users_file()

            user_id = str(user_id)

            if user_id not in users:
                return False

            if field not in users[user_id]:
                return False

            if field == 'Groups':
                users[user_id][field].append(data)
            elif field in users[user_id]:
                users[user_id][field] = data
            else:
                return False

            self.modify_users_file(users)
            return users[user_id][field]

        except:
            print('Please enter valid information')
            return False

    # def update_groups(self, group_id, field, data):
    #     '''
    #     Description: fonction qui modifie les donnes du groupe
    #     Par example, update_groups(2, "Trust", 30) va changer le valeur de "Trust"
    #     pour le grouppe avec id 2 au 30.
    #     update_groups(3, "List_of_members", "test@mail.com") va ajouter l'utilisateur
    #     avec email test@mail.com dans le liste des membres de groupe
    #     avec id 3.
    #     Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
    #     '''
    #     try:
    #         groups = self.read_groups_file()
    #
    #         group_id = str(group_id)
    #
    #         if group_id not in groups:
    #             return False
    #
    #         if field not in groups[group_id]:
    #             return False
    #
    #         if field == 'List_of_members':
    #             groups[group_id][field].append(data)
    #         elif field in groups[group_id]:
    #             groups[group_id][field] = data
    #         else:
    #             return False
    #
    #         self.modify_groups_file(groups)
    #         return groups[group_id][field]
    #     except:
    #         print('Please enter valid information')
    #         return False

    ##***********DELETE***********************

    def remove_user(self, user_id):
        '''
        Description: fonction qui suprime l'utilisateur de fichier 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            users = self.read_users_file()
            users.pop(str(user_id))
            self.modify_users_file(users)
            return True
        except:
            print("This user doesn't exist")
            return False

        # raise NotImplementedError("")

    def remove_user_group(self, user_id, group_name):
        '''
        Description: fonction qui suprime de le fichier 'users.json' le groupe 
        auquel appartient un utilisateur.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            users = self.read_users_file()

            if str(user_id) not in users:
                return False

            users[str(user_id)]['Groups'].remove(group_name)
            self.modify_users_file(users)
            return True
        except:
            print("This user is not part of this group")
            return False

    # def remove_group(self, group_id):
    #     '''
    #     Description: fonction qui suprime le groupe de fichier 'groups.json'
    #     Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
    #     '''
    #     try:
    #         group_id = str(group_id)
    #         groups = self.read_groups_file()
    #         if group_id not in groups:
    #             return False
    #         groups.pop(group_id)
    #         self.modify_groups_file(groups)
    #         return self.read_groups_file()
    #     except:
    #         print("This group doesn't exist")
    #         return False
    #
    # def remove_group_member(self, group_id, member):
    #     '''
    #     Description: fonction qui enleve le membre de le liste des membres pour
    #     un groupe dans le 'groups.json'
    #     Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
    #     '''
    #     try:
    #         group_id = str(group_id)
    #         groups = self.read_groups_file()
    #         if group_id not in groups:
    #             return False
    #         groups[group_id]['List_of_members'].remove(member)
    #         self.modify_groups_file(groups)
    #         return groups[group_id]['List_of_members']
    #     except:
    #         print('This member is not part of this group')
    #         return False
