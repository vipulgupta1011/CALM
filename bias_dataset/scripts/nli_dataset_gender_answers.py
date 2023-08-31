import json
import pdb, re
import csv
import random
import sys
sys.path.append('../../')
from utils import *
from itertools import islice

random.seed(10)
nli_templates_path = '../nli_templates.json'
names_dataset_path = '../../names/categorised_data/segregated_names.csv'
non_binary_data_path = '../../names/unisex/unisex_names_table.csv'

non_binary_dataset = read_csv(non_binary_data_path)
non_binary_data = {}
for i in range(1, len(non_binary_dataset)):
    name, difference = non_binary_dataset[i][1], float(non_binary_dataset[i][5])
    non_binary_data[name] = difference

## sort a dictionary in ascending order based on keys value
non_binary_data_sorted = dict(sorted(non_binary_data.items(), key=lambda x: x[1]))

## get top 50 non_binary names
non_binary_names = list(non_binary_data_sorted.keys())[:50]

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

with open(nli_templates_path, 'r', encoding='utf-8') as fp:
    nli_templates = json.load(fp)

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
answers_save.append(["idx","template_idx","answer","gender","source_dataset"])
for idx in nli_templates:
    template = nli_templates[idx]
    premise = template['premise']
    hypothesis = template['hypothesis']
    answer = template['answer']
    options = template['options']
    source_dataset = template['source_dataset']


    ##Male perturbation
    male_names_random = select_n_random(male_names, 50)
    for j in range(50):
        replace_name = male_names_random[j]
        male_premise = premise.replace('<PERSON>', replace_name)
        male_hypothesis = hypothesis.replace('<PERSON>', replace_name)
        male_answer = answer.replace('<PERSON>', replace_name)

        replacements = find_words(male_premise + male_hypothesis)

        for replacement in replacements : 
            word = replacement.replace('<', '').split('/')[0]
            male_premise = male_premise.replace(replacement, word)
            male_hypothesis = male_hypothesis.replace(replacement, word)
            male_answer = male_answer.replace(replacement, word)

        #sample = {}
        #sample['premise'] = male_premise
        #sample['hypothesis'] = male_hypothesis
        #sample['answer'] = male_answer
        #sample['source_dataset'] = source_dataset
        #sample['options'] = options
        #sample['gender'] = 'male'

        answer_idx = [i, idx, male_answer, "male", source_dataset]
        answers_save.append(answer_idx)
        
        #dataset.append(sample)
        i += 1

    ##Female perturbation
    female_names_random = select_n_random(female_names, 50)
    for j in range(50):
        replace_name = female_names_random[j] 
        female_premise = premise.replace('<PERSON>', replace_name)
        female_hypothesis = hypothesis.replace('<PERSON>', replace_name)
        female_answer = answer.replace('<PERSON>', replace_name)

        for replacement in replacements :
            word = replacement.replace('>', '').split('/')[1]
            female_premise = female_premise.replace(replacement, word)
            female_hypothesis = female_hypothesis.replace(replacement, word)
            female_answer = female_answer.replace(replacement, word)

        #sample = {}
        #sample['premise'] = female_premise
        #sample['hypothesis'] = female_hypothesis
        #sample['answer'] = female_answer
        #sample['source_dataset'] = source_dataset
        #sample['options'] = options
        #sample['gender'] = 'female'

        answer_idx = [i, idx, female_answer, "female", source_dataset]
        answers_save.append(answer_idx)
        #dataset.append(sample)
        i += 1

    ##non_binary perturbation
    for name in non_binary_names : 
        replace_name = name
        non_binary_premise = premise.replace('<PERSON>', replace_name)
        non_binary_hypothesis = hypothesis.replace('<PERSON>', replace_name)
        non_binary_answer = answer.replace('<PERSON>', replace_name)

        for replacement in replacements :
            word = replacement.replace('>', '').split('/')[2]
            non_binary_premise = non_binary_premise.replace(replacement, word)
            non_binary_hypothesis = non_binary_hypothesis.replace(replacement, word)
            non_binary_answer = non_binary_answer.replace(replacement, word)

        #sample = {}
        #sample['premise'] = female_premise
        #sample['hypothesis'] = female_hypothesis
        #sample['answer'] = female_answer
        #sample['source_dataset'] = source_dataset
        #sample['options'] = options
        #sample['gender'] = 'non_binary'

        answer_idx = [i, idx, non_binary_answer, "non-binary", source_dataset]
        answers_save.append(answer_idx)
        #dataset.append(sample)
        i += 1


write_csv(answers_save, "/home/nlp/vkg5164/code/bias_dataset/evaluation/gt/gt_nli_gender.csv")
