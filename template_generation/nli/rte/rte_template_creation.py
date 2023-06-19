import json, os, csv
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from utils import *
import random
import argparse

def check_word_in_dictionary(string, dictionary) :
    words = string.split()
    for word in words :
        if word in dictionary :
            return True
    return False

def count_words_in_dictionary(string, dictionary) :
    count=0
    words = string.split()
    for word in words :
        if word in dictionary :
            count += 1
            #return True
    return count

file_path = os.path.join(os.path.dirname(__file__), '../../../', 'dataset/RTE/val.jsonl')

names_file_path = os.path.join(os.path.dirname(__file__), '../../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = read_jsonl(file_path)

names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0].lower()] = {}

j,k=0,0
templates = {}
## write to a csv file

lengths = {'0-20':0, '20-40':0, '40-60':0, '60-80':0, '80-100':0, '100-120':0, '120+': 0}
print ('datset size : ', len(dataset))

for i in range(len(dataset)) :
    row = dataset[i]
    sentence1, sentence2 = row['premise'], row['hypothesis']

    if check_word_in_dictionary(sentence1.lower(), names_dict) and check_word_in_dictionary(sentence2.lower(), names_dict) :
        j += 1
        template = {}
        template['premise'] = sentence1
        template['hypothesis'] = sentence2
        template['answer'] = row['label']
        template['source_dataset'] = "RTE"

        if random.randint(0,1) == 0 :
            k +=1
            templates[k] = template
            length = len(sentence1.split())
            ## if length is less than 20
            if length < 20 :
                lengths['0-20'] += 1
            elif length < 40 :
                lengths['20-40'] += 1
            elif length < 60 :
                lengths['40-60'] += 1
            elif length < 80 :
                lengths['60-80'] += 1
            elif length < 100 :
                lengths['80-100'] += 1
            elif length < 120 :
                lengths['100-120'] += 1
            else :
                lengths['120+'] += 1


print (lengths) 
save_json('rte_templates_basic.json', templates)
print (j)
print (k)
