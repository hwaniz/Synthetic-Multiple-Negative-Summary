import json
import numpy as np

input_path_1 = ''
input_path_2 = ''
input_path_3 = ''

inputs_1 = []
for line in open(input_path_1, 'r'):
    line = json.loads(line)
    inputs_1.append(line)

inputs_2 = []
for line in open(input_path_2, 'r'):
    line = json.loads(line)
    inputs_2.append(line)

inputs_3 = []
for line in open(input_path_3, 'r'):
    line = json.loads(line)
    inputs_3.append(line)


list_sum_score_1 = []
list_sum_score_2 = []
list_sum_score_3 = []

for inputs in [inputs_1, inputs_2, inputs_3]:
    for input_id, input_json in enumerate(inputs):
        # input json parsing example
        coherency_score = input_json['coherency']
        consistency_score = input_json['consistency']
        relevence_score = input_json['relevence']

        if inputs == inputs_1:
            list_sum_score_1.append(coherency_score + consistency_score + relevence_score)

        if inputs == inputs_2:
            list_sum_score_2.append(coherency_score + consistency_score + relevence_score)
        
        if inputs == inputs_3:
            list_sum_score_3.append(coherency_score + consistency_score + relevence_score)
        
result = np.array(list_sum_score_1) + np.array(list_sum_score_2) - 2*np.array(list_sum_score_3)
dict_result =  dict(zip(result.argsort(), np.sort(result)))
print(dict_result)