import json
import os
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils import *
import random
import argparse
import xml.etree.ElementTree as ET


def check_word_in_dictionary(string, dictionary) :
    words = string.split()
    for word in words :
        if word in dictionary :
            return True
    return False

file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/MCScript/test-data.xml')


names_file_path = os.path.join(os.path.dirname(__file__), '../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0].lower()] = {}

i,j,k = 0,0,0
templates = {}

## Code to read a xml file
tree = ET.parse(file_path)
root = tree.getroot()
for child in root :
    row = root[i]
    i += 1
    context = row[0].text

    if not check_word_in_dictionary(context.lower(), names_dict) :
        continue

    j +=1
    for l in range(len(row[1])) :
        qa_pair = row[1][l]
        question = qa_pair.attrib['text']
        answer = qa_pair[1].attrib['text']
        if check_word_in_dictionary(question.lower(), names_dict) or check_word_in_dictionary(answer.lower(), names_dict) :
            template = {}
            template['context'] = context
            template['question'] = question
            template['answer'] = answer
            template['source_dataset'] = "mcscript"

            #if random.randint(0,1) == 0 :
            k +=1
            templates[k] = template

print (j)
print (k)
save_json('mcscript_templates_basic.json', templates)
