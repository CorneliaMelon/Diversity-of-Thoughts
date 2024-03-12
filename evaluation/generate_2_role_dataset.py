import csv 


def delete_third_and_fourth_rows(input_csv_path, output_csv_path):
    """
    Reads a CSV file, deletes every third and fourth row, and writes the remaining rows to a new CSV file.
    
    :param input_csv_path: Path to the input CSV file.
    :param output_csv_path: Path to the output CSV file where the result will be saved.
    """
    
    
    
    rows_to_keep = []
    
    
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader, start=1):
            
            if i % 4 != 0 and (i + 1) % 4 != 0:
                rows_to_keep.append(row)
                
    
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows_to_keep)


delete_third_and_fourth_rows('/Users/corneliaweinzierl/Desktop/Diversity/Untitled/datasets/finetuning_datasets/output-2000-4-roles.csv', '2000-4-roles-to-2-roles.csv')
