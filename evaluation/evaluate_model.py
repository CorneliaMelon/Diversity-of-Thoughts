import json
import openai
import re
import time




openai.api_key = ''

def compare(model_answer, ground_truth):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful Assistant. Your task is to check whether two texts are semantically equal. You are only allowed to answer with 'Yes' or 'No'. "},
                    {"role": "user", "content": f"Are the following two texts semantically equal?\n\nText 1: {model_answer}\n\nText 2: {ground_truth}\n\nAnswer with 'Yes' or 'No'."}
                    ]
                    )
    
        response = completion.choices[0].message['content']
        print(response)
        return 1 if response.strip().lower() in ['yes', 'yes.'] else 0

    
    except Exception as e:
        print(f"Error during API call: {e}")
        return 0
    

def extract_after_response(text):
    
    #match = re.search(r'### Response:\s*(.*)', text, re.DOTALL)
    #if match:
        #print(match)
        #return match.group(1).strip()  
    #return "" 

    parts = text.split('### Response:')
    response = parts[1].strip() if len(parts) > 1 else ''
    #print(response)
    return response






def read_and_compare_json(file_path):
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    
    num_matches = 0
    rows_processed = 0

    for _, content in data.items():
        full_model_answer = content[0][0][0].get('content', '')  
        model_answer = extract_after_response(full_model_answer)  # Only the part after '### Response:' is being used
        ground_truth = content[1]

        
        if compare(model_answer, ground_truth):
            num_matches += 1
        
        rows_processed += 1
        if rows_processed % 50 == 0:
                print(f"Processed {rows_processed} rows, pausing for 60 seconds.")
                time.sleep(60)  

    print(f"Total matches: {num_matches}")
    accuracy = num_matches / 140
    print(f"Accuracy: {accuracy}")


json_file_path = '/Users/corneliaweinzierl/Downloads/exp_800_2r_cleaned.json'
comparison_results = read_and_compare_json(json_file_path)


