import json

input_path = ''

inputs = []
for line in open(input_path, 'r'):
    line = json.loads(line)
    inputs.append(line)
    
sum_coherency_score = 0
sum_consistency_score = 0
sum_fluency_score = 0
sum_relevence_score = 0

count_coherency = 0
count_consistency = 0
count_fluency = 0
count_relevence = 0

for input_id, input_json in enumerate(inputs):
    # input json parsing example
    coherency_score = input_json['coherency']
    consistency_score = input_json['consistency']
    fluency_score = input_json['fluency']
    relevence_score = input_json['relevence']
     
    if isinstance(coherency_score, int) and 1<=coherency_score<=5:
        count_coherency += 1
    else:
        coherency_score = 0
        print(input_id, 'coherency error')    

    if isinstance(consistency_score, int) and 1<=consistency_score<=5:
        count_consistency += 1
    else:
        consistency_score = 0
        print(input_id, 'consistency error')

    if isinstance(fluency_score, int) and 1<=fluency_score<=3:
        count_fluency += 1
    else:
        fluency_score = 0
        print(input_id, 'fluency error')
    
    if isinstance(relevence_score, int) and 1<=relevence_score<=5: 
        count_relevence += 1
    else:
        relevence_score = 0
        print(input_id, 'relevence error')

    sum_coherency_score += coherency_score
    sum_consistency_score += consistency_score
    sum_fluency_score += fluency_score
    sum_relevence_score += relevence_score
    
print('[AVG coherency]:', sum_coherency_score/count_coherency, '[COUNT coherency]:', count_coherency)
print('[AVG consistency]:', sum_consistency_score/count_consistency, '[COUNT consistency]:', count_consistency)
print('[AVG fluency]:', sum_fluency_score/count_fluency, '[COUNT fluency]:', count_fluency)
print('[AVG relevence]:', sum_relevence_score/count_relevence, '[COUNT relevence]:', count_relevence)