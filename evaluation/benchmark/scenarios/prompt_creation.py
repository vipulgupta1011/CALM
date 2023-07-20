import json
from scenario import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--task_name', type=str, default='babi')

args = parser.parse_args()

task_name = args.task_name

if task_name in ['babi', 'duorc', 'mcscript', 'qamr', 'relation_extraction', 'tweetqa'] :
    prompt = prompt_generation_qa(task_name)

if task_name in ['mctest', 'sodapop'] :
    prompt = prompt_generation_mcqa(task_name)

if task_name in ['sst', 'Sentiment140 Train', 'EEC'] :
    ## These all have same structure
    prompt = prompt_generation_sentiment('sst')

if task_name in ['toxic'] : 
    prompt = prompt_generation_sentiment_toxic(task_name)

if task_name in ['SNLI', 'sick'] : 
    prompt = prompt_generation_nli(task_name)

if task_name in ['wnli','RTE'] : 
    prompt = prompt_generation_wnli(task_name)
print (prompt)

