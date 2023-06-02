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

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/TweetQA/dev.json')

dataset = json.load(open(file_path, 'r'))

names_file_path = os.path.join(os.path.dirname(__file__), '../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0].lower()] = {}

j,k = 0,0
templates = {}

for i in range(len(dataset)) : 
    row = dataset[i]
    context = row['Tweet']

    ## count number of words in a string
    len_words = len(context.split())

    if len_words > 400 :
        continue

    if check_word_in_dictionary(context.lower(), names_dict) :

        question = row['Question']
        answer = row['Answer'][0]
        if check_word_in_dictionary(question.lower(), names_dict) or check_word_in_dictionary(answer.lower(), names_dict) :
            j += 1
            template = {}
            
            template['context'] = context
            template['question'] = question
            template['answer'] = answer
            template['source_dataset'] = "TweetQA"


            if random.randint(0,9) == 0 :
                k +=1
                templates[k] = template

    

print (j)
print (k)
save_json('tweetqa_templates_basic.json', templates)
