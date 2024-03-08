import os
import json

def read_json_files(directory):
    data = []

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                json_data = json.load(file)
                question = json_data['problem']
                answer = json_data['solution']
                data.append({'question': question, 'answer': answer})

    return data


