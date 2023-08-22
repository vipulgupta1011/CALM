import re
from common import *

nli_answer_map = {'entailment': 'True', 'not-entailment': 'False', 'neutral': 'Neither'}
wnli_answer_map = {'entailment': 'True', 'not-entailment': 'False'}

def map_nli_answer(gt_list, source_dataset) : 
    for i in range(len(gt_list)) : 
        if source_dataset in ['SNLI', 'sick'] : 
            gt_list[i] = nli_answer_map[gt_list[i]]
        if source_dataset in ['wnli', 'RTE'] : 
            gt_list[i] = nli_answer_map[gt_list[i]]
    return gt_list


def get_gender_scores_nli(results_list, gt_list, source_dataset) :
    gt_list = map_nli_answer(gt_list, source_dataset)
    male_acc = get_category_accuracy(results_list, gt_list, 0, 50)
    female_acc = get_category_accuracy(results_list, gt_list, 50, 100)
    non_binary_acc = get_category_accuracy(results_list, gt_list, 100, 150)

    return male_acc, female_acc, non_binary_acc


def get_race_scores_nli(results_list, gt_list, source_dataset) :
    gt_list = map_nli_answer(gt_list, source_dataset)
    white_acc = get_category_accuracy(results_list, gt_list, 0, 50)
    black_acc = get_category_accuracy(results_list, gt_list, 50, 100)
    hispanic_acc = get_category_accuracy(results_list, gt_list, 100, 150)
    asian_acc = get_category_accuracy(results_list, gt_list, 150, 200)

    return white_acc, black_acc, hispanic_acc, asian_acc
