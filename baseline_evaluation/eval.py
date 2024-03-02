import json
import os
import numpy as np
import time
import re
import sys
from util import delete_extra_zero,_strip_string, is_equiv, extract_math_answer

#RES_JSON_DIR = sys.argv[1]
#FILTER = sys.argv[2]

def parse_bullets(sentence):
    bullets_preprocess = sentence.split("\n")
    bullets = []

    for bullet in bullets_preprocess:
        try:
            idx = bullet.find(next(filter(str.isalpha, bullet)))
        except:
            continue

        bullet = bullet[idx:]

        if len(bullet) != 0:
            bullets.append(bullet)

    return bullets


def parse_yes_no(string):
    """
    Parses a string containing "yes" or "no" and returns a boolean value.

    Args:
        string (str): The string to parse.

    Returns:
        bool: True if the string contains "yes", False if the string contains "no".

    Raises:
        ValueError: If the input string does not contain "yes" or "no".
    """
    if "yes" in string.lower():
        return True
    elif "no" in string.lower():
        return False
    else:
        return None


def solve_math_problems(input_str):
    pattern = r"\d+\.?\d*"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1]

    return None

def compute_accuracy(gt, pred_solutions):
    pred_answers = []

    for pred_solution in pred_solutions:
        pred_answer = extract_math_answer(pred_solution)
        pred_answers.append(pred_answer)
    pred_answer = most_frequent(pred_answers)
    # pred_answer = pred_answers[0]

    try:
        is_correct = is_equiv(gt, pred_answer)
    except:
        is_correct = False
    if is_correct:
        return 1
    else:
        return 0


def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        current_frequency = sum(is_equiv(i, item) for item in List)
        if current_frequency > counter:
            counter = current_frequency
            num = i

    return num

def parse_resp(file):
    with open(file, "r") as f:
        lines = f.readlines()
    
    return sum([int(line.strip()) for line in lines])

def sum_tokens(text):
    """
    Parse the given text and sum up the usage of prompt tokens and completion tokens.

    Args:
    - text (str): The input text containing token usage.

    Returns:
    - tuple: A tuple containing the total prompt tokens and total completion tokens.
    """
    total_prompt_tokens = 0
    total_completion_tokens = 0

    # Split the text into lines and iterate over each line
    for line in text.strip().split('\n'):
        # Extract the numbers using string manipulation
        prompt_tokens = int(line.split('Prompt tokens: ')[1].split(',')[0])
        completion_tokens = int(line.split('Completion tokens: ')[1])

        # Add the extracted numbers to the total counts
        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens

    return total_prompt_tokens, total_completion_tokens

def run_evaluations(RES_JSON_DIR, FILTER='None'):
    accuracies = []
    details = {'algebra_': [], 'counting_': [], 
               'geometry_': [], 'intermediate_algebra_': [],
               'number_': [], 'prealgebra_': [], 'precalculus_': [], }

    for file in os.listdir(RES_JSON_DIR):
        if FILTER != 'None' and FILTER not in file:
            continue

        if not file.endswith(".json"):
            continue

        with open(os.path.join(RES_JSON_DIR, file), "r") as f:
            response_dict = json.load(f)
        
        for question, (responses, gt) in response_dict.items():
            pred_solutions = [response[-1]['content'] for response in responses if len(response) == max(len(response) for response in responses)]

            accurate = compute_accuracy(gt, pred_solutions)
            if accurate is not None:
                accuracies.append(float(accurate))
                for key in details.keys():
                    if file.startswith(key):
                        details[key].append(float(accurate))
                        break

    # Prepare and return the summary of results
    results_summary = {
        "total_evaluations": len(accuracies),
        "overall_accuracy": np.mean(accuracies) if accuracies else 0,
        "accuracy_std_error": np.std(accuracies) / np.sqrt(len(accuracies)) if accuracies else 0,
    }

    # Add category-specific accuracies and their standard errors
    for key, accuracies in details.items():
        if accuracies:
            results_summary[f"{key}accuracy"] = np.mean(accuracies)
            results_summary[f"{key}std_error"] = np.std(accuracies) / np.sqrt(len(accuracies))
        else:
            results_summary[f"{key}accuracy"] = 0
            results_summary[f"{key}std_error"] = 0

    return results_summary