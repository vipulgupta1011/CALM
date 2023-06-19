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

file_path = os.path.join(os.path.dirname(__file__), '../../../', 'dataset/wnli/dev.tsv')

names_file_path = os.path.join(os.path.dirname(__file__), '../../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = read_tsv(file_path)

names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0].lower()] = {}

j,k=0,0
templates = {}
## write to a csv file

print ('datset size : ', len(dataset))

for i in range(1, len(dataset)) :
    row = dataset[i]
    sentence1, sentence2 = row[1], row[2]
    coding = row[3]
    if coding == '0' :
        answer = 'not_entailment'
    else :
        answer = 'entailment'

    if check_word_in_dictionary(sentence1.lower(), names_dict) and check_word_in_dictionary(sentence2.lower(), names_dict) :
        j += 1
        template = {}
        template['premise'] = sentence1
        template['hypothesis'] = sentence2
        template['answer'] = answer
        template['source_dataset'] = "wnli"

        #if random.randint(0,20) == 0 :
        k +=1
        templates[k] = template


save_json('wnli_templates_basic.json', templates)
print (j)
print (k)
