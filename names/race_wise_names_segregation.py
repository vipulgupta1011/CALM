''' 
This script will convert data from multiple races into a single csv file wil columns for each race. Each colhumn can be used in different kind of analysis based on requirements.
- Getting top 300 names for each race from usa ssa dataset. 
- We categorize names belonging to a race if the occurance in that race > 80%
'''

import json
import sys
import pdb
import pandas as pd

sys.path.append('..')

from utils import *

# Load the data
ssa_data = read_txt('source_data/ssa/yob2021.txt')
harvard_race = read_csv('source_data/harvard_dataverse/first_nameRaceProbs.csv')

names_race_mapping = {}

for line in range(1, len(harvard_race)) : 
    [name, white, black, hispanic, asian, others] = harvard_race[line]
    name = name.capitalize()
    if float(white) > 0.8 :
        names_race_mapping[name] =  'white'
    if float(black) > 0.8 :
        names_race_mapping[name] =  'black'
    if float(hispanic) > 0.8 :
        names_race_mapping[name] =  'hispanic'
    if float(asian) > 0.8 :
        names_race_mapping[name] =  'asian'

white_count, black_count, hispanic_count, asian_count, others_count = 0, 0, 0, 0, 0

race_dataset = {}

for i in range(30000) :
    ssa_data[i] = ssa_data[i].split(',')

    name = ssa_data[i][0].capitalize()

    if name in names_race_mapping :
        if names_race_mapping[name] == 'white' :
            white_count += 1
            if white_count < 300 :
                race_dataset[name] = 'white'
        if names_race_mapping[name] == 'black' :
            black_count += 1
            if black_count < 300 :
                race_dataset[name] = 'black'
        if names_race_mapping[name] == 'hispanic' :
            hispanic_count += 1
            if hispanic_count < 300 :
                race_dataset[name] = 'hispanic'
        if names_race_mapping[name] == 'asian' :
            asian_count += 1
            if asian_count < 300 :
                race_dataset[name] = 'asian'

names_segregation = {}

def scoring_gender(names_dict) :
    for name in names_dict : 
        if names_dict[name] == 'white' :
            if name not in names_segregation :
                names_segregation[name] = {}
            names_segregation[name]['usa.white'] = 1
        if names_dict[name] == 'black' :
            if name not in names_segregation :
                names_segregation[name] = {}
            names_segregation[name]['usa.black'] = 1
        if names_dict[name] == 'hispanic' :
            if name not in names_segregation :
                names_segregation[name] = {}
            names_segregation[name]['usa.hispanic'] = 1
        if names_dict[name] == 'asian' :
            if name not in names_segregation :
                names_segregation[name] = {}
            names_segregation[name]['usa.asian'] = 1


scoring_gender(race_dataset)
## Make it compact, this is ugly code :p
vals = ['usa.white', 'usa.black', 'usa.hispanic', 'usa.asian']
for name in names_segregation :
    for val in vals : 
        if val not in names_segregation[name] :
            names_segregation[name][val] = 0


names_list = list(names_segregation.keys())

data = {
        'Name' : names_list,
        'usa.white' : [names_segregation[name]['usa.white'] for name in names_list],
        'usa.black' : [names_segregation[name]['usa.black'] for name in names_list],
        'usa.hispanic' : [names_segregation[name]['usa.hispanic'] for name in names_list],
        'usa.asian' : [names_segregation[name]['usa.asian'] for name in names_list]}

df = pd.DataFrame(data)

df.to_csv('categorised_data/names_race_categorisation.csv', index=False)
