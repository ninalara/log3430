import json


class CRUD:
    """
    Classe pour realiser la fonctionalite CRUD.
    """

    def __init__(self):
        self.users_file = "users.json"
        self.groups_file = "groups.json"
        self.number_of_users = 0
        self.number_of_groups = 0
    ##*************CREATE**************

    def add_new_user(self, user_email, date):
        '''
        Description: fonction pour ajouter un nouvel utilisateur 
        dans le fichier 'users.json', selon le format donné dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        if not user_email or not date:
            return False

        self.number_of_users += 1
        user = {
            'name': user_email,
            'Trust': 50,
            'SpamN': 0,
            'HamN': 0,
            'Date_of_first_seen_message': date,
            'Date_of_last_seen_message': date,
            'Groups': ['default']
        }
        json_object = {str(self.number_of_users): user}

        try:
            with open(self.users_file, 'a') as users_file:
                json.dump(json_object, users_file)
        except IOError:
            self.number_of_users -= 1
            return False

        return True

    def add_new_group(self, name, trust, members_list):
        '''
        Description: fonction pour ajouter une grouppe  
        dans le fichier 'groups.json', selon le format donne dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        if len(name) > 64 or len(name) < 1 or trust < 0 or trust > 100 or not isinstance(members_list, list):
            return False

        self.number_of_groups += 1
        group = {"name": name,
                 "Trust": trust,
                 "List_of_members" : members_list
                 }
        json_object = {str(self.number_of_groups): group}

        try:
            with open(self.groups_file, 'a') as groups_file:
                json.dump(json_object, groups_file)
        except IOError as e:
            self.number_of_groups -= 1
            return False

        return True

    ###***********READ****************
    def read_users_file(self):
        '''
        fonction deja implemente
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les utilisateurs 
        '''
        with open(self.users_file) as users_file:
            return json.load(users_file)

    def read_groups_file(self):
        '''
        fonction deja implemente
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les groupes
        '''
        with open(self.groups_file) as group_file:
            return json.load(group_file)

    def get_user_data(self, user_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une utilisateur specifie.
        Par example, spam_number = get_user_data(2, "SpamN") va donner le
        numero de messages spam pour utilisateur avec id 2.
        Sortie: la valeur d'information specifie pour utilisateur
        '''
        if field != "name" and field != "Trust" and field != "SpamN" and field != "HamN" \
                and field != "Date_of_first_seen_message" and field != "Date_of_last_seen_message" \
                and field != "Groups":
            return None

        if int(user_id) < 0 or int(user_id) > self.number_of_users:
            return None

        users_dict = self.read_users_file()
        user = users_dict.get(str(user_id))
        specified_user_data = user.get(field)

        return specified_user_data

    def get_group_data(self, group_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une grouppe specifie.
        Par example, group_trust_level = get_group_data(2, "Trust") va donner la
        valeur de "Trust" pour grouppe avec id 2.
        Sortie: la valeur d'information specifie pour le grouppe
        '''
        if field != "name" and field != "Trust" and field != "List_of_members":
            return None

        if group_id < 0 or group_id > self.number_of_groups:
            return None

        groups_dict = self.read_groups_file()
        group = groups_dict.get(str(group_id))
        specified_group_data = group.get(field)

        return specified_group_data

    def get_user_id(self, name):
        '''
        Description: fonction sorte l'id d'utilisateur, donne le nom (email d'utilisater)
        Sortie: la valeur d'id d'utilisateur
        '''
        try:
            users_dict = self.read_users_file()
            for key in users_dict:
                user = users_dict.get(key)
                if user.get("name") == name:
                    return key
        except Exception:
            return None

    def get_group_id(self, name):
        '''
        Description: fonction sorte l'id de grouppe, donne le nom de grouppe
        Sortie: la valeur d'id de grouppe
        '''
        groups_dict = self.read_groups_file()
        for key in groups_dict:
            group = groups_dict.get(key)
            if group.get("name") == name:
                return key

        return None

    ##*******UPDATE******************

    def modify_users_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        d'utilisateurs dans le fichiers 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.users_file, "w") as outfile:
            json.dump(data, outfile)
        return True

    def modify_groups_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        des grouppes dans le fichiers 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.groups_file, "w") as outfile:
            json.dump(data, outfile)
        return True

    def update_users(self, user_id, field, data):
        '''
        Description: fonction qui modifie les donnes d'utilisateur
        Par example, update_users(3, "Trust", 60) va changer le valeur de "Trust"
        pour utilisateur avec id 3 au 60.
        update_users(3, "Groups", "friends") va ajouter le grouppe 'friends'
        pour utilisater avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        user_dict = self.read_users_file()
        try:
            check_val = user_dict[user_id][field]
            user_dict[user_id][field] = data
        except KeyError:
            return False

        self.modify_users_file(user_dict)

        return True

    def update_groups(self, group_id, field, data):
        '''
        Description: fonction qui modifie les donnes du groupe
        Par example, update_groups(2, "Trust", 30) va changer le valeur de "Trust"
        pour le grouppe avec id 2 au 30.
        update_groups(3, "List_of_members", "test@mail.com") va ajouter l'utilisateur
        avec email test@mail.com dans le liste des membres de groupe
        avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        group_dict = self.read_groups_file()

        try:
            check_val = group_dict[group_id][field]
            group_dict[group_id][field] = data
        except KeyError:
            return False

        self.modify_groups_file(group_dict)

        return True

    ##***********DELETE***********************

    def remove_user(self, user_id):
        '''
        Description: fonction qui suprime l'utilisateur de fichier 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        users = self.read_users_file()

        try:
            users.pop(user_id)
        except KeyError:
            return False

        self.modify_users_file(users)

        return True

    def remove_user_group(self, user_id, group_name):
        '''
        Description: fonction qui suprime de le fichier 'users.json' le groupe 
        auquel appartient un utilisateur.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        users = self.read_users_file()

        try:
            users[user_id]['Groups'].remove(group_name)
        except (KeyError, ValueError):
            return False

        self.modify_users_file(users)

        return True

    def remove_group(self, group_id):
        '''
        Description: fonction qui suprime le groupe de fichier 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        groups = self.read_groups_file()

        try:
            groups.pop(group_id)
        except KeyError:
            return False

        self.modify_groups_file(groups)

        return True

    def remove_group_member(self, group_id, member):
        '''
        Description: fonction qui enleve le membre de le liste des membres pour
        un groupe dans le 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        groups = self.read_groups_file()
        try:
            groups[group_id]["List_of_members"].remove(member)
        except (KeyError,ValueError):
            return False

        self.modify_groups_file(groups)
        return True
