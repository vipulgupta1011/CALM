import json
import pdb, re

qa_templates_path = '../similarity/qa_templates_filtered.json'
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

dataset = {}
i=0

for idx in qa_templates:
    template = qa_templates[idx]
    context = template['context']
    question = template['question']
    if 'answer' in template:
        answer = template['answer']
    else :
        answer = template['correct']

    ##Male perturbation
    male_context = context.replace('<PERSON>', 'James')
    male_question = question.replace('<PERSON>', 'James')
    male_answer = answer.replace('<PERSON>', 'James')

    replacements = find_words(male_context)

    for replacement in replacements : 
        word = replacement.replace('<', '').split('/')[0]
        male_context = male_context.replace(replacement, word)
        male_question = male_question.replace(replacement, word)

    sample = {}
    sample['context'] = male_context
    sample['question'] = male_question
    sample['answer'] = male_answer

    dataset[i] = sample
    i += 1

    ##Female perturbation
    female_context = context.replace('<PERSON>', 'Olivia')
    female_question = question.replace('<PERSON>', 'Olivia')
    female_answer = answer.replace('<PERSON>', 'Olivia')

    for replacement in replacements :
        word = replacement.replace('>', '').split('/')[1]
        female_context = female_context.replace(replacement, word)
        female_question = female_question.replace(replacement, word)

    sample = {}
    sample['context'] = female_context
    sample['question'] = female_question
    sample['answer'] = female_answer

    dataset[i] = sample
    i += 1

with open('dataset.json', 'w+', encoding='utf-8') as fp:
    json.dump(dataset, fp, indent=4)


