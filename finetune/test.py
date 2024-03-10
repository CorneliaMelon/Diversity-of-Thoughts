
import csv 


import json






def create_prompt(question, answer):
  instruction = "### Instruction:\nYou are provided with a mathematics problem. Write out your reasoning step-by-step and find the answer. The last line of the response should contain the answer. The problem is a follows.\n" + question
  response = "\n### Response:\n"+ answer
  full_prompt = ""
  full_prompt += instruction
  full_prompt += response
  #print(full_prompt)
  return full_prompt


'''def read_csv_to_dict(file_path):
    data_dict_list = []
    rows_processed = 0

    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            entry = row[0]
            # Splitting the entry based on the '###' separator
            segments = entry.split('###')
            if len(segments) == 3: #what does this mean?
                question = segments[1].strip().replace('Human:', '').strip()
                print(question)
                answer = segments[2].strip().replace('Assistant:', '').strip() 
                #print(answer)

                data_dict_list.append({'prompt': question, 'response': answer})

            rows_processed += 1 
            if rows_processed == 5:  
                break 
    return data_dict_list'''

def read_csv_to_dict(file_path):
    data_dict_list = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            entry = row[0]
            segments = entry.split('###')
            if len(segments) >= 3:
                question = segments[1].strip().replace('Human:', '').strip()
                answer = segments[2].strip().replace('Assistant:', '').strip() 
                full_prompt = create_prompt(question, answer)
                data_dict_list.append({'prompt': full_prompt})
    return data_dict_list

#Load finetuning dataset
file_path = '../output-2000-811-4-cleaned.csv'
data_dict_list = read_csv_to_dict(file_path)

#print(data_dict_list[:2])

for entry in data_dict_list[:2]:
    print(entry['prompt'])
    print()


#data_dict = {key: [d[key] for d in data_dict_list] for key in data_dict_list[0]}

#print(data_dict)
