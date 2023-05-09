''' Datasets used to create below list : 
    1. Social security US data
    2. Open source government data from US, UK, Canada and Australia 

Filtering names :
    1. Names with atleast 100 frequency in social security names or 5k frequency in open source government data
'''

import json
import sys
import pdb

sys.path.append('..')

from utils import *

# Load the data
ssa_data = read_txt('source_data/ssa/yob2021.txt')
multiple_countries = read_csv('source_data/multiple_countries/name_gender_dataset.csv')

ssa_dataset = {}
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


multiple_countries_dataset = {}
#convert multiple_countries to dict
for i in range(1,len(multiple_countries)):
    freq = int(multiple_countries[i][2])

    ## Pick names with atleast 5k frequency
    if freq < 5000 :
        break

    gender = 'M' if multiple_countries[i][1] == 'M' else 'F'

    if multiple_countries[i][0] not in multiple_countries_dataset:
        multiple_countries_dataset[multiple_countries[i][0]] = {'M': 0, 'F': 0}

    multiple_countries_dataset[multiple_countries[i][0]][gender] = freq


males, females = {}, {}

def selecting_gender(names_dict) :
    t=0
    for name in names_dict : 
        m_freq, f_freq = names_dict[name]['M'], names_dict[name]['F']
        
        percent_m = m_freq/(m_freq+f_freq)

        if percent_m < 1.0 and percent_m > 0.0 :
            t +=1

        if percent_m > 0.8 :
            males[name] = percent_m
        elif percent_m < 0.2 :
            females[name] = 1-percent_m
    print (t)

## Selecting gender from ssa dataset
selecting_gender(ssa_dataset)

## Selecting gender from multiple countries dataset
selecting_gender(multiple_countries_dataset)

save_json('categorised_data/males.json', males) 
save_json('categorised_data/females.json', females) 



