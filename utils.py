import json
import csv
import pandas as pd
import json

''' Input = path of a text file
    Output = lines in form of a list '''
def read_txt(path) :
    with open(path) as f :
        lines = f.readlines()
    return lines


def save_json(out_path, save_dict, indent=4, encoding='utf-8') :
    with open(out_path, 'w+') as f :
        json.dump(save_dict, f, indent=indent, ensure_ascii=False)


''' Input  : path to xlsx file
    Output : dictionary with keys as sheet names with values as corresponding data
'''
def read_xlsx(inp_file) :
    dfs = pd.read_excel(inp_file, sheet_name=None)

    return dfs


''' Input  : path to csv file
    Output : list with entries as all rows of the csv where each entry is a list of columns
'''


def read_csv(inp_file, encoding='utf-8') :
    rows = []
    with open(inp_file, newline='', encoding=encoding) as csvfile:
        #csvreader = csv.reader(csvfile, quotechar='|', skipinitialspace=True)
        csvreader = csv.reader(csvfile, skipinitialspace=True)
        for row in csvreader:
            rows.append(row)

    return rows


'''
out_file = full path of csv file to be saved
dataset = list of lists of data to be saved in csv. Example : dataset -> data = [['Albania', 28748, 'AL', 'ALB'], ['Algeria', 2381741, 'DZ', 'DZA'], ['American Samoa', 199, 'AS', 'ASM']]
'''
def write_csv(dataset, out_file) :
    with open(out_file, 'w+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(dataset)



def read_tsv(file_path):
    data = []
    with open(file_path, 'r', newline='') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', newline='') as jsonl_file:
        for line in jsonl_file:
            data.append(json.loads(line))
    return data	
