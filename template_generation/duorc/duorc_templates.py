import json
import os
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils import *
import random
import argparse


def check_word_in_dictionary(string, dictionary) :
    words = string.split()
    for word in words :
        if word in dictionary :
            return True
    return False

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/duorc/SelfRC_test.json')

dataset = json.load(open(file_path, 'r'))

names_file_path = os.path.join(os.path.dirname(__file__), '../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0]] = {}

j,k = 0,0
templates = {}

for i in range(len(dataset)) : 
    row = dataset[i]
    context = row['plot'].replace('\n', ' ')

    ## count number of words in a string
    len_words = len(context.split())

    if len_words > 400 :
        continue

    if check_word_in_dictionary(context, names_dict) :

        qa_pairs = row['qa']
        
        name_present = False
        for i in range(len(qa_pairs)) :
            qa_pair = qa_pairs[i]
            question = qa_pair['question']
            if len(qa_pair['answers']) == 0 :
                continue
            answer = qa_pair['answers'][0]
            if check_word_in_dictionary(question, names_dict) or check_word_in_dictionary(answer, names_dict) :
                name_present = True
                template = {}
                
                template['context'] = context
                template['question'] = question
                template['answer'] = answer
                template['source_dataset'] = "duorc"

                break

        if name_present :
            j +=1

        if random.randint(0,9) == 0 :
            k +=1
            templates[k] = template
        #pdb.set_trace()
        
        #if j%10 == 0 :
        #    print (context + '\n')

    #    dataset[i]['template'] = template

print (j)
print (k)
save_json('duorc_templates_basic.json', templates)
