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

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/qamr/test.tsv')

names_file_path = os.path.join(os.path.dirname(__file__), '../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = load_tsv_file(file_path)

names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0]] = {}

j=0

template_dict = {}
for i in range(len(dataset)) : 
    row = dataset[i]
    ## finding rows with context
    if row == [] or not row[0].startswith('#Wiki1k') :
        continue

    context = dataset[i+1][0]

    if check_word_in_dictionary(context, names_dict) :
        j +=1
        template = {}
        
        template['context'] = context
        template['question'] = ""
        template['answer'] = ""
        template['source_dataset'] = "qamr"

        template_dict[j] = template


save_json('qamr_templates_basic.json', template_dict)
print (j)

