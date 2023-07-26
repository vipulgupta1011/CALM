import sys
import os, pdb
import csv


nli_answer_map = {'entailment': 'True', 'not-entailment': 'False', 'neutral': 'Neither'}
wnli_answer_map = {'entailment': 'True', 'not-entailment': 'False'}

##read csv file
def read_csv(inp_file, encoding='utf-8') :
    rows = []
    with open(inp_file, newline='', encoding=encoding) as csvfile:
        #csvreader = csv.reader(csvfile, quotechar='|', skipinitialspace=True)
        csvreader = csv.reader(csvfile, skipinitialspace=True)
        for row in csvreader:
            rows.append(row)

    return rows


def get_file_path(task_name) : 
    return os.path.join(os.path.dirname(__file__), '../' , 'incontext_examples/', str(task_name) + '_examples.csv')


def create_options_string(options_list) :
    options_string = ''
    character = 'A'
    for option in options_list :
        options_string += character + ': ' + option + '\n'
        character = chr(ord(character)+1)
    return options_string


def prompt_generation_qa(task_name, in_context_examples) :
    file_path = get_file_path(task_name)

    examples = read_csv(file_path)
    j = 0
    prompt = ''
    for i in range(1, len(examples)) :
        if j == in_context_examples :
            return prompt
        j += 1
        example = examples[i]
        prompt += PassageQAExample(passage=example[0], question=example[1], answer=example[2])
        
    # in case of less examples than in-context examples required
    return prompt


def prompt_generation_mcqa(task_name, in_context_examples) :
    file_path = get_file_path(task_name)

    examples = read_csv(file_path)
    j = 0
    prompt = ''
    for i in range(1, len(examples)) :
        if j == in_context_examples :
            return prompt
        j += 1
        example = examples[i]
        answer = example[-1]
        answer_options = create_options_string(example[2:-1])
        prompt += PassageMCQAExample(passage=example[0], question=example[1], options=answer_options, answer=example[-1])
        
    # in case of less examples than in-context examples required
    return prompt


def prompt_generation_nli(task_name, in_context_examples) :
    file_path = get_file_path(task_name)

    examples = read_csv(file_path)
    j = 0
    prompt = ''
    for i in range(1, len(examples)) :
        if j == in_context_examples :
            return prompt
        j += 1
        example = examples[i]
        prompt += PassageNLIExample(passage=example[0], hypothesis=example[1],answer=nli_answer_map[example[2]])
        
    # in case of less examples than in-context examples required
    return prompt


def prompt_generation_wnli(task_name, in_context_examples) :
    file_path = get_file_path(task_name)

    examples = read_csv(file_path)
    j = 0
    prompt = ''
    for i in range(1, len(examples)) :
        if j == in_context_examples :
            return prompt
        j += 1
        example = examples[i]
        prompt += PassageWNLIExample(passage=example[0], hypothesis=example[1],answer=wnli_answer_map[example[2]])
        
    # in case of less examples than in-context examples required
    return prompt


def prompt_generation_sentiment(task_name, in_context_examples) :
    file_path = get_file_path(task_name)

    examples = read_csv(file_path)
    j = 0
    prompt = ''
    for i in range(1, len(examples)) :
        if j == in_context_examples :
            return prompt
        j += 1
        example = examples[i]
        prompt += PassageSentimentExample(passage=example[0], sentiment=example[1])
        
    # in case of less examples than in-context examples required
    return prompt


def prompt_generation_sentiment_toxic(task_name, in_context_examples) :
    file_path = get_file_path(task_name)

    examples = read_csv(file_path)
    j = 0
    prompt = ''
    for i in range(1, len(examples)) :
        if j == in_context_examples :
            return prompt
        j += 1
        example = examples[i]
        prompt += PassageSentimentToxicExample(passage=example[0], answer=example[1])
        
    # in case of less examples than in-context examples required
    return prompt


def PassageQAExample(
        passage: str,
        question: str,
        answer: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        """
        Passage-question pair used for in-context question answering scenarios.

        Using examples from train data for each dataset

        This is how the prompt will look like : 

        Passage: Mary journeyed to the office. John journeyed to the garden.
        Question: Where is Mary?
        Answer: office
        """
        return f"{passage_prefix}{passage}{separator}{question_prefix}{question}{separator}{answer_prefix}{answer}{separator}"


def PassageMCQAExample(
        passage: str,
        question: str,
        options: list,
        answer: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        """
        Passage-question pair used for in-context question answering scenarios.

        Using examples from train data for each dataset

        This is how the prompt will look like :

        Passage: Once there was a girl named Ruth, who loved to play outside whenever she could. One day, she was running around outside 
        with a friend, but she tripped and scraped her knee very badly. She doubled over in pain, screaming for her father 'DADDY!!!' she 
        yelled, until he ran outside to help. 'Thank goodness that only the skin on your knee was hurt!' he said, as he picked her up to 
        bring her inside. 'We need to cover your cut, and it looks like it was about to start raining anyway,' he said. He brought her into
        the restroom, so he could wash the cut, then put on medicine and a large bandage. 'That medicine hurt...' Ruth said, but her cut wash 
        feeling better than it did before. 'Well, at least now you don't have to worry about it getting worse,' her father said. 'Hopefully
        it won't take long for your cut to get better, then you can go back to playing outside again - be careful from now on!'
        Question: How did Ruth's father treat the cut?
        A: He used medicine
        B: He cleaned it with medicine and put on a bandage.
        C: He put on a bandage
        D: He told her to ignore the cut
        Answer: B
        """
        return f"{passage_prefix}{passage}{separator}{question_prefix}{question}{separator}{options}{answer_prefix}{answer}{separator}"


def PassageNLIExample(
        passage: str,
        hypothesis: str,
        answer: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        question_suffix: str = " True, False, or Neither?",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        """
        Passage-sentiment pair used for in-context sentiment analysis scenarios.

        Using examples from train data for each dataset

        This is how the prompt will look like :
        Passage: A person on a horse jumps over a broken down airplane.
        Question: A person is training his horse for a competition. True, False, or Neither?
        Answer: Neither
        """
        return f"{passage_prefix}{passage}{separator}{question_prefix}{hypothesis}{separator}{question_suffix}{separator}{answer_prefix}{answer}{separator}"


def PassageWNLIExample(
        passage: str,
        hypothesis: str,
        answer: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        question_suffix: str = " True or False?",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        """
        Passage-sentiment pair used for in-context sentiment analysis scenarios.

        Using examples from train data for each dataset

        This is how the prompt will look like :
        Passage: I stuck a pin through a carrot. When I pulled the pin out, it had a hole.
        Question: The carrot had a hole. True or False?
        Answer: True
        """
        return f"{passage_prefix}{passage}{separator}{question_prefix}{hypothesis}{question_suffix}{separator}{answer_prefix}{answer}{separator}"


def PassageSentimentExample(
        passage: str,
        sentiment: str,
        passage_prefix: str = "Passage: ",
        sentiment_prefix: str = "Sentiment: ",
        separator: str = "\n",
    ):
        """
        Passage-sentiment pair used for in-context sentiment analysis scenarios.

        Using examples from train data for each dataset

        This is how the prompt will look like : 
        Yet the act is still charming here.
        Sentiment: positive
        """
        return f"{passage_prefix}{passage}{separator}{sentiment_prefix}{sentiment}{separator}"


def PassageSentimentToxicExample(
        passage: str,
        answer: str,
        question: str = 'Is the passage above toxic?',
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        sentiment_prefix: str = "",
        separator: str = "\n",
    ):
        """
        Passage-sentiment pair used for in-context sentiment analysis scenarios.

        Using examples from train data for each dataset

        This is how the prompt will look like :
        You, sir, are my hero. Any chance you remember what page that's on?
        Question: Is the passage above toxic?
        False

        """
        return f"{passage_prefix}{passage}{separator}{question_prefix}{question}{separator}{sentiment_prefix}{answer}{separator}"


