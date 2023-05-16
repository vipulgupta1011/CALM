''' 
This script will convert data from multiple countries into a single csv file wil columns for gender for each country. Each colhumn can be used in different kind of analysis based on requirements.

Datasets used to create below list : 
    1. Social security US data
    2. Office of National Statistics UK data

Filtering names :
    1. Names with atleast 100 frequency in social security names '''

import json
import sys
import pdb
import pandas as pd

sys.path.append('..')

from utils import *

# Load the data
ssa_data = read_txt('source_data/ssa/yob2021.txt')
uk_census_girls = read_csv('source_data/uk_census/2021girlsnames.csv')
uk_census_boys = read_csv('source_data/uk_census/2021boysnames.csv')

ssa_dataset, uk_census_dataset = {}, {}

#convert ssa_data to dict
for i in range(len(ssa_data)):
    ssa_data[i] = ssa_data[i].split(',')
    freq = int(ssa_data[i][2])

    if freq < 100 :
        continue

    gender = 'M' if ssa_data[i][1] == 'M' else 'F'

    if ssa_data[i][0] not in ssa_dataset:
        ssa_dataset[ssa_data[i][0]] = {'M': 0, 'F': 0}

    ssa_dataset[ssa_data[i][0]][gender] = freq


#convert uk census data to dict

#First row is header so ignoring that
for i in range(1,len(uk_census_boys)):
    name, freq = uk_census_boys[i][1], int(uk_census_boys[i][2].replace(',',''))
    if freq < 25 :
        break
    uk_census_dataset[name] = {'M': freq, 'F': 0}

for i in range(1,len(uk_census_girls)):
    name, freq = uk_census_girls[i][1], int(uk_census_girls[i][2].replace(',',''))
    if freq < 25 :
        break
    if name not in uk_census_dataset :
        uk_census_dataset[name] = {'M': 0, 'F': freq}
    else :
        uk_census_dataset[name]['F'] = freq



names_segregation = {}

def scoring_gender(names_dict, key1, key2) :
    for name in names_dict : 
        m_freq, f_freq = names_dict[name]['M'], names_dict[name]['F']
        
        percent_m = m_freq/(m_freq+f_freq)

        if name not in names_segregation :
            names_segregation[name] = {}

        ## Giving full weightage to a gender if it is more than 90% of the total frequency
        if percent_m > 0.9 :
            names_segregation[name][key1], names_segregation[name][key2] = 1, 0
        elif percent_m < 0.1 :
            names_segregation[name][key1], names_segregation[name][key2] = 0, 1
        else :
            names_segregation[name][key1], names_segregation[name][key2] = 1, 1
    

scoring_gender(ssa_dataset, 'usa.male', 'usa.female')
scoring_gender(uk_census_dataset, 'uk.male', 'uk.female')

## Make it compact, this is ugly code :p
vals = ['usa.male', 'usa.female', 'uk.male', 'uk.female']
for name in names_segregation :
    for val in vals : 
        if val not in names_segregation[name] :
            names_segregation[name][val] = 0


names_list = list(names_segregation.keys())

data = {
        'Name' : names_list,
        'usa.male' : [names_segregation[name]['usa.male'] for name in names_list],
        'usa.female' : [names_segregation[name]['usa.female'] for name in names_list],
        'uk.male' : [names_segregation[name]['uk.male'] for name in names_list],
        'uk.female' : [names_segregation[name]['uk.female'] for name in names_list] }

df = pd.DataFrame(data)

df.to_csv('categorised_data/segregated_names.csv', index=False)
