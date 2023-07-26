from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
import string
from tqdm import tqdm
import pdb, os
import torch
import time 
from benchmark.scenarios.prompt_creation_gpt2 import PromptGenerator
import argparse
from transformers import StoppingCriteria, StoppingCriteriaList
import json
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore") 
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='EleutherAI/gpt-j-6B')
parser.add_argument('--num_examples', type=int, default=5)
parser.add_argument('--batch_size', type=int, default=10)

args = parser.parse_args()
#NAME_MODEL = "gpt2"  # gpt2 small
NAME_MODEL = args.model # gpt-j-6B
TOKENIZER_MAX_SEQ_LEN = 2048

BATCH_SIZE = args.batch_size  # Could be much bigger depending on your model and your GPU. To be tuned for speed performance

NUM_BEAMS = 3  # 1 for greedy decoding. To be tuned to optimize the accuracy
MAX_NEW_TOKENS = 10  # Increase for a task with long output

device = "cuda:0" if torch.cuda.is_available() else "cpu"

##Initializing in_context examples
prompt_generator = PromptGenerator(args.num_examples)

class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self, stops = [], encounters=1):
        super().__init__()
        self.stops = stops
        self.ENCOUNTERS = encounters

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        stop_count = 0
        for stop in self.stops:
            stop_count = (stop == input_ids[0]).sum().item()

        if stop_count >= self.ENCOUNTERS:
            return True
        return False


qa_gender_ds = load_dataset("vipulgupta/CALMB", "qa_gender", split='test')
qa_race_ds = load_dataset("vipulgupta/CALMB", "qa_race", split='test')
nli_gender_ds = load_dataset("vipulgupta/CALMB", "nli_gender", split='test')
nli_race_ds = load_dataset("vipulgupta/CALMB", "nli_race", split='test')
sentiment_gender_ds = load_dataset("vipulgupta/CALMB", "sentiment_gender", split='test')
sentiment_race_ds = load_dataset("vipulgupta/CALMB", "sentiment_race", split='test')

tokenizer = AutoTokenizer.from_pretrained(NAME_MODEL, truncation_side="left", use_fast=True)
tokenizer.padding_side = "left"
tokenizer.pad_token = tokenizer.eos_token  # Comment this unless there is a bug in the `generate` method

stop_words_ids = [
        tokenizer(stop_word, return_tensors='pt')['input_ids'].squeeze() for stop_word in ['\n']]

stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids, encounters=18)])

#stopping_criteria = StoppingCriteria(eos_token_id=10)

model = AutoModelForCausalLM.from_pretrained(NAME_MODEL, device_map='auto', torch_dtype=torch.float16)

def save_result(dataset, out_file, batch_size) :  
    all_generated_answers = []
    idx_batches = [list(range(idx, min(idx + batch_size, len(dataset)))) for idx in range(0, len(dataset), batch_size)]
    for idx_batch in tqdm(idx_batches):
        batch = dataset.select(idx_batch)
        texts = [prompt_generator.prepare_prompt(sample) for sample in batch]
        #if '' in texts:
        #    continue
        tokens = tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            max_length=TOKENIZER_MAX_SEQ_LEN,
            padding=True,
            add_special_tokens=False,
        ).to(device)
        ###
        generated_tokens_org = model.generate(
            **tokens,
            num_beams=NUM_BEAMS,
            #max_length=TOKENIZER_MAX_SEQ_LEN,
            #stopping_criteria=stopping_criteria,
            #end_sequence='\n',
            max_new_tokens=MAX_NEW_TOKENS,
            #ignore_warnings=True,
            #early_stopping=True
        )
        ###
        generated_tokens = generated_tokens_org[:, tokens.input_ids.shape[1]:]  # We truncate the original prompts from the generated texts
        generated_texts = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        #print ('output : ', generated_texts)
        all_generated_answers.append(generated_texts)

    ## convert list of list to list 
    all_generated_answers = [item for sublist in all_generated_answers for item in sublist]
    ## save list in text file 
    with open(out_file, 'w+') as f:
            json.dump(all_generated_answers,f,indent=4)


if not os.path.exists('results'):
    os.makedir('results')

file_name = args.model.split('/')[1]

save_result(qa_gender_ds,'results/' + file_name + '-qa_gender.json', int(BATCH_SIZE / 2))
save_result(qa_race_ds,'results/' + file_name + '-qa_race.json', int(BATCH_SIZE / 2))
save_result(nli_gender_ds,'results/' + file_name + '-nli_gender.json', BATCH_SIZE)
save_result(nli_race_ds,'results/' + file_name +  '-nli_race.json', BATCH_SIZE)
save_result(sentiment_gender_ds,'results/' + file_name +'-sentiment_gender.json', BATCH_SIZE)
save_result(sentiment_race_ds,'results/' + file_name  + '-sentiment_race.json', BATCH_SIZE)
