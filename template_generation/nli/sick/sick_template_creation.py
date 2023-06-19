import json, os, csv
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from utils import *
import random
import argparse

def check_word_in_dictionary(string, dictionary, debug=False) :
    words = string.split()
    for word in words :
        if word in dictionary :
            if debug :
                print (word)
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

file_path = os.path.join(os.path.dirname(__file__), '../../../', 'dataset/sick/test.csv')

names_file_path = os.path.join(os.path.dirname(__file__), '../../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = read_csv(file_path)

names_dict = {}

for row in names_dataset[1:2000] :
    names_dict[row[0].lower()] = {}

#pdb.set_trace()
j,k=0,0
templates = {}

print ('datset size : ', len(dataset))

for i in range(1, len(dataset)) :
    row = dataset[i]
    sentence1, sentence2, coding = row[1], row[2], row[3]
    if coding == '0' :
        answer = 'entailement'
    if coding == '1' :
        answer = 'neutral'
    if coding == '2' :
        answer = 'contradiction'

    if check_word_in_dictionary(sentence1.lower(), names_dict) and check_word_in_dictionary(sentence2.lower(), names_dict) :
        j += 1
        template = {}
        template['premise'] = sentence1
        template['hypothesis'] = sentence2
        template['answer'] = answer
        template['source_dataset'] = "sick"

        #if random.randint(0,1) == 0 :
        k +=1
        templates[k] = template

save_json('sick_templates_basic.json', templates)
print (j)
print (k)
