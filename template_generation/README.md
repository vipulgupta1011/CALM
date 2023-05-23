bABI (generated raw data using first 10000 lines for each task) : 
  - First level filtering 
    1.  Take examples with atleast 20 words in context
    2.  With a probability of 1/200 select if an example needs to be considered for template
  - Second level filtering
    1. Filtering to remove similar templates. Have one template per unique answer for each task

Tasks not including from babi :
    1. Task 2, Task 3 : question does not contain enough info to measure gender bias
    2. Task 4, 19 : contains only info about location and direction, no person data
    3. Task 5 : Too many names in the context
    4. Task 7 : counting objects
    5. Task 15 : contains animal information
    6. Task 16 : contains animal and color information
    7. Task 17,18 : No person data
    8. Task 20 : Answer not present in context

