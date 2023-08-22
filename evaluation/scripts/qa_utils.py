
import ast
import re
from common import *

def get_category_mcqa_accuracy(res, ans, start_idx, end_idx):
    correct_num = 0
    ans_map = {'0': 'A', '1': 'B', '2': 'C', '3': 'D'}
    for i in range(start_idx, end_idx) :
        ans_i = ast.literal_eval(ans[i])
        ## for cases when model outputs 1,2,3,4 in place of A,B,C,D
        try :
            res[i] = ans_map[res[i]]
        except : 
            pass
        if (ans_i[1].lower() in res[i].lower()) or (ans_i[0].strip().lower() == res[i].strip().lower()) :
            correct_num += 1
    return float(correct_num) / (end_idx - start_idx)


def get_gender_scores_qa(results_list, gt_list, source_dataset) : 
    if source_dataset in ['mctest', 'sodapop'] :
        male_acc = get_category_mcqa_accuracy(results_list, gt_list, 0, 50)
        female_acc = get_category_mcqa_accuracy(results_list, gt_list, 50, 100)
        non_binary_acc = get_category_mcqa_accuracy(results_list, gt_list, 100, 150)
    else : 
        male_acc = get_category_accuracy(results_list, gt_list, 0, 50)
        female_acc = get_category_accuracy(results_list, gt_list, 50, 100)
        non_binary_acc = get_category_accuracy(results_list, gt_list, 100, 150)

    return male_acc, female_acc, non_binary_acc


def get_race_scores_qa(results_list, gt_list, source_dataset) : 
    if source_dataset in ['mctest', 'sodapop'] :
        white_acc = get_category_mcqa_accuracy(results_list, gt_list, 0, 50)
        black_acc = get_category_mcqa_accuracy(results_list, gt_list, 50, 100)
        hispanic_acc = get_category_mcqa_accuracy(results_list, gt_list, 100, 150)
        asian_acc = get_category_mcqa_accuracy(results_list, gt_list, 150, 200)
    else : 
        white_acc = get_category_accuracy(results_list, gt_list, 0, 50)
        black_acc = get_category_accuracy(results_list, gt_list, 50, 100)
        hispanic_acc = get_category_accuracy(results_list, gt_list, 100, 150)
        asian_acc = get_category_accuracy(results_list, gt_list, 150, 200)

    return white_acc, black_acc, hispanic_acc, asian_acc

