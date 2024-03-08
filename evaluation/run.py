import torch
import re
import accelerate
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)
import pickle
import random
import json
import csv 
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, PeftModel
import os
import read_json as rj
from tqdm import tqdm



def generate_model_answers(problems, gen_pipeline):
    results = []
    for question in tqdm(problems):
        result = gen_pipeline(question)
        results.append({"content": result[0]['generated_text']})
    return results

MODEL_WEIGHTS_DIR = '../finetune/exp1_400epochs/checkpoint-240'

#Model parameters
model_id_tokenizer = "NousResearch/Nous-Hermes-llama-2-7b"
model_id = "NousResearch/Nous-Hermes-llama-2-7b"

#Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id_tokenizer)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

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

# Reload model in FP16 and merge it with LoRA weights
base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map,
)

# Path to your fine-tuned weights
fine_tuned_weights_path = '../finetune/exp1_400epochs/checkpoints/checkpoint-240/'

#Load finetuned weights
model = PeftModel.from_pretrained(base_model, fine_tuned_weights_path)
model = model.merge_and_unload()

# Set the device to GPU if available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

#Read test json files into a list called data
# Directory containing JSON files
test_directory = '../data/test_set/'
# Read JSON files and convert to list of dictionaries
data = rj.read_json_files(test_directory)

def create_prompt(sample):
  instruction = "### Instruction:\nYou are provided with a mathematics problem. Write out your reasoning step-by-step and find the answer. The last line of the response should contain the answer. The problem is a follows.\n" + sample
  response = "\n### Response:\n"
  full_prompt = ""
  full_prompt += instruction
  full_prompt += response
  return full_prompt

problems = [create_prompt(item["question"]) for item in data]
solutions = [item["answer"] for item in data]

print(problems)
print(solutions)

gen_pipeline = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=4000)
model_answers = generate_model_answers(problems, gen_pipeline)


json_structure = {}
for index, problem in enumerate(problems):
    question_id = problem
    ground_truth = solutions[index]
    model_answer = model_answers[index]
    print(model_answer)
    json_structure[question_id] = [
        [[model_answer]],
         ground_truth
    ]

json_string = json.dumps(json_structure, indent=4)


json_output_file_path = 'exp1_400epochs_eval_results.json'
with open(json_output_file_path, 'w') as jsonfile:
    jsonfile.write(json_string)


print(json_string)

