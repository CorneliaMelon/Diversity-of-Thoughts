import torch
import re
import accelerate
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
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

def get_prompt(query):
  chat = [
    {"role": "user", "content": f"You are provided with a mathematics problem. Write out your reasoning step-by-step and find the answer. The last line of the response should contain the answer. The problem is a follows.\n{query}"},
  ]
  return tokenizer.apply_chat_template(chat, tokenize=False)

def generate_model_answers(problems, gen_pipeline):
    results = []
    for question in problems:
        result = gen_pipeline(get_prompt(question))
        results.append({"content": result[0]['generated_text']})
    return results

MODEL_WEIGHTS_DIR = ''
device_map = {"": 0}

# Model name
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

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

# Load the model with quantization and device mapping
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config= bnb_config,  # Quantization configuration, you can change it according to your needs
    device_map=device_map
)

# Path to your fine-tuned weights
fine_tuned_weights_path = ""

# Load your fine-tuned weights
#model.load_state_dict(torch.load(fine_tuned_weights_path))

# Set the device to GPU if available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"

#Read EVALUATION_QUESTIONS.pkl to get questions
# Load the dataset dictionary from the pickle file
filename = 'EVALUATION_QUESTIONS.pkl'

with open(filename, 'rb') as f:
    data = pickle.load(f)


problems = [item["question"].removeprefix("b'").removesuffix("\\n'") for item in data]
solutions = [item["answer"].removeprefix("b'").removesuffix("\\n'") for item in data]

gen_pipeline = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=10000)
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


json_output_file_path = 'EVALUATION_RESULTS.json'
with open(json_output_file_path, 'w') as jsonfile:
    jsonfile.write(json_string)


print(json_string)

