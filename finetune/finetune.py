from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import csv 
from datasets import Dataset
from peft import LoraConfig, PeftModel
#get_peft_model, prepare_model_for_kbit_training
from transformers import TrainingArguments
from trl import SFTTrainer
import os
import json

#Model parameters
model_id_tokenizer = "NousResearch/Nous-Hermes-llama-2-7b"
model_id = "NousResearch/Nous-Hermes-llama-2-7b"

#Quantization
# Activate 4-bit precision base model loading
use_4bit = True
# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16"
# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4"
# Activate nested quantization for 4-bit base models (double quantization)
use_nested_quant = False

compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
)
device_map = {"": 0}
# Load the model with quantization and device mapping
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config= bnb_config,  # Quantization configuration, you can change it according to your needs
    device_map=device_map,
    #temperature = 0
)

#Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id_tokenizer)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


def create_prompt(question, answer):
  instruction = "### Instruction:\nYou are provided with a mathematics problem. Write out your reasoning step-by-step and find the answer. The last line of the response should contain the answer. The problem is a follows.\n" + question
  response = "\n### Response:\n"+ answer
  full_prompt = ""
  full_prompt += instruction
  full_prompt += response
  #print(full_prompt)
  return full_prompt


# def tokenize_prompts(prompt):
#    return tokenizer(create_prompt(prompt))

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
                question = segments[1].strip().replace('Human:', '').strip() # add blank space
                print(question)
                answer = segments[2].strip().replace('Assistant:', '').strip() # add blank space
                print(answer)
                data_dict_list.append({'prompt': question, 'response': answer})

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

dataset = Dataset.from_dict({'prompt': [d['prompt'] for d in data_dict_list]})


# Convert the list of dictionaries to a dictionary of lists
#data_dict = {key: [d[key] for d in data_dict_list] for key in data_dict_list[0]}
# Create a dataset
#dataset = Dataset.from_dict(data_dict)
#Tokenize the dataset
#tokenized_train_dataset = dataset.map(tokenize_prompts)

#Load validation dataset
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
                #problem_solution_dict = {'prompt': json_data['problem'], 'response': json_data['solution']}
                # Append the dictionary to the list
                full_prompt = create_prompt(json_data['problem'], json_data['solution'])
                #data_list.append(problem_solution_dict)
                data_dict_list.append({'prompt': full_prompt})
    return data_list

val_path = '../data/val_set'
val_dict_list = read_json_files(val_path)
#val_dict = {key: [d[key] for d in val_dict_list] for key in val_dict_list[0]}
# Create a dataset
#val_dataset = Dataset.from_dict(val_dict)
#Tokenize the dataset
#val_tokenized_train_dataset = val_dataset.map(tokenize_prompts)
val_dataset = Dataset.from_dict({'prompt': [d['prompt'] for d in val_dict_list]})

#PEFT configurations
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
        target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "lm_head",
    ],
    task_type="CAUSAL_LM"
)
#print(model)
#model = prepare_model_for_kbit_training(model)
#model = get_peft_model(model, peft_config)

#Training arguments
args = TrainingArguments(
  output_dir = "exp_1_epoch_2000_4_roles/checkpoints",
  num_train_epochs=1,
  #max_steps = 300, # comment out this line if you want to train in epochs
  per_device_train_batch_size = 4,
  per_device_eval_batch_size = 4,
  gradient_accumulation_steps=1,
  gradient_checkpointing=True,
  optim = "paged_adamw_32bit",
  #warmup_steps = 0.03,
  save_strategy="steps",
  save_steps = 20,
  logging_steps= 10,
  #evaluation_strategy="epoch",
  evaluation_strategy="steps",
  eval_steps=10, # comment out this line if you want to evaluate at the end of each epoch
  #learning_rate=2.5e-5,
  learning_rate=2e-4,
  weight_decay = 0.001,
  bf16=False,
  fp16 = False,
  #bf16=True,
  #tf32=True,
  max_grad_norm=0.3,
  warmup_ratio=0.03,
  group_by_length = True,
  lr_scheduler_type='cosine',
  max_steps =-1,
  #disable_tqdm=True,
  report_to = "tensorboard"
)

#We choose this value based on the distribution of the custom dataset we generated
#max_seq_length = 1500
max_seq_length = 0 

trainer = SFTTrainer(
    model=model,
    args=args,
    train_dataset=dataset,
    eval_dataset=val_dataset,
    peft_config=peft_config,
    dataset_text_field='prompt',
    max_seq_length=max_seq_length,
    tokenizer=tokenizer,
    packing=True,
)
  
  

#formatting_func=create_prompt, this will aplly the create_prompt mapping to all training and test dataset

#Start training -> need to dump loss values into a file so that we can plot
trainer.train()


#model = model.merge_and_unload()

#print(model)
# Save trained model
trainer.model.save_pretrained("final_model")
#model.save_pretrained("final_model")



