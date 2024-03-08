import data_generation
import openai
import os
import json
import random
import csv



openai.api_key = ''

output_file_path = 'output-500-4-roles-extension.csv'

output_problem_path = 'problems-4-roles-extension.csv'



batch_size = 18

#QUERY = "A standard six-sided fair die is rolled four times. The probability that the product of all four numbers rolled is a perfect square is $\\tfrac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m+n$.\n" 
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/algebra'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/counting_and_probability'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/geometry'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/number_theory'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/prealgebra'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/precalculus'
#directory = '/Users/corneliaweinzierl/Downloads/MATH/train/intermediate_algebra'

ROLES = ["Mathematician", "Economist", "Lawyer", "Programmer"]



def process_random_files(directory, batch_size, output_problem_path):
    
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Randomly sample batch_size number of files
    if batch_size < len(json_files):
        sampled_files = random.sample(json_files, batch_size)
    else:
        sampled_files = json_files
    
    with open(output_problem_path, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        
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
    
def append_csv_files(source_csv_1, source_csv_2, destination_csv):
    with open(destination_csv, 'w', newline='', encoding='utf-8') as dest_file:
        csv_writer = csv.writer(dest_file)
        
        
        with open(source_csv_1, 'r', encoding='utf-8') as src_file1:
            csv_reader1 = csv.reader(src_file1)
            for row in csv_reader1:
                csv_writer.writerow(row)
        
        
        with open(source_csv_2, 'r', encoding='utf-8') as src_file2:
            csv_reader2 = csv.reader(src_file2)
            for row in csv_reader2:
                csv_writer.writerow(row)

source_csv_1 = 'output-1000-4-roles-extension.csv'
source_csv_2 = 'output-1000-4-roles.csv'
destination_csv = 'output-2000-4-roles.csv'

def main():
    #process_random_files(directory = directory, batch_size = batch_size, output_problem_path = output_problem_path)
    #data_generation.construct_training_data(QUERY, ROLES, data_generation.ROLE_MAP, openai, output_file_path)
    append_csv_files(source_csv_1, source_csv_2, destination_csv)

if __name__ == "__main__":
    main()

