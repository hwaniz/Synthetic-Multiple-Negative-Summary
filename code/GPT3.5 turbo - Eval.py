import openai
import json
import sys
import os
import time
import ast

# api key
_api_key = '' # our api key
_client = openai.OpenAI(api_key=_api_key)
_model = "gpt-3.5-turbo" # specify your model name

hands_on_prompt = "You must STRICRLY follow the rules.\n\nSummarize in one paragraph. You MUST give at least 4 sentences in summary.\nThen gradually change the important factual meaning of that summary to weird meaning until 4 summaries generated. \n\nHallucinated summary must include following 6 types of errors.\nDefinition:\n1.Entity errors: a small part of a sentence, often an entity (e.g., age, numeric, location name, person name, time, object name, price), is incorrect (usually 1-3 words). Entity errors often involve noun phrases or nouns. \n2.Relational error: a sentence is partially incorrect as a small part (usually 1 - 3 words). Relational errors often involve verbs and are often the opposite of what it should be. \n3.Contradictory sentence error: a sentence where the entire sentence is contradicted by the given reference, meaning the sentence can be proven false due to a contradiction with information in the passage. \n4.Invented info error: these errors refer to entities that are not known or do not exist. This does not include fictional characters in books or movies. invented errors include phrases or sentences which have unknown entities or misleading information. \n5.Subjective sentence: an entire sentence or phrase that is subjective and cannot be verified, so it should not be included. \n6.Unverifiable sentence: a sentence where the whole sentence or phrase is unlikely to be factually grounded although it can be true, and the sentence cannot be confirmed nor denied using the reference given or internet search, it is often something personal or private and hence cannot be confirmed.\n\n Three level:\nhallucination level = low: Just a few infomation in the summarization paragraph should be changed to hallucinated summary. (almost summary and very few hallucination with small amount of errors)\nhallucination level = mid: There should be more hallucination than the hallucination level low summary. Half of the summary sentences should be changed to hallucinated summary. This summarization should be different with the previous ones. (summary and hallucinated summary together with reasonable amount of errors)\nhallucination level = high: Even more sentences should be hallucinated than the mid level summary. Most summary sentences should be changed to hallucinated summary.() \n\nThis summarization should be different with the previous ones. (almost hallucinated summary and a little bit of true information with large amount of errors) \n\nFinally, You MUST give ONLY ONE SENTENSE explanation of differences among 4 texts. \n\nYou should give {summary:, hallucinated_summary_low:, hallucinated_summary_mid:, hallucinated_summary_high:, explanation} in JSON format."

coherency_prmpt = """
You will be given one summary written for a news article.

Your task is to rate the summary on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:

Coherence (1-5) - the collective quality of all sentences. We align this dimension with the DUC quality question of structure and coherence whereby "the summary should be well-structured and well-organized. The summary should not just be a heap of related information, but should build from sentence to a coherent body of information about a topic."

Evaluation Steps:

1. Read the news article carefully and identify the main topic and key points.
2. Read the summary and compare it to the news article. Check if the summary covers the main topic and key points of the news article, and if it presents them in a clear and logical order.
3. Assign a score for coherence on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.

Example:

Source Text:

{{Document}}

Summary:

{{Summary}}

Evaluation Form (scores ONLY):

- Coherence:
"""

consistency_prompt  = """
You will be given a news article. You will then be given one summary written for this article.

Your task is to rate the summary on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.


Evaluation Criteria:

Consistency (1-5) - the factual alignment between the summary and the summarized source. A factually consistent summary contains only statements that are entailed by the source document. Annotators were also asked to penalize summaries that contained hallucinated facts. 

Evaluation Steps:

1. Read the news article carefully and identify the main facts and details it presents.
2. Read the summary and compare it to the article. Check if the summary contains any factual errors that are not supported by the article.
3. Assign a score for consistency based on the Evaluation Criteria.


Example:


Source Text: 

{{Document}}

Summary: 

{{Summary}}


Evaluation Form (scores ONLY):

- Consistency:
"""

fluency_prompt = """
You will be given one summary written for a news article.

Your task is to rate the summary on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.


Evaluation Criteria:

Fluency (1-3): the quality of the summary in terms of grammar, spelling, punctuation, word choice, and sentence structure.

- 1: Poor. The summary has many errors that make it hard to understand or sound unnatural.
- 2: Fair. The summary has some errors that affect the clarity or smoothness of the text, but the main points are still comprehensible.
- 3: Good. The summary has few or no errors and is easy to read and follow.


Example:

Summary:

{{Summary}}


Evaluation Form (scores ONLY):

- Fluency (1-3):
"""

relevence_prompt = """
You will be given one summary written for a news article.

Your task is to rate the summary on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:

Relevance (1-5) - selection of important content from the source. The summary should include only important information from the source document. Annotators were instructed to penalize summaries which contained redundancies and excess information.

Evaluation Steps:

1. Read the summary and the source document carefully.
2. Compare the summary to the source document and identify the main points of the article.
3. Assess how well the summary covers the main points of the article, and how much irrelevant or redundant information it contains.
4. Assign a relevance score from 1 to 5.


Example:


Source Text:

{{Document}}

Summary:

{{Summary}}


Evaluation Form (scores ONLY):

- Relevance:
"""



def get_response(client, prompt, model):

    response = client.chat.completions.create(
    model=model,
    # This is an example of chat completion.
    messages=[{"role": "user", "content": prompt}],
    max_tokens=600,
    top_p=1,
    temperature=0,
    frequency_penalty=0,
    presence_penalty=0,
    )
    text_response = response.choices[0].message.content

    return text_response


def main(input_path, output_path):

    # data load.
    inputs = []
    for line in open(input_path, 'r'):
        line = json.loads(line)
        inputs.append(line)

    # writer
    writer = open(output_path, 'w')

    for input_id, input_json in enumerate(inputs):
        # input json parsing example
        src = input_json['article']
        pred_summary = input_json['pred_summary']
        
        #sentences = input_json['sentences']
        for prompt_eval in [coherency_prmpt, consistency_prompt, fluency_prompt, relevence_prompt]:
            # prompt generation
            if prompt_eval != fluency_prompt:
                prompt = prompt_eval.replace('{Document}', src).replace('{Summary}', pred_summary)
                print("[PROMPT]:", prompt)
            
            else: 
                prompt = prompt_eval.replace('{Summary}', pred_summary)
                print("[PROMPT]:", prompt)
            
            try:
                time.sleep(3)

                _t = time.perf_counter()
                output = get_response(client=_client, prompt=prompt, model=_model)
                t = time.perf_counter() - _t

            except Exception as e:
                print(e)
                print("[error] detected!, stopped with input id", input_id)
                sys.exit(1)

            if prompt_eval == coherency_prmpt:
                input_json['coherency'] = parsing_llm_output(output) # raw output from llm
                print('[coherency]:', parsing_llm_output(output))
            
            if prompt_eval == consistency_prompt:
                input_json['consistency'] = parsing_llm_output(output) # raw output from llm
                print('[consistency]:', parsing_llm_output(output))
            
            if prompt_eval == fluency_prompt:
                input_json['fluency'] = parsing_llm_output(output) # raw output from llm
                print('[fluency]:', parsing_llm_output(output))
            
            if prompt_eval == relevence_prompt:
                input_json['relevence'] = parsing_llm_output(output) # raw output from llm
                print('[relevence]:', parsing_llm_output(output))
            
        input_json['model'] = 'gpt3.5-turbo'

        json.dump(input_json, writer)
        writer.write('\n')
        writer.flush()
    writer.close()


def parsing_llm_output(llm_output):
    number = ''.join(filter(str.isdigit, llm_output))
    if number == '':
        output = 'NaN'
    else:
        output = int(number)
    return output


if __name__ == "__main__":

    input_path = ''
    output_path = ''

    main(input_path, output_path)