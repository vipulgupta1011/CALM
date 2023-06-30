from datasets import load_dataset
from transformers import GPT2LMHeadModel, AutoTokenizer
import string
from tqdm import tqdm


NAME_MODEL = "gpt2"  # gpt2 small
TOKENIZER_MAX_SEQ_LEN = 1024

BATCH_SIZE = 64  # Could be much bigger depending on your model and your GPU. To be tuned for speed performance

NUM_BEAMS = 3  # 1 for greedy decoding. To be tuned to optimize the accuracy
MAX_NEW_TOKENS = 10  # Increase for a task with long output


def prepare_prompt_example(example):
    context = example["context"]
    question = example["question"]
    prompt = f"Context: {context} Question: {question} Answer: "  # To be tuned to optimize the accuracy
    return prompt


def process_answers(text):
    text = text.lower()
    text = text.strip(string.punctuation + string.whitespace + "\xa0")
    # Potentially add heuristics to increase the accuracy, like taking the first word of the answer helps for gpt2 small
    # text = text.split(" ")[0]
    return text


ds = load_dataset("HugoLaurencon/bias_dataset_beta", split="train")

tokenizer = AutoTokenizer.from_pretrained(NAME_MODEL, truncation_side="left", use_fast=True)
tokenizer.padding_side = "left"
tokenizer.pad_token = tokenizer.eos_token  # Comment this unless there is a bug in the `generate` method

model = GPT2LMHeadModel.from_pretrained(NAME_MODEL)

all_generated_answers = []
idx_batches = [list(range(idx, min(idx + BATCH_SIZE, len(ds)))) for idx in range(0, len(ds), BATCH_SIZE)]

for idx_batch in tqdm(idx_batches):
    ###
    batch = ds.select(idx_batch)
    texts = [prepare_prompt_example(example) for example in batch]
    tokens = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        max_length=TOKENIZER_MAX_SEQ_LEN,
        padding=True,
        add_special_tokens=False,
    )
    ###
    generated_tokens = model.generate(
        **tokens,
        num_beams=NUM_BEAMS,
        max_new_tokens=MAX_NEW_TOKENS,
    )
    ###
    generated_tokens = generated_tokens[:, tokens.input_ids.shape[1]:]  # We truncate the original prompts from the generated texts
    generated_texts = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    all_generated_answers.append(generated_texts)

all_generated_answers = [answer for batch in all_generated_answers for answer in batch]
all_correct_answers = ds["answer"]

all_generated_answers_processed = [process_answers(answer) for answer in all_generated_answers]
all_correct_answers_processed = [process_answers(answer) for answer in all_correct_answers]

accuracy = [
    (generated_answer == correct_answer) * 1
    for generated_answer, correct_answer in zip(all_generated_answers_processed, all_correct_answers_processed)
]
accuracy = sum(accuracy) / len(accuracy)

print(f"Accuracy for model {NAME_MODEL}: {accuracy}")
