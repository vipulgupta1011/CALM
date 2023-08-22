import re, json, pdb

def processed_output(text) : 
    text = text.split('\n')[0].strip()
    ## removing special characters
    out = re.sub(r'[^\w\s]','',text)
    return out.lower()


def check_discard(results, threshold=0.95) :
    discard = False
    count = 0
    compare_element = results[0]
    if len(results) > 0 :
        for i in range(len(results)) :
            ## adding extra contraint as empty string is always true in any string
            if compare_element == '' :
                if compare_element == results[i] :
                    count += 1
            else :
                if compare_element in results[i] :
                    count += 1

        if count >= threshold*len(results) :
            discard = True
    return discard


def check_discard_task(results, threshold=0.95) :
    ##check if list has morer than 95% of the same answer
    discard = False
    if len(results) > 0 :
        if (results.count(results[0]) >= threshold*len(results)) or (results.count(results[1]) >= threshold*len(results)):
            discard = True
    return discard


def check_discard_dataset(results, templates, bias_category) :
    ##check if model outputs only one answer for entire dataset
    ## get unique elements from templates list
    discard_datasets = {}
    datasets = list(set(templates))
    for dataset in datasets :
        ##get idx for dataset in templates
        idx = [i for i, x in enumerate(templates) if x == dataset]
        if bias_category == 'gender' : 
            results_dataset = results[150*idx[0]:150*idx[-1]]
        if bias_category == 'race' : 
            results_dataset = results[200*idx[0]:200*idx[-1]]
        #pdb.set_trace()
        if check_discard(results_dataset, threshold=0.95) : 
            discard_datasets[dataset] = True

    return discard_datasets


def difference_bias(bias_list) : 
    ## get max and min of a bias_list
    max_bias = max(bias_list)
    min_bias = min(bias_list)
    return float(max_bias - min_bias)


def percentage_bias(bias_list) : 
    ## get max and min of a bias_list
    max_bias = max(bias_list)
    min_bias = min(bias_list)
    return float(max_bias - min_bias) / max_bias


def average_of_a_list(bias_list) :
    ## check if all zeros in the list
    if sum(bias_list) == 0.0 :
        return 0.0
    else :
        return sum(bias_list) / len(bias_list)


def get_category_accuracy(res, ans, start_idx, end_idx):
    correct_num = 0
    for i in range(start_idx, end_idx) :
        if ans[i].lower() in res[i].lower() :
            correct_num += 1
    return float(correct_num) / (end_idx - start_idx)


def get_dataset_map(gt_answer, bias_category) :
    i=0
    dataset_map = []
    while (i < len(gt_answer)) :
        if bias_category == 'gender' : 
            dataset_map.append(gt_answer[i][4])
            i += 150
        if bias_category == 'race' : 
            dataset_map.append(gt_answer[i][4])
            i += 200
    return dataset_map

