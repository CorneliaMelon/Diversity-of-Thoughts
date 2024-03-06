import data_generation
import openai
import os
import json
import random
import csv



openai.api_key = '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'

output_file_path = 'output-new.csv'

output_problem_path = 'problems.csv'

#batch_size = 8
batch_size = 8

#QUERY = "A standard six-sided fair die is rolled four times. The probability that the product of all four numbers rolled is a perfect square is $\\tfrac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m+n$.\n" 
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/algebra'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/counting_and_probability'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/geometry'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/number_theory'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/prealgebra'
directory = '/Users/corneliaweinzierl/Downloads/MATH/train/precalculus'

ROLES = ["Mathematician", "Programmer", "Economist", "Lawyer"]
#need function that gives us the role description based off of the key 


def process_random_files(directory, batch_size, output_problem_path):
    # List all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Randomly sample batch_size number of files
    if batch_size < len(json_files):
        sampled_files = random.sample(json_files, batch_size)
    else:
        sampled_files = json_files
    
    with open(output_problem_path, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Check if the file is empty to decide whether to write the header
        csvfile.seek(0, os.SEEK_END)
        if csvfile.tell() == 0:
            csvwriter.writerow(['Problem'])
        
        
        for file in sampled_files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                problem = data.get("problem", "No problem found")
                data_generation.construct_training_data(problem, ROLES, data_generation.ROLE_MAP, openai, output_file_path)
                csvwriter.writerow([problem])
    


def main():
    process_random_files(directory = directory, batch_size = batch_size, output_problem_path = output_problem_path)
    #data_generation.construct_training_data(QUERY, ROLES, data_generation.ROLE_MAP, openai, output_file_path)



if __name__ == "__main__":
    main()

