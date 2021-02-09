import json
from vocabulary_creator_tp1 import VocabularyCreatorTP1
from renege import RENEGE
from email_analyzer_tp1 import EmailAnalyzer


def evaluate():
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0

    # Mettre le vocabulary qu'on veut utiliser
    analyzer = EmailAnalyzer('vocabulary_train700.json')

    # Mettre le bon fichier test
    with open("test300.json") as email_file:
        new_emails = json.load(email_file)

    for e_mail in new_emails["dataset"]:
        print('loading')
        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if ((analyzer.is_spam(subject, body))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "true"):
            fn += 1
        total += 1
    print("Accuracy: ", (tp + tn) / (tp + tn + fp + fn))
    print("Precision: ", tp / (tp + fp))
    print("Recall: ", tp / (tp + fn))
    return True


if __name__ == "__main__":

    # 1. Creation de vocabulaire.
    # vocab = VocabularyCreatorTP1()
    # vocab.create_vocab()

    # 2. Classification des emails et initialisation de utilisateurs et groupes.
    # renege = RENEGE()
    # renege.classify_emails()

    #3. Evaluation de performance du modele avec la fonction evaluate()
    evaluate()
