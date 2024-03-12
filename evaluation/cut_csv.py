import csv

def extract_first_n_questions(input_file_path, output_file_path, n=70):
    """
    Extracts the first n questions from a CSV file and stores them in a different CSV file.
    
    :param input_file_path: Path to the input CSV file.
    :param output_file_path: Path to the output CSV file where the first n questions will be stored.
    :param n: Number of questions to extract.
    """
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file, \
         open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
        
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        
        # Assuming the first row is the header
        header = next(reader)
        writer.writerow(header)
        
        # Write the first n rows to the output file
        for i, row in enumerate(reader):
            if i < n:
                writer.writerow(row)
            else:
                break

# Example usage
# Replace 'path_to_input.csv' and 'path_to_output.csv' with your actual file paths.
# extract_first_n_questions('path_to_input.csv', 'path_to_output.csv', 70)

extract_first_n_questions('/Users/corneliaweinzierl/Desktop/Diversity/Untitled/evaluation/312-2-roles-cleaned.csv', '70-2-roles-evals-cleaned.csv')
