import csv
import shutil
import json
import os 

def list_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def get_problems_from_csv(file_path):
    problems = set() 
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row_content = row[0]
            parts = row_content.split('###')
            for part in parts:
                if part.startswith(' Human:'):
                    problem = part.replace(' Human:', '').strip().replace("Let's think step-by-step.", "").rstrip()
                    problems.add(problem)
    return problems


def process_and_filter_json_files(json_directory, csv_file_path, output_directory):
    
    csv_problems = get_problems_from_csv(csv_file_path)
    
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    
    json_files = list_json_files(json_directory)
    
    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            problem = data.get("problem")
            
            if problem not in csv_problems:
                
                shutil.copy(file_path, output_directory)

# Example usage
json_directory = ''
csv_file_path = '/Users/corneliaweinzierl/Desktop/Diversity/Untitled/output-2000-811-4-cleaned.csv'
output_directory = '/Users/corneliaweinzierl/Downloads/MATH/filtered'
process_and_filter_json_files(json_directory, csv_file_path, output_directory)
