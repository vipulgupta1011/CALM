import json, os, csv
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils import *
import random
import argparse


def load_tsv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def check_word_in_dictionary(string, dictionary) :
    words = string.split()
    for word in words :
        if word in dictionary :
            return True
    return False

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/mctest/mc500.test.tsv')
ans_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/mctest/mc500.test.ans')

names_file_path = os.path.join(os.path.dirname(__file__), '../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = load_tsv_file(file_path)
answers = load_tsv_file(ans_path)

names_dict = {}
templates = {}

for row in names_dataset[1:] :
    names_dict[row[0]] = {}

j=0
for row in dataset :
    context = row[2]
    if check_word_in_dictionary(context, names_dict) :
        question_1 = row[3]
        question_2 = row[8]
        question_3 = row[13]
        question_4 = row[18]
        answer_row = answers[int(row[0].split('.')[2])]

        #if check_word_in_dictionary(question_1, names_dict) or check_word_in_dictionary(question_2, names_dict) or check_word_in_dictionary(question_3, names_dict) or check_word_in_dictionary(question_4, names_dict) :
        #    j+=1
        #    print(row[0])

        included = False

        if check_word_in_dictionary(question_1, names_dict) or check_word_in_dictionary(row[4], names_dict) or check_word_in_dictionary(row[5], names_dict) or check_word_in_dictionary(row[6], names_dict) or check_word_in_dictionary(row[7], names_dict) :

            if random.randint(0,5) == 0 :
                template = {}
                template['context'] = context
                template['question'] = question_1 + ' Possible Answers : ' + '  A: ' + row[4] + '  B: ' + row[5] + '  C: ' + row[6] + '  D: ' + row[7]
                template['answer'] = answer_row[0]
                included = True

        if (not included) and (check_word_in_dictionary(question_2, names_dict) or check_word_in_dictionary(row[9], names_dict) or check_word_in_dictionary(row[5], names_dict) or check_word_in_dictionary(row[11], names_dict) or check_word_in_dictionary(row[12], names_dict)) :

            if random.randint(0,5) == 0 :
                template = {}
                template['context'] = context
                template['question'] = question_2 + ' Possible Answers : ' + '  A: ' + row[9] + '  B: ' + row[10] + '  C: ' + row[11] + '  D: ' + row[12]
                template['answer'] = answer_row[1]
                included = True

        if (not included) and (check_word_in_dictionary(question_3, names_dict) or check_word_in_dictionary(row[14], names_dict) or check_word_in_dictionary(row[15], names_dict) or check_word_in_dictionary(row[16], names_dict) or check_word_in_dictionary(row[17], names_dict)) :
            if random.randint(0,5) == 0 :
                template = {}
                template['context'] = context
                template['question'] = question_3 + ' Possible Answers : ' + '  A: ' + row[14] + '  B: ' + row[15] + '  C: ' + row[16] + '  D: ' + row[17]
                template['answer'] = answer_row[2]
                included = True

        if (not included) and (check_word_in_dictionary(question_4, names_dict) or check_word_in_dictionary(row[19], names_dict) or check_word_in_dictionary(row[20], names_dict) or check_word_in_dictionary(row[21], names_dict) or check_word_in_dictionary(row[22], names_dict)) :
            if random.randint(0,5) == 0 :
                template = {}
                template['context'] = context
                template['question'] = question_4 + ' Possible Answers : ' + '  A: ' + row[19] + '  B: ' + row[20] + '  C: ' + row[21] + '  D: ' + row[22]
                template['answer'] = answer_row[3]
                included = True


        if included :
            templates[j] = template
            j+=1

save_json('mctest500_templates.json', templates)

print(j)
