import json
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from csv import reader

def evaluate(is_log_estimation, is_log_combination, clean_text_mode, k):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test_set.json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])

    print("Evaluating emails ")
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end="")

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if ((analyzer.is_spam(subject, body, is_log_estimation, is_log_combination, clean_text_mode, k))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body, is_log_estimation, is_log_combination, clean_text_mode, k))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body, is_log_estimation, is_log_combination, clean_text_mode, k))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body, is_log_estimation, is_log_combination, clean_text_mode, k))) and (spam == "true"):
            fn += 1
        total += 1
    
    print("")
    print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
    if(tp+fp == 0):
        print("Precision: ", 0)
    else:
        print("Precision: ", round(tp / (tp + fp), 2))
    print("Recall: ", round(tp / (tp + fn), 2))
    return True

def read_csv(csv_file):
    with open(csv_file) as inputfile:
        csv = reader(inputfile)
        lines = []
        header = next(csv)
        for line in csv:
            lines.append(line)

    return lines

if __name__ == "__main__":

    rows = read_csv("test_cases-output.csv")

    # 1. Creation de vocabulaire.
    vocab = VocabularyCreator()
    for row in rows:
        is_log_estimation = int(row[0])
        is_log_combination = int(row[1])
        word_frequency = int(row[2])
        clean_text_mode = int(row[3])
        spam_formula = int(row[4])

        vocab.create_vocab(word_frequency, clean_text_mode)

        # 2. Classification des emails et initialisation de utilisateurs et groupes.
        renege = RENEGE()
        renege.classify_emails(spam_formula)

        #3. Evaluation de performance du modele avec la fonction evaluate()
        evaluate(is_log_estimation, is_log_combination, clean_text_mode, 0.4)



