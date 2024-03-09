import os
import json
import csv
#from openai import OpenAI
import openai



openai.api_key = ''

def list_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def concatenate_json_files(json_files):
    concatenated_data = {}
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            problem = data.get("problem")
            if problem:
                concatenated_data[problem] = data.get("solution", "No solution provided")
    return concatenated_data

def search_by_problem(problem_query, concatenated_data):
    return concatenated_data.get(problem_query, "Problem not found")


directory_path = '/Users/corneliaweinzierl/Downloads/MATH/train'


json_files = list_json_files(directory_path)


concatenated_data = concatenate_json_files(json_files)



def is_semantically_similar_gpt4(text1, text2):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful Assistant. Your task is to check whether two texts are semantically equal. You are only allowed to answer with 'Yes' or 'No'. "},
                    {"role": "user", "content": f"Are the following two texts semantically equal?\n\nText 1: {text1}\n\nText 2: {text2}\n\nAnswer with 'Yes' or 'No'."}
                    ]
                    )
    
        response = completion.choices[0].message['content']
        print(response)
        return 1 if response.strip().lower() in ['yes', 'yes.'] else 0

    
    except Exception as e:
        print(f"Error during API call: {e}")
        return 0

    


def process_csv_matches(file_path):
    
    num_matches = 0
    #rows_processed = 0

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            
            row_content = row[0]
            
            parts = row_content.split('###')
            problem = None
            solution = None
            for part in parts:
                if part.startswith(' Human:'):
                    problem = part.replace(' Human:', '').strip().replace("Let's think step-by-step.", "").rstrip()
                elif part.startswith(' Assistant:'):
                    solution = part.replace(' Assistant:', '').strip()

            #print(problem)
            #print(solution)
            ground_truth = search_by_problem(problem, concatenated_data)
            #print(ground_truth)

            match = is_semantically_similar_gpt4(ground_truth, solution)

            num_matches += match
            #rows_processed += 1 
            #if rows_processed == 50:  
            #    break 

    return num_matches


            


file_path = '/Users/corneliaweinzierl/Desktop/Diversity/Untitled/datasets/output-140.csv'  # Update this to your actual CSV file path
matches = process_csv_matches(file_path)
number_of_datapoints = 140

print(f"Number of matches: {matches}")

accuracy = matches / number_of_datapoints

print(f"Accuracy: {accuracy}")
