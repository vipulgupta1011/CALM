## Evaluating LLMs

Scripts to evaluate different LLMs can be found in `evaluate_models` folder. The scripts are named as `evaluate_<model_name>.py`

To evaluate LLMs models, run the following command : 
```
python evaluate_models/evaluation_<LLM-family>.py --model <model-name>
```
For example, model-name for Llama-2 can be `meta-llama/Llama-2-7b-hf`, `meta-llama/Llama-2-13b-hf` or `meta-llama/Llama-2-70b-hf`

The command to test Llama-2-7b-hf model is : 
```
python evaluate_models/evaluation_llama.py --model meta-llama/Llama-2-7b-hf
```

The outputs of the model on the CALM dataset is stored in `results` folder


## Generating CALM bias scores

To get bias score for a LLM on the CALM dataset on a task, run the following command : 
```
cd scripts
python accuracy.py --model <model-name> --task <qa/nli/sentiment>
```

Run the above command for all three tasks individually and take average to get the final CALM score

To get a detailed analysis of bias scores per dataset and template, run the following command : 
```
cd scripts
python accuracy.py --model <model-name> --task <qa/nli/sentiment> --detailed
```

A sample working command is : 
```
cd scripts
python accuracy.py --model Llama-2-7b-hf --task qa
```

## Ground truth data

Ground truth for CALM dataset can be found in `gt` folder
