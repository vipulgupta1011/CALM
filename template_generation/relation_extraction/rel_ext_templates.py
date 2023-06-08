import json
import os
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils import *
import random
import argparse
import csv


def check_word_in_dictionary(string, dictionary) :
    words = string.split()
    for word in words :
        if word in dictionary :
            return True
    return False

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/relation_extraction/test.0')

## read tab-delimited textual (UTF-8) file
def read_csv_tabs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        return list(reader) 

dataset = read_csv_tabs(file_path)

names_file_path = os.path.join(os.path.dirname(__file__), '../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0].lower()] = {}

j,k = 0,0
templates = {}

question_types = {}
for i in range(len(dataset)) : 
    row = dataset[i]
    context = row[3]

    ## count number of words in a string
    len_words = len(context.split())

    if len_words > 400 :
        continue

    #if 'touchdown' in context :
    #    continue

    if check_word_in_dictionary(context.lower(), names_dict) :

        sub_word = row[2]

        if len(row) < 5 :
            continue
        if row[4] == '' :
            continue

        if not check_word_in_dictionary(sub_word.lower(), names_dict) :
            continue

        question_type = row[0]
        #if question_type not in question_types :
        #    question_types[question_type] = 1
        #else :
        #    question_types[question_type] += 1

        if question_type not in ['occupation', 'medical condition'] :
            continue

        j += 1
        question = row[1].replace('XXX', sub_word)
        answer = row[4]
                
        template = {}
        
        template['context'] = context.replace(sub_word, '<PERSON>')
        template['question'] = question.replace(sub_word, '<PERSON>')
        template['answer'] = answer.replace(sub_word, '<PERSON>')
        template['source_dataset'] = "relation_extraction"
        template['sub_word'] = sub_word


        if random.randint(0,9) == 0 :
            k +=1
            templates[k] = template

print (j)
print (k)
save_json('relation_extract_templates_basic.json', templates)
