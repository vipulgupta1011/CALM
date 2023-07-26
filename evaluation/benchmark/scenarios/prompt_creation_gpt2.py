import json
from .scenario_examples import *
from .scenario_input import *
import pdb


class PromptGenerator():
    def __init__(self, num_examples=5):
        self.in_context_examples = num_examples
        
        self.prompt_babi = prompt_generation_qa('babi', in_context_examples=num_examples)
        #self.prompt_duorc = prompt_generation_qa('duorc', in_context_examples=num_examples)
        self.prompt_duorc = prompt_generation_qa('duorc', in_context_examples=3)
        #self.prompt_mcscript = prompt_generation_qa('mcscript', in_context_examples=num_examples)
        self.prompt_mcscript = prompt_generation_qa('mcscript', in_context_examples=3)
        self.prompt_qamr = prompt_generation_qa('qamr', in_context_examples=num_examples)
        self.prompt_relation_extraction = prompt_generation_qa('relation_extraction', in_context_examples=num_examples)
        self.prompt_tweetqa = prompt_generation_qa('TweetQA', in_context_examples=num_examples)
        #self.prompt_mctest = prompt_generation_mcqa('mctest', in_context_examples=num_examples)
        self.prompt_mctest = prompt_generation_mcqa('mctest', in_context_examples=2)
        self.prompt_sodapop = prompt_generation_mcqa('sodapop', in_context_examples=num_examples)
        self.prompt_snli = prompt_generation_nli('SNLI', in_context_examples=num_examples)
        self.prompt_sick = prompt_generation_nli('sick', in_context_examples=num_examples)
        self.prompt_wnli = prompt_generation_wnli('wnli', in_context_examples=num_examples)
        self.prompt_rte = prompt_generation_wnli('RTE', in_context_examples=num_examples)
        self.prompt_sst = prompt_generation_sentiment('sst', in_context_examples=num_examples)
        self.prompt_sentiment140 = prompt_generation_sentiment('sst', in_context_examples=num_examples)
        self.prompt_eec = prompt_generation_sentiment('sst', in_context_examples=num_examples)
        self.prompt_toxic = prompt_generation_sentiment_toxic('toxic', in_context_examples=num_examples)


    def prepare_prompt(self, sample) :

        task_name = sample['source_dataset']
        #prompt = ''
        #if task_name not in ['mctest'] :
        #    return prompt
        if task_name in ['babi'] :
            prompt = self.prepare_prompt_babi(sample)

        if task_name in ['duorc'] :
            ## context window issue
            prompt = self.prepare_prompt_duorc(sample)

        if task_name in ['mcscript'] :
            ## context window issue
            prompt = self.prepare_prompt_mcscript(sample)

        if task_name in ['qamr'] :
            prompt = self.prepare_prompt_qamr(sample)

        if task_name in ['relation_extraction'] :
            prompt = self.prepare_prompt_relation_extraction(sample)

        if task_name in ['TweetQA'] :
            prompt = self.prepare_prompt_tweetqa(sample)

        if task_name in ['mctest'] :
            ## context window issue
            prompt = self.prepare_prompt_mctest(sample)

        if task_name in ['sodapop'] :
            prompt = self.prepare_prompt_sodapop(sample)

        if task_name in ['SNLI'] :
            prompt = self.prepare_prompt_snli(sample)

        if task_name in ['sick'] :
            prompt = self.prepare_prompt_sick(sample)

        if task_name in ['wnli'] :
            prompt = self.prepare_prompt_wnli(sample)

        if task_name in ['RTE'] :
            prompt = self.prepare_prompt_rte(sample)

        if task_name in ['SST'] :
            prompt = self.prepare_prompt_sst(sample)

        if task_name in ['Sentiment140'] :
            prompt = self.prepare_prompt_sentiment140(sample)

        if task_name in ['EEC'] :
            prompt = self.prepare_prompt_eec(sample)

        if task_name in ['Toxic'] :
            prompt = self.prepare_prompt_toxic(sample)

        return prompt



    def prepare_prompt_babi(self, sample) :
        prompt = self.prompt_babi + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_duorc(self, sample) :
        prompt = self.prompt_duorc + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_mcscript(self, sample) :
        prompt = self.prompt_mcscript + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_qamr(self, sample) :
        prompt = self.prompt_qamr + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_relation_extraction(self, sample) :
        prompt = self.prompt_relation_extraction + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_tweetqa(self, sample) :
        prompt = self.prompt_tweetqa + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_mctest(self, sample) :
        prompt = self.prompt_mctest + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt
        
    def prepare_prompt_sodapop(self, sample) :
        prompt = self.prompt_sodapop + PassageQAInput(passage=sample['context'], question=sample['question']) 
        return prompt

    def prepare_prompt_snli(self, sample) :
        prompt = self.prompt_snli + PassageNLIInput(passage=sample['premise'], hypothesis=sample['hypothesis']) 
        return prompt

    def prepare_prompt_sick(self, sample) :
        prompt = self.prompt_sick + PassageNLIInput(passage=sample['premise'], hypothesis=sample['hypothesis']) 
        return prompt

    def prepare_prompt_wnli(self, sample) :
        prompt = self.prompt_wnli + PassageWNLIInput(passage=sample['premise'], hypothesis=sample['hypothesis']) 
        return prompt

    def prepare_prompt_rte(self, sample) :
        prompt = self.prompt_rte + PassageWNLIInput(passage=sample['premise'], hypothesis=sample['hypothesis']) 
        return prompt

    def prepare_prompt_sst(self, sample) :
        prompt = self.prompt_sst + PassageSentimentInput(passage=sample['sentence']) 
        return prompt

    def prepare_prompt_sentiment140(self, sample) :
        prompt = self.prompt_sentiment140 + PassageSentimentInput(passage=sample['sentence']) 
        return prompt

    def prepare_prompt_eec(self, sample) :
        prompt = self.prompt_eec + PassageSentimentInput(passage=sample['sentence']) 
        return prompt

    def prepare_prompt_toxic(self, sample) :
        prompt = self.prompt_toxic + PassageSentimentToxicInput(passage=sample['sentence']) 
        return prompt
