import json, time
from evaluate import load
import pdb, re
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--task', type=str, default='qa', help='qa or nli or sentiment')

args = parser.parse_args()

bertscore = load("bertscore")

if args.task == 'qa':
    templates = 'qa_templates.json'
if args.task == 'nli':
    templates = 'nli_templates.json'

with open(templates) as f:
    data = json.load(f)

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

contexts = []
for i in data :
    if args.task == 'qa':
        context = data[i]['context']
    elif args.task == 'nli':
        context = data[i]['premise'] + ' ' + data[i]['hypothesis']
    context = context.replace('<PERSON>', 'James')
    replace_words = find_words(context)

    for phrase in replace_words:
        word = phrase.replace('<', '').split('/')[0]
        context = context.replace(phrase, word)

    contexts.append(context)
        
    #pdb.set_trace()

len_matrix = len(data)
## create a matrix of size len_matrix x len_matrix
matrix_bertscore = []
for i in range(len_matrix):
    matrix_bertscore.append([0.]*len_matrix)

## compute bertscore for all combinations of contexts
for i in range(len_matrix):
    for j in range(i,len_matrix):
        results = bertscore.compute(predictions=[contexts[i]], references=[contexts[j]], model_type="bert-base-uncased")
        matrix_bertscore[i][j] = results['f1'][0]

start_time = time.time()
## save list in a txt file
output_file = 'matrix_bertscore_' + str(args.task) + '.txt'

with open(output_file, 'w') as f:
    for item in matrix_bertscore:
        f.write("%s\n" % item)
    f.close()

print ("Time taken to save matrix_bertscore.txt: ", time.time() - start_time)
print (matrix_bertscore)
