import json
import pdb, re
import csv
import random
import sys
sys.path.append('../../')
from utils import *
from itertools import islice

random.seed(10)
sentiment_templates_path = '../sentiment_templates.json'
names_dataset_path = '../../names/categorised_data/segregated_names.csv'
unisex_data_path = '../../names/unisex/unisex_names_table.csv'

unisex_dataset = read_csv(unisex_data_path)
unisex_data = {}
for i in range(1, len(unisex_dataset)):
    name, difference = unisex_dataset[i][1], float(unisex_dataset[i][5])
    unisex_data[name] = difference

## sort a dictionary in ascending order based on keys value
unisex_data_sorted = dict(sorted(unisex_data.items(), key=lambda x: x[1]))

## get top 50 unisex names
unisex_names = list(unisex_data_sorted.keys())[:50]

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


##read csv file
def read_csv(names_dataset_path):
    with open(names_dataset_path, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    return lines

names_dataset = read_csv_column_wise(names_dataset_path)

male_names, female_names = [], []

for idx in range(len(names_dataset['Name'])):
    name = names_dataset['Name'][idx]
    if names_dataset['usa.male'][idx]=='1' and names_dataset['usa.female'][idx]=='0' :
        male_names.append(name)
    if names_dataset['usa.male'][idx]=='0' and names_dataset['usa.female'][idx]=='1' :
        female_names.append(name)

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

for idx in sentiment_templates:
    template = sentiment_templates[idx]
    sentence = template['sentence']
    answer = template['answer']
    source_dataset = template['source_dataset']


    ##Male perturbation
    male_names_random = select_n_random(male_names, 50)
    for j in range(50):
        replace_name = male_names_random[j]
        male_sentence = sentence.replace('<PERSON>', replace_name)

        replacements = find_words(male_sentence)

        for replacement in replacements : 
            word = replacement.replace('<', '').split('/')[0]
            male_sentence = male_sentence.replace(replacement, word)

        sample = {}
        sample['sentence'] = male_sentence
        sample['answer'] = answer
        sample['source_dataset'] = source_dataset
        sample['gender'] = 'male'

        dataset.append(sample)
        i += 1

    ##Female perturbation
    female_names_random = select_n_random(female_names, 50)
    for j in range(50):
        replace_name = female_names_random[j] 
        female_sentence = sentence.replace('<PERSON>', replace_name)

        for replacement in replacements :
            word = replacement.replace('>', '').split('/')[1]
            female_sentence = female_sentence.replace(replacement, word)

        sample = {}
        sample['sentence'] = female_sentence
        sample['answer'] = answer
        sample['source_dataset'] = source_dataset
        sample['gender'] = 'female'

        dataset.append(sample)
        i += 1

    ##Unisex perturbation
    for name in unisex_names : 
        replace_name = name
        unisex_sentence = sentence.replace('<PERSON>', replace_name)

        for replacement in replacements :
            word = replacement.replace('>', '').split('/')[2]
            unisex_sentence = unisex_sentence.replace(replacement, word)

        sample = {}
        sample['sentence'] = unisex_sentence
        sample['answer'] = answer
        sample['source_dataset'] = source_dataset
        sample['gender'] = 'unisex'

        dataset.append(sample)
        i += 1

with open('../gender_datasets/sentiment_gender_dataset.jsonl', 'w+', encoding='utf-8') as fp:
    for line in dataset:
        json.dump(line, fp)
        fp.write('\n')
    fp.close()
