## bABI (generated raw data using first 10000 lines for each task) : 
  - First level filtering 
    1.  Take examples with atleast 20 words in context
    2.  With a probability of 1/200 select if an example needs to be considered for template
  - Second level filtering
    1. Filtering to remove similar templates. Have one template per unique answer for each task

Tasks not including from babi :
- Task 2, Task 3 : question does not contain enough info to measure gender bias
- Task 4, 19 : contains only info about location and direction, no person data
- Task 5 : Too many names in the context
- Task 7 : counting objects
- Task 15 : contains animal information
- Task 16 : contains animal and color information
- Task 17,18 : No person data
- Task 20 : Answer not present in context



## QAMR (using only test data) : 
- Take context with atleast one person name in it
- Remove contexts which contains factual data like President Barack Obama and Noble Prize in 1958 etc.

## MCTest
Using mc500 test as it is a better version and is more grammatically correct
- Remove templates where person names were used for entities like animals, cars, 
- Remove templates with multiple person names mentioned in the question
- Select example for a template with a probability 1/5

## DuoRC
Using SelfRC test as it focuses only on Wikipedia movie plots
- Remove examples with context greater than 400, to avoid testing issue with models which have context length of 512
- Remove examples with no mention of names
- Select example for a template with a probability 1/10
- Remove examples with special characters, animal name references for names, long word answers, multiple person names in questions and answers
- Removed factual examples

## DROP
FOUND NO EXAMPLES WHICH CAN BE USED AS TEMPLATES
Using drop dev dataset as test data is not publicly available
- Remove examples with context greater than 400, to avoid testing issue with models which have context length of 512
- Remove examples with no mention of names
- Filter examples with summary of football matches
- Select example for a template with a probability 1/5

## Zero-Shot Relation Extraction
Using test.0 data
- Take context with atleast one person name in it
- Take examples with person name in question
- Take examples is they belong to one of the 2 types : occupation or medical condition. Other ttype questions are not suitable for measuring bias. Some are factual based
- Select example for a template with a probability 1/10
- Removed examples with multiple answers possible 

## MCScript
Using only test data
- Using examples with atleast one person name in context
- Using examples with mention of a person name in question or answer
- Select example for a template with a probability 1/2

## TweetQA
Using dev set as test answers are not available
- Using examples with atleast one person name in context
- Using examples with mention of a person name in question or answer
- Select example for a template with a probability 1/10
- Filtering factual examples

## SODAPOP
Using Bethany dataset file provided by authors
- Select example for a template with a probability 1/10
