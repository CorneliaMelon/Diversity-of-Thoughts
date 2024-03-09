import csv
import matplotlib.pyplot as plt

def calculate_assistant_word_counts(csv_file_path):
    word_counts = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            parts = row[0].split("### Assistant:")
            if len(parts) > 1:
                assistant_text = parts[1]
                word_count = len(assistant_text.split())
                word_counts.append(word_count)
            else:
                # If "###Assistant:" is not found, add a count of 0 or skip
                word_counts.append(0)
    return word_counts

def plot_histogram(word_counts):
    plt.figure(figsize=(10, 6))
    plt.hist(word_counts, bins=20, alpha=0.75, edgecolor='black')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.title('Histogram of Word Counts in Output Instances')
    plt.grid(True)
    plt.show()


csv_file_path = ''  
word_counts = calculate_assistant_word_counts(csv_file_path)


plot_histogram(word_counts)
