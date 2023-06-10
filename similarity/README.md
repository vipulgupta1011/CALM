Bertscore is computed between reference sentence and a testing sentence. We modify it and compute bertscore between all pair of templates and save it in text file and then read this text file to filter templates.

We can combine these 2 files into one easily. Currently kept seperate as computing bertscore is computationally time consuming.

File to compute bertscore between templates. Input to this file is a json file with templates (eg. qa\_temaplates.json) : 
```
python bertscore.py
```

The above command will save bertscores in a text file.

Logic to compare bertscore and filter templates :
- Check if bertscore between a pair is >0.9
- If trure then we randomly remove one of these templates from the dataset

Command to remove templates with high bertscore similarity
```
python filter_matix.py
```

