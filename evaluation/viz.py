import matplotlib.pyplot as plt
import json

# Load the trainer state log
file_path = '/Users/corneliaweinzierl/Desktop/Diversity/Untitled/evaluation/trainer_state 800-2-roles.json'

with open(file_path, 'r') as file:
    data = json.load(file)

# Extract log history
log_history = data["log_history"]

# Initialize lists for epochs, training loss, and evaluation loss
epochs = []
training_loss = []
eval_loss = []

# Extract data from log history
for entry in log_history:
    if "loss" in entry:
        epochs.append(entry["epoch"])
        training_loss.append(entry["loss"])
    if "eval_loss" in entry:
        eval_loss.append(entry["eval_loss"])

# Ensure eval_loss list is aligned with training_loss list in length
# This step is necessary because training loss is recorded more frequently than evaluation loss
aligned_eval_loss = [None] * len(training_loss)
eval_steps = len(training_loss) // len(eval_loss)
aligned_eval_loss[::eval_steps] = eval_loss

# Plotting the losses
plt.figure(figsize=(10, 6))
plt.plot(epochs, training_loss, label='Training Loss')
plt.plot(epochs, aligned_eval_loss, label='Evaluation Loss', linestyle='--')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Evaluation Loss')
plt.legend()
plt.grid(True)
plt.show()

