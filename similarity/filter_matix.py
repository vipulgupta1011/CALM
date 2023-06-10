import json, pdb
import re
import random

## read txt file line by line
def read_txt_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

## read json file
def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

matrix_bertscore = read_txt_file('matrix_bertscore.txt')
matrix_bertscore = [line.strip() for line in matrix_bertscore]

qa_templates = read_json_file('qa_templates.json')

remove_indexes = []

k=0
for i in range(len(matrix_bertscore)):
    ## remove '[]' from string
    matrix = re.sub(r'\[|\]', '', matrix_bertscore[i])
    ## split string by ','
    bertscores = matrix.split(',')

    for j in range(i+1, len(bertscores)):
        if i == j :
            continue
        bertscore_i_j = float(bertscores[j].strip())
        if bertscore_i_j > 0.9:
            if i in remove_indexes or j in remove_indexes:
                continue
            if random.random() > 0.5:
                remove_indexes.append(i)
            else :
                remove_indexes.append(j)
            k += 1
            print('Matching templates : ', i , '  :   ', j , '  :  ', bertscore_i_j)

    #pdb.set_trace()

print (remove_indexes)
print (len(remove_indexes))
print(k)

for remove_index in remove_indexes:
    qa_templates.pop(str(remove_index))

## save json file
with open('qa_templates_filtered.json', 'w+') as f:
    json.dump(qa_templates, f, indent=4)
