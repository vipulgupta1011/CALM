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

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/sodapop/socialIQa_v1.4_dev_Bethany_0_2191.jsonl')

## code to read a jsonl file
dataset = []
with open(file_path) as f :
    for line in f :
        dataset.append(json.loads(line))

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
    context = row['context']

    question = row['question']
               
    if check_word_in_dictionary(question, names_dict) :
        j +=1

    #template = 
    #
    #template['context'] = context
    #template['question'] = question
    #template['answer'] = answer
    #template['source_dataset'] = "relation_extraction"
    #template['sub_word'] = sub_word


        if random.randint(0,20) == 0 :
            k +=1
            templates[k] = row

print (j)
print (k)
save_json('sodapop_templates_basic.json', templates)
