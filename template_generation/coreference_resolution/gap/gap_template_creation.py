
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

file_path = os.path.join(os.path.dirname(__file__), '../../../', 'dataset/gap/test.csv')

names_file_path = os.path.join(os.path.dirname(__file__), '../../../', 'names/categorised_data/segregated_names.csv')

names_dataset = read_csv(names_file_path)
dataset = read_csv(file_path)

names_dict = {}

for row in names_dataset[1:] :
    names_dict[row[0]] = {}

## check if a string has a four digit number
def has_four_digit_number(string) :
    string = string.replace(',', '').replace('(', '').replace(')', '')
    words = string.split()
    for word in words :
        if word.isdigit() and len(word) == 4 :
            return True
    return False


j=0

filtered_rows = []

for i in range(1, len(dataset)) :
    row = dataset[i]
    context = row[1]

    if check_word_in_dictionary(context, names_dict) : 
        if has_four_digit_number(context) :
            continue
        if 'democrat' in context.lower() or 'republic' in context.lower() :
            continue
        filtered_rows.append(row)
        j += 1
        if i<100 :
            print (i)

write_csv(filtered_rows, 'gap_filtered.csv')
print (j)
print (len(dataset))
