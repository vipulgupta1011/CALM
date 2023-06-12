''' 
This script will convert data from multiple countries into a single csv file wil columns for gender for each country. Each colhumn can be used in different kind of analysis based on requirements.

Datasets used to create below list : 
    1. Social security US data
    2. Office of National Statistics UK data
    3. Canada : British Columbia government statistics data
    4. Australia : Australia Attorney-General's Department

Filtering names :
    1. Taking top 1000 names for male and female for each country
    1. Associating gender with a name if percentage occurane in a gender >80%, else it is considered as unisex '''

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
canada_census_boys = json.load(open('source_data/canada/canada_boys_names_sorted.json'))
canada_census_girls = json.load(open('source_data/canada/canada_girls_names_sorted.json'))
australia_census_male = read_csv('source_data/australia/males_2017.csv', encoding='latin-1')
australia_census_female = read_csv('source_data/australia/females_2017.csv', encoding='latin-1')

ssa_dataset, uk_census_dataset, canada_census_dataset, australia_census_dataset = {}, {}, {}, {}
ssa_male_count, ssa_female_count = 0, 0
uk_male_count, uk_female_count = 0, 0
canada_male_count, canada_female_count = 0, 0
australia_male_count, australia_female_count = 0, 0

#convert ssa_data to dict
for i in range(len(ssa_data)):
    ssa_data[i] = ssa_data[i].split(',')
    freq = int(ssa_data[i][2])

    #if freq < 100 :
    #    continue

    gender = 'M' if ssa_data[i][1] == 'M' else 'F'

    if gender == 'M' :
        ssa_male_count += 1
        if ssa_male_count > 1000 :
            continue
    else :
        ssa_female_count += 1
        if ssa_female_count > 1000 :
            continue

    if ssa_data[i][0] not in ssa_dataset:
        ssa_dataset[ssa_data[i][0]] = {'M': 0, 'F': 0}

    ssa_dataset[ssa_data[i][0]][gender] = freq


#convert uk census data to dict

#First row is header so ignoring that
#for i in range(1,len(uk_census_boys)):
for i in range(1,1000):
    name, freq = uk_census_boys[i][1], int(uk_census_boys[i][2].replace(',',''))
    #if freq < 25 :
    #    break
    uk_census_dataset[name] = {'M': freq, 'F': 0}

#for i in range(1,len(uk_census_girls)):
for i in range(1,1000):
    name, freq = uk_census_girls[i][1], int(uk_census_girls[i][2].replace(',',''))
    #if freq < 25 :
    #    break
    if name not in uk_census_dataset :
        uk_census_dataset[name] = {'M': 0, 'F': freq}
    else :
        uk_census_dataset[name]['F'] = freq


#convert canada census data to dict
for name in canada_census_boys : 
    freq = int(canada_census_boys[name])
    name = name.capitalize()

    canada_census_dataset[name] = {'M': freq, 'F': 0}

    canada_male_count += 1
    if canada_male_count > 1000 :
        continue

for name in canada_census_girls : 
    freq = int(canada_census_girls[name])
    name = name.capitalize()

    if name not in canada_census_dataset :
        canada_census_dataset[name] = {'M': 0, 'F': freq}
    else :
        canada_census_dataset[name]['F'] = freq

    canada_female_count += 1
    if canada_female_count > 1000 :
        continue

#convert australia census data to dict

#First row is header so ignoring that
for i in range(1,1000):
    name, freq = australia_census_male[i][0].capitalize(), int(australia_census_male[i][1])
    if freq < 2 :
        break
    australia_census_dataset[name] = {'M': freq, 'F': 0}

#for i in range(1,len(australia_census_girls)):
for i in range(1,1000):
    name, freq = australia_census_female[i][0].capitalize(), int(australia_census_female[i][1])
    if freq < 2 :
        break
    if name not in australia_census_dataset :
        australia_census_dataset[name] = {'M': 0, 'F': freq}
    else :
        australia_census_dataset[name]['F'] = freq


names_segregation = {}

def scoring_gender(names_dict, key1, key2) :
    for name in names_dict : 
        m_freq, f_freq = names_dict[name]['M'], names_dict[name]['F']
        
        percent_m = m_freq/(m_freq+f_freq)

        if name not in names_segregation :
            names_segregation[name] = {}

        ## Giving full weightage to a gender if it is more than 90% of the total frequency
        if percent_m > 0.8 :
            names_segregation[name][key1], names_segregation[name][key2] = 1, 0
        elif percent_m < 0.2 :
            names_segregation[name][key1], names_segregation[name][key2] = 0, 1
        else :
            names_segregation[name][key1], names_segregation[name][key2] = 1, 1
    

scoring_gender(ssa_dataset, 'usa.male', 'usa.female')
scoring_gender(uk_census_dataset, 'uk.male', 'uk.female')
scoring_gender(canada_census_dataset, 'canada.male', 'canada.female')
scoring_gender(australia_census_dataset, 'australia.male', 'australia.female')

## Make it compact, this is ugly code :p
vals = ['usa.male', 'usa.female', 'uk.male', 'uk.female', 'canada.male', 'canada.female', 'australia.male', 'australia.female']
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
        'uk.female' : [names_segregation[name]['uk.female'] for name in names_list],
        'canada.male' : [names_segregation[name]['canada.male'] for name in names_list],
        'canada.female' : [names_segregation[name]['canada.female'] for name in names_list],
        'australia.male' : [names_segregation[name]['australia.male'] for name in names_list],
        'australia.female' : [names_segregation[name]['australia.female'] for name in names_list]}

df = pd.DataFrame(data)

df.to_csv('categorised_data/segregated_names.csv', index=False)
