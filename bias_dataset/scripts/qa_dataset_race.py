import json
import pdb, re
import csv
import random
import sys
sys.path.append('../../')
from utils import *
from itertools import islice

qa_templates_path = '../qa_templates.json'
names_dataset_path = '../../names/categorised_data/names_race_categorisation.csv'

random.seed(11)
## read csv filesewdcwdc column wise
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

with open(qa_templates_path, 'r', encoding='utf-8') as fp:
    qa_templates = json.load(fp)

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

for idx in qa_templates:
    template = qa_templates[idx]
    context = template['context']
    question = template['question']
    answer = template['answer']
    source_dataset = template['source_dataset']


    ##White race perturbation
    white_names_random = select_n_random(white_names, 50)
    for j in range(50):
        replace_name = white_names_random[j]
        white_context = context.replace('<PERSON>', replace_name)
        white_question = question.replace('<PERSON>', replace_name)
        white_answer = answer.replace('<PERSON>', replace_name)

        replacements = find_words(white_context)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            white_context = white_context.replace(replacement, word)
            white_question = white_question.replace(replacement, word)

        sample = {}
        sample['context'] = white_context
        sample['question'] = white_question
        sample['answer'] = white_answer
        sample['source_dataset'] = source_dataset
        sample['race'] = 'white'

        dataset.append(sample)
        i += 1

    ##black race perturbation
    black_names_random = select_n_random(black_names, 50)
    for j in range(50):
        replace_name = black_names_random[j]
        black_context = context.replace('<PERSON>', replace_name)
        black_question = question.replace('<PERSON>', replace_name)
        black_answer = answer.replace('<PERSON>', replace_name)

        replacements = find_words(black_context)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            black_context = black_context.replace(replacement, word)
            black_question = black_question.replace(replacement, word)

        sample = {}
        sample['context'] = black_context
        sample['question'] = black_question
        sample['answer'] = black_answer
        sample['source_dataset'] = source_dataset
        sample['race'] = 'black'

        dataset.append(sample)
        i += 1

    ##hispanic race perturbation
    hispanic_names_random = select_n_random(hispanic_names, 50)
    for j in range(50):
        replace_name = hispanic_names_random[j]
        hispanic_context = context.replace('<PERSON>', replace_name)
        hispanic_question = question.replace('<PERSON>', replace_name)
        hispanic_answer = answer.replace('<PERSON>', replace_name)

        replacements = find_words(hispanic_context)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            hispanic_context = hispanic_context.replace(replacement, word)
            hispanic_question = hispanic_question.replace(replacement, word)

        sample = {}
        sample['context'] = hispanic_context
        sample['question'] = hispanic_question
        sample['answer'] = hispanic_answer
        sample['source_dataset'] = source_dataset
        sample['race'] = 'hispanic'

        dataset.append(sample)
        i += 1

    ##asian race perturbation
    asian_names_random = select_n_random(asian_names, 50)
    for j in range(50):
        replace_name = asian_names_random[j]
        asian_context = context.replace('<PERSON>', replace_name)
        asian_question = question.replace('<PERSON>', replace_name)
        asian_answer = answer.replace('<PERSON>', replace_name)

        replacements = find_words(asian_context)

        for replacement in replacements : 
            word = replacement.replace('>', '').split('/')[2]
            asian_context = asian_context.replace(replacement, word)
            asian_question = asian_question.replace(replacement, word)

        sample = {}
        sample['context'] = asian_context
        sample['question'] = asian_question
        sample['answer'] = asian_answer
        sample['source_dataset'] = source_dataset
        sample['race'] = 'asian'

        dataset.append(sample)
        i += 1


with open('../race_datasets/qa_race_dataset.jsonl', 'w+', encoding='utf-8') as fp:
    for line in dataset:
        json.dump(line, fp)
        fp.write('\n')
    fp.close()
