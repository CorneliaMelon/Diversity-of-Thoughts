import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def calculate_grouped_word_counts(csv_file_path):
    grouped_counts = defaultdict(list)
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)  # Chunking csv file here to group answers by 4 roles 
        
        
        for i in range(0, len(rows), 4):
            group = rows[i:i+4]  
            for row in group:
                parts = row[0].split("### Assistant:")
                if len(parts) > 1:
                    assistant_text = parts[1].strip()  
                    word_count = len(assistant_text.split())
                    grouped_counts[i // 4].append(word_count)
                else:
                    # handle rows without "### Assistant:"; here we add 0 to keep group sizes consistent
                    grouped_counts[i // 4].append(0)
    return grouped_counts

def plot_accumulated_histograms(grouped_counts):
    fig, axs = plt.subplots(7, 5, figsize=(20, 14), sharex=True, sharey=True)
    fig.suptitle('Accumulated Histograms of Output Instance Word Counts per question')
    
    for (group_idx, counts) in grouped_counts.items():
        ax = axs[group_idx // 5, group_idx % 5]  # Determine subplot position
        ax.hist(counts, bins=range(0, max(counts) + 2), alpha=0.75, edgecolor='black')
        ax.set_title(f'Group {group_idx+1}')
        ax.grid(True)
    
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect to make room for the global title
    plt.show()


csv_file_path = ''  
grouped_counts = calculate_grouped_word_counts(csv_file_path)
plot_accumulated_histograms(grouped_counts)