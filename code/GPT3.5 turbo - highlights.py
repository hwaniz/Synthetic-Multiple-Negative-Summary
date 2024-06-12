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

hands_on_prompt = "You must STRICRLY follow the rules.\n\nChange this summary to hallucinated summary in one paragraph. You MUST give at least 4 sentences in hallucinated summary.\nThen gradually change the important factual meaning of that summary to weird meaning until 4 summaries generated. \n\nHallucinated summary must include following 6 types of errors.\nDefinition:\n1.Entity errors: a small part of a sentence, often an entity (e.g., age, numeric, location name, person name, time, object name, price), is incorrect (usually 1-3 words). Entity errors often involve noun phrases or nouns. \n2.Relational error: a sentence is partially incorrect as a small part (usually 1 - 3 words). Relational errors often involve verbs and are often the opposite of what it should be. \n3.Contradictory sentence error: a sentence where the entire sentence is contradicted by the given reference, meaning the sentence can be proven false due to a contradiction with information in the passage. \n4.Invented info error: these errors refer to entities that are not known or do not exist. This does not include fictional characters in books or movies. invented errors include phrases or sentences which have unknown entities or misleading information. \n5.Subjective sentence: an entire sentence or phrase that is subjective and cannot be verified, so it should not be included. \n6.Unverifiable sentence: a sentence where the whole sentence or phrase is unlikely to be factually grounded although it can be true, and the sentence cannot be confirmed nor denied using the reference given or internet search, it is often something personal or private and hence cannot be confirmed.\n\n Three level:\nhallucination level = low: Just a few infomation in the summarization paragraph should be changed to hallucinated summary. (almost summary and very few hallucination with small amount of errors)\nhallucination level = mid: There should be more hallucination than the hallucination level low summary. Half of the summary sentences should be changed to hallucinated summary. This summarization should be different with the previous ones. (summary and hallucinated summary together with reasonable amount of errors)\nhallucination level = high: Even more sentences should be hallucinated than the mid level summary. Most summary sentences should be changed to hallucinated summary.() \n\nThis summarization should be different with the previous ones. (almost hallucinated summary and a little bit of true information with large amount of errors) \n\nFinally, You MUST give ONLY ONE SENTENSE explanation of differences among 4 texts. \n\nYou should give {hallucinated_summary_low:, hallucinated_summary_mid:, hallucinated_summary_high:, explanation} in JSON format."

def get_response(client, prompt, model):

    response = client.chat.completions.create(
    model=model,
    # This is an example of chat completion.
    messages=[{"role": "user", "content": prompt}],
    max_tokens=600,
    top_p=1,
    temperature=1,
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
        src = input_json['highlights']
        #sentences = input_json['sentences']

        # prompt generation
        prompt = hands_on_prompt + '\n\n' + src
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


        input_json['llm_output'] = [output] # raw output from llm
        
        try:
            input_json['parsed_output'] = parsing_llm_output(output) # parsed output
        
        except Exception as e:
            input_json['parsed_output'] = "" # parsed output
            print(e)
            print("ERROR! Stopped with input id", input_id)
            pass

        #input_json['llm_summary'] = input_json['parsed_output']['summary']
        #input_json['hallucinated_summary_high'] = input_json['parsed_output']['hallucinated_summary_high']
        #input_json['hallucinated_summary_mid'] = input_json['parsed_output']['hallucinated_summary_mid']
        #input_json['hallucinated_summary_low'] = input_json['parsed_output']['hallucinated_summary_low']
        #input_json['differences'] = input_json['parsed_output']['differences']
        input_json['model'] = 'gpt3.5-turbo'

        print('[LLM OUTPUT]:', input_json['llm_output'])
        #print('[PRED]:', input_json['parsed_output'])
        #print(input_json['parsed_output']['summary'])
        #print(input_json['parsed_output']['hallucinated_summary_high'])
        #print(input_json['parsed_output']['hallucinated_summary_mid'])
        #print(input_json['parsed_output']['hallucinated_summary_low'])
        #print(input_json['parsed_output']['differences'])
        json.dump(input_json, writer)
        writer.write('\n')
        writer.flush()
    writer.close()


def get_prompt(input, prompt):
    #### write our prompt template here
    return None # need to change


def parsing_llm_output(llm_output):
    start_idx = llm_output.find('[')
    if start_idx != -1:

        end_idx = llm_output.rfind(']')
        evaluation_output = llm_output[start_idx:end_idx+1]
        evaluation_output = evaluation_output.replace('\n  ','').replace('\n','')
        evaluation_output_json = json.loads(evaluation_output)

    else:
        start_idx = llm_output.find('{')
        end_idx = llm_output.rfind('}')
        evaluation_output = llm_output[start_idx:end_idx+1]
        evaluation_output = evaluation_output.replace('\n  ','').replace('\n','')
        evaluation_output_json = json.loads(evaluation_output)

    return evaluation_output_json    
    #return None # need to change


if __name__ == "__main__":

    input_path = ''
    output_path = ''
    main(input_path, output_path)