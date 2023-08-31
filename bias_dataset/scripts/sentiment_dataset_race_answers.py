import json
import pdb, re
import csv
import random
import sys
sys.path.append('../../')
from utils import *
from itertools import islice

sentiment_templates_path = '../sentiment_templates.json'
names_dataset_path = '../../names/categorised_data/names_race_categorisation.csv'

random.seed(11)
## read csv file column wise
def read_csv_column_wise(path):
    with open(path, 'r') as file:
        reader = csv.reader(file)
        
        # Read the first row to get the column names
        columns = next(reader)
        
        # Create a dictionary to store the column data
        data = {col: [] for col in columns}
        
        # Iterate through each row and store the values in the respective columns
        for row in reader:
            for i, value in enumerate(row):
                data[columns[i]].append(value)
    return data

names_dataset = read_csv_column_wise(names_dataset_path)

white_names, black_names, hispanic_names, asian_names = [], [], [], []

## filtering names for each race
for idx in range(len(names_dataset['Name'])):
    name = names_dataset['Name'][idx]
    if names_dataset['usa.white'][idx]=='1' and names_dataset['usa.black'][idx]=='0' and names_dataset['usa.hispanic'][idx]=='0' and names_dataset['usa.asian'][idx]=='0' :
        white_names.append(name)
    if names_dataset['usa.white'][idx]=='0' and names_dataset['usa.black'][idx]=='1' and names_dataset['usa.hispanic'][idx]=='0' and names_dataset['usa.asian'][idx]=='0' :
        black_names.append(name)
    if names_dataset['usa.white'][idx]=='0' and names_dataset['usa.black'][idx]=='0' and names_dataset['usa.hispanic'][idx]=='1' and names_dataset['usa.asian'][idx]=='0' :
        hispanic_names.append(name)
    if names_dataset['usa.white'][idx]=='0' and names_dataset['usa.black'][idx]=='0' and names_dataset['usa.hispanic'][idx]=='0' and names_dataset['usa.asian'][idx]=='1' :
        asian_names.append(name)

#pdb.set_trace()

##select random key from a dictionary
def select_random(list_name):
    return random.choice(list_name)

##select n random entries from a list without replacements
def select_n_random(list_name, n):
    return random.sample(list_name, n)

with open(sentiment_templates_path, 'r', encoding='utf-8') as fp:
    sentiment_templates = json.load(fp)

## in a string find all words which start with < and end with >
def find_words(string):
    replacements = re.findall(r'<.*?>', string)

    return create_unique_list(replacements)

## given a list of strings, create a list of all unique string
def create_unique_list(list_of_strings):
    unique_list = []
    for string in list_of_strings:
        if string not in unique_list:
            unique_list.append(string)
    return unique_list

dataset = []
i=0

answers_save = []
answers_save.append(["idx","template_idx","answer","race","source_dataset"])
for idx in sentiment_templates:
    template = sentiment_templates[idx]
    sentence = template['sentence']
    answer = template['answer']
    source_dataset = template['source_dataset']


    ##White race perturbation
    white_names_random = select_n_random(white_names, 50)
    for j in range(50):
        replace_name = white_names_random[j]
        white_sentence = sentence.replace('<PERSON>', replace_name)

        replacements = find_words(white_sentence)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            white_sentence = white_sentence.replace(replacement, word)

        #sample = {}
        #sample['sentence'] = white_sentence
        #sample['answer'] = answer
        #sample['source_dataset'] = source_dataset
        #sample['race'] = 'white'

        answer_idx = [i, idx, answer, "white", source_dataset]
        answers_save.append(answer_idx)
        #dataset.append(sample)
        i += 1

    ##black race perturbation
    black_names_random = select_n_random(black_names, 50)
    for j in range(50):
        replace_name = black_names_random[j]
        black_sentence = sentence.replace('<PERSON>', replace_name)

        replacements = find_words(black_sentence)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            black_sentence = black_sentence.replace(replacement, word)

        #sample = {}
        #sample['sentence'] = black_sentence
        #sample['answer'] = answer
        #sample['source_dataset'] = source_dataset
        #sample['race'] = 'black'
        answer_idx = [i, idx, answer, "black", source_dataset]
        answers_save.append(answer_idx)

        #dataset.append(sample)
        i += 1

    ##hispanic race perturbation
    hispanic_names_random = select_n_random(hispanic_names, 50)
    for j in range(50):
        replace_name = hispanic_names_random[j]
        hispanic_sentence = sentence.replace('<PERSON>', replace_name)

        replacements = find_words(hispanic_sentence)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            hispanic_sentence = hispanic_sentence.replace(replacement, word)

        #sample = {}
        #sample['sentence'] = hispanic_sentence
        #sample['answer'] = answer
        #sample['source_dataset'] = source_dataset
        #sample['race'] = 'hispanic'
        answer_idx = [i, idx, answer, "hispanic", source_dataset]
        answers_save.append(answer_idx)

        #dataset.append(sample)
        i += 1

    ##asian race gt   
    asian_names_random = select_n_random(asian_names, 50)
    for j in range(50):
        replace_name = asian_names_random[j]
        asian_sentence = sentence.replace('<PERSON>', replace_name)

        replacements = find_words(asian_sentence)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            asian_sentence = asian_sentence.replace(replacement, word)

        #sample = {}
        #sample['sentence'] = asian_sentence
        #sample['answer'] = answer
        #sample['source_dataset'] = source_dataset
        #sample['race'] = 'asian'
        answer_idx = [i, idx, answer, "asian", source_dataset]
        answers_save.append(answer_idx)

        #dataset.append(sample)
        i += 1


write_csv(answers_save, "/home/nlp/vkg5164/code/bias_dataset/evaluation/gt/gt_sentiment_race.csv")
