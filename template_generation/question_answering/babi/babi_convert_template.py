import json
import os
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils import *
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--task', type=int, default=6, help='task number')
args = parser.parse_args()


file_path = os.path.join(os.path.dirname(__file__), '../../', 'dataset/babi/task' +str(args.task) + '.json')

dataset = json.load(open(file_path, 'r'))

templates = {}
count, new_count = {}, {}
i=0
for idx in dataset :
    question = dataset[idx]['question']
    context = dataset[idx]['context']
    answer = dataset[idx]['answer']


    if len(context.split(' ')) < 20:
        continue

    if args.task in [6,9,10] :
        person = question.split(' ')[1]
    elif args.task in [1,11,12,13] :
        person = question.split(' ')[2].replace('?', '')
    elif args.task in [8,14] :
        person = question.split(' ')[2]


    #if args.task == 1:
    #    if context.count(person) < 2:
    #        continue

    count_words = len(context.split(' '))
    if count_words not in count:
        count[count_words] = 1
    else :
        count[count_words] += 1

    question_new = question.replace(person, '<PERSON>')
    context_new = context.replace(person, '<PERSON>')

    template = {"question": question_new, "context": context_new, "answer": answer}

    if any(inner_dict == template for inner_dict in templates.values()):
        continue
    else :
        random_int = random.randint(0, 200)
        if random_int ==0 :
            templates[i] = template
            i+=1
            if count_words not in new_count:
                new_count[count_words] = 1
            else :
                new_count[count_words] += 1

print (count)
print (new_count)
print (len(templates))
save_json('templates_task' + str(args.task) + '.json', templates)

