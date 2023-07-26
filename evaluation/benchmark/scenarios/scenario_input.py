import os, json

def PassageQAInput(
        passage: str,
        question: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        return f"{passage_prefix}{passage}{separator}{question_prefix}{question}{separator}{answer_prefix}"

def PassageMCQAInput(
        passage: str,
        question: str,
        options: list,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        return f"{passage_prefix}{passage}{separator}{question_prefix}{question}{separator}{options}{answer_prefix}"

def PassageNLIInput(
        passage: str,
        hypothesis: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        question_suffix: str = " True, False, or Neither?",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        return f"{passage_prefix}{passage}{separator}{question_prefix}{hypothesis}{separator}{question_suffix}{separator}{answer_prefix}"

def PassageWNLIInput(
        passage: str,
        hypothesis: str,
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        question_suffix: str = " True or False?",
        answer_prefix: str = "Answer: ",
        separator: str = "\n",
    ):
        return f"{passage_prefix}{passage}{separator}{question_prefix}{hypothesis}{question_suffix}{separator}{answer_prefix}"

def PassageSentimentInput(
        passage: str,
        passage_prefix: str = "Passage: ",
        sentiment_prefix: str = "Sentiment: ",
        separator: str = " \n",
    ):
        return f"{passage_prefix}{passage}{separator}{sentiment_prefix}"

def PassageSentimentToxicInput(
        passage: str,
        question: str = 'Is the passage above toxic?',
        passage_prefix: str = "Passage: ",
        question_prefix: str = "Question: ",
        sentiment_prefix: str = "",
        separator: str = " \n",
    ):
        return f"{passage_prefix}{passage}{separator}{question_prefix}{question}{separator}{sentiment_prefix}"


