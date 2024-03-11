import csv
import shutil
import json
import os 
import random

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




#json_directory = ''
#csv_file_path = '/Users/corneliaweinzierl/Desktop/Diversity/Untitled/output-2000-811-4-cleaned.csv'
#output_directory = '/Users/corneliaweinzierl/Downloads/MATH/filtered'
#process_and_filter_json_files(json_directory, csv_file_path, output_directory)


def sample_json_files(directory, csv_problems, max_files=70):
    total_subfolders = 7 
    max_files_per_subfolder = max_files // total_subfolders
    sampled_files = []

    subfolders = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    for subfolder in subfolders:
        subfolder_sampled_files = []  
        json_files = [os.path.join(subfolder, f) for f in os.listdir(subfolder) if f.endswith('.json')]
        
        while len(subfolder_sampled_files) < max_files_per_subfolder and json_files:
            file_path = random.choice(json_files)  
            json_files.remove(file_path)  
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if data.get("problem") not in csv_problems and data.get("level") == "Level 1":
                    subfolder_sampled_files.append(file_path)
            
            if len(sampled_files) + len(subfolder_sampled_files) == max_files:
                        
                break
        
        sampled_files.extend(subfolder_sampled_files)  
        
        if len(sampled_files) == max_files:  
            break

    return sampled_files



def copy_files_to_folder(files, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for file_path in files:
        shutil.copy(file_path, output_directory)


def main():
    csv_file_path = '/Users/corneliaweinzierl/Desktop/Diversity/Untitled/output-2000-811-4-cleaned.csv'
    json_directory = '/Users/corneliaweinzierl/Downloads/MATH/train'
    output_directory = '/Users/corneliaweinzierl/Desktop/Diversity/Untitled/datasets/filtered_eval_data_from_MATH/level_1_eval'
    
    csv_problems = get_problems_from_csv(csv_file_path)
    sampled_files = sample_json_files(json_directory, csv_problems)
    copy_files_to_folder(sampled_files, output_directory)
    
    print(f"Total files copied: {len(sampled_files)}")

if __name__ == "__main__":
    main()


