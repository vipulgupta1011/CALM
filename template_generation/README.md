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
