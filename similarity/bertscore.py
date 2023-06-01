from evaluate import load
bertscore = load("bertscore")
predictions = ["hello world", "general kenobi"]
references = ["hello world", "general kenobi"]
#results = bertscore.compute(predictions=predictions, references=references, model_type="distilbert-base-uncased")
#print(results)
sentences = ['he likes chocolates', 'he likes vanilla', 'he hates vanilla', 'this is stupid']
results = bertscore.compute(predictions=[sentences[0]], references=[sentences[1]], model_type="distilbert-base-uncased")
print(results)
results = bertscore.compute(predictions=[sentences[0]], references=[sentences[2]], model_type="distilbert-base-uncased")
print(results)
results = bertscore.compute(predictions=[sentences[0]], references=[sentences[3]], model_type="distilbert-base-uncased")
print(results)

#{'precision': [1.0, 1.0], 'recall': [1.0, 1.0], 'f1': [1.0, 1.0], 'hashcode': 'distilbert-base-uncased_L5_no-idf_version=0.3.10(hug_trans=4.10.3)'}
