import json
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from csv import reader


def evaluate(estimation_option, combination_option):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test-emails.json") as email_file:
        new_emails = json.load(email_file)

    for e_mail in new_emails["dataset"]:
        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if (analyzer.is_spam_with_params(subject, body, estimation_option, combination_option, cleaning_mode, 0.3)) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam_with_params(subject, body, estimation_option, combination_option, cleaning_mode, 0.3))) and (spam == "false"):
            tn += 1
        if (analyzer.is_spam_with_params(subject, body, estimation_option, combination_option, cleaning_mode, 0.3)) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam_with_params(subject, body, estimation_option, combination_option, cleaning_mode, 0.3))) and (spam == "true"):
            fn += 1
        total += 1
    print("Accuracy: ", (tp + tn) / (tp + tn + fp + fn))
    print("Precision: ", tp / (tp + fp))
    print("Recall: ", tp / (tp + fn))
    return True


def read_cvs(file_name):
    with open(file_name) as test_file:
        csv = reader(test_file)
        all_lines = []
        # permet de sauter la ligne du header du tableau dans le fichier
        header = next(csv)
        for line in csv:
            all_lines.append(line)

        return all_lines


if __name__ == "__main__":
    # 1. Saisir les cas de tests du fichier .csv
    all_rows = read_cvs("TC.csv")

    vocab = VocabularyCreator()

    for row in all_rows:
        # 2. Creation de vocabulaire
        prob_calculation_option = int(row[0])
        prob_combination_option = int(row[1])
        word_frequency_mode = int(row[2])
        cleaning_mode = int(row[3])
        spam_def_mode = int(row[4])
        vocab.create_vocab(word_frequency_mode, cleaning_mode)

        # 3. Classification des emails et initialisation de utilisateurs et groupes
        renege = RENEGE()
        renege.classify_emails(spam_def_mode)

        # 4. Evaluation de performance du modele avec la fonction evaluate()
        print("For test case ", row)
        evaluate(prob_calculation_option, prob_combination_option)
        print("----------------------------------------------------------")
