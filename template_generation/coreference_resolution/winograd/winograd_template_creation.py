
import json, os, csv
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from utils import *
import random
import argparse

def check_word_in_dictionary(string, dictionary) :
    words = string.split()
    for word in words :
        if word in dictionary :
            return True
    return False

def count_words_in_dictionary(string, dictionary) :
    count=0
    words = string.split()
    for word in words :
        if word in dictionary :
            count += 1
            #return True
    return count

file_path = os.path.join(os.path.dirname(__file__), '../../../', 'dataset/winograd/test.csv')

names_file_path = os.path.join(os.path.dirname(__file__), '../../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = read_csv(file_path)

names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0]] = {}

j=0
## write to a csv file

filtered_rows = []

for i in range(1, len(dataset)) :
    row = dataset[i]
    context = row[0]

    if check_word_in_dictionary(context, names_dict) : 
        filtered_rows.append(row)
        j += 1

write_csv(filtered_rows, 'winograd_filtered.csv')
print (j)
