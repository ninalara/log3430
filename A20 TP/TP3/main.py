import json
import csv
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer

def runTestCases():
    with open('TP3.csv', mode='r') as csv_file:
        tests_reader = csv.reader(csv_file, delimiter=',')
    with open('TP3.csv', mode='w') as csv_file:
        tests_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in tests_reader:
            vocab.create_vocab(row[2], row[3])
            renege.classify_emails(row[0], row[1], row[4])
            accuracy, precision, recall = evaluate(row[0], row[1], row[4])
            row.append(accuracy)
            row.append(precision)
            row.append(recall)
            tests_writer.writerow(row)

def evaluate(is_log_estimation, is_log_combo, calculation_mode):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("200-mails.json") as email_file:
        new_emails = json.load(email_file)

    counter = 0
    for e_mail in new_emails["dataset"]:
        counter += 1
        print(counter)
        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if ((analyzer.is_spam(subject, body, is_log_estimation, False, 0))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body, False, False, 0))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body, False, False, 0))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body, False, False, 0))) and (spam == "true"):
            fn += 1
        total += 1
    
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print("Accuracy: ", accuracy)
    print("Precision: ", tp / (tp + fp))
    print("Recall: ", tp / (tp + fn))

    return accuracy, precision, recall


if __name__ == "__main__":

    # execution de tous les cas de tests
    runTestCases()