import json, time
from evaluate import load
import pdb, re

bertscore = load("bertscore")

qa_templates = 'qa_templates.json'

with open(qa_templates) as f:
    qa_data = json.load(f)
#predictions = ["hello world", "general kenobi"]
#references = ["hello world", "general kenobi"]
#results = bertscore.compute(predictions=predictions, references=references, model_type="bert-base-uncased")
#print(results)
#sentences = ['he likes chocolates', 'he likes vanilla', 'he hates vanilla', 'this is stupid']
#results = bertscore.compute(predictions=[sentences[0]], references=[sentences[1]], model_type="bert-base-uncased")
#print(results)
#results = bertscore.compute(predictions=[sentences[0]], references=[sentences[2]], model_type="bert-base-uncased")
#print(results)
#results = bertscore.compute(predictions=[sentences[0]], references=[sentences[3]], model_type="bert-base-uncased")
#print(results)

#{'precision': [1.0, 1.0], 'recall': [1.0, 1.0], 'f1': [1.0, 1.0], 'hashcode': 'distilbert-base-uncased_L5_no-idf_version=0.3.10(hug_trans=4.10.3)'}


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
for i in qa_data :
    context = qa_data[i]['context']
    context = context.replace('<PERSON>', 'James')
    replace_words = find_words(context)

    for phrase in replace_words:
        word = phrase.replace('<', '').split('/')[0]
        context = context.replace(phrase, word)

    contexts.append(context)
        
    #pdb.set_trace()

len_matrix = len(qa_data)
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
with open('matrix_bertscore.txt', 'w') as f:
    for item in matrix_bertscore:
        f.write("%s\n" % item)
    f.close()
print ("Time taken to save matrix_bertscore.txt: ", time.time() - start_time)
print (matrix_bertscore)
