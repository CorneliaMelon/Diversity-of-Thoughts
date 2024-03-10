import matplotlib.pyplot as plt
import json

def load_log_data(file_path):
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    
    log_history = []
    for entry in data["log_history"]:
        
        epoch = entry.get("epoch")
        loss = entry.get("loss")
        eval_loss = entry.get("eval_loss")
        step = entry.get("step")
        
        
        if epoch is not None and loss is not None and eval_loss is not None and step is not None:
            log_history.append({
                "epoch": epoch,
                "loss": loss,
                "eval_loss": eval_loss,
                "step": step
            })
    
    return log_history


file_path = '/Users/corneliaweinzierl/Downloads/trainer_state_new.json'  # Update this to your actual file path
log_history = load_log_data(file_path)

print(log_history)


steps = [entry["step"] for entry in log_history]
training_loss = [entry["loss"] for entry in log_history]
eval_loss = [entry["eval_loss"] for entry in log_history]


plt.figure(figsize=(10, 6))
plt.plot(steps, training_loss, label='Training Loss')
plt.plot(steps, eval_loss, label='Evaluation Loss', linestyle='--')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.title('Training and Evaluation Loss')
plt.legend()
plt.grid(True)
plt.show()
