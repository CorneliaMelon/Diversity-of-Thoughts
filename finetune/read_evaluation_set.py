import os
import json

# Define the path to your folder containing the JSON files
folder_path = '../data/val_set'

# Function to read JSON files and extract 'problem' and 'solution'
def read_json_files(folder_path):
    # List to store dictionaries
    data_list = []

    # Iterate through each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                # Load JSON data from the file
                json_data = json.load(file)
                # Extract 'problem' and 'solution' fields and store them in a dictionary
                problem_solution_dict = {'prompt': json_data['problem'], 'response': json_data['solution']}
                # Append the dictionary to the list
                data_list.append(problem_solution_dict)

    return data_list

# Read JSON files and format them into a list of dictionaries
formatted_data = read_json_files(folder_path)

# Print the list of dictionaries
print(formatted_data)
print(len(formatted_data))
