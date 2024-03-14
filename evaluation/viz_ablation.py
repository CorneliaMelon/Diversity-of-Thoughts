import matplotlib.pyplot as plt

# Data
number_of_roles = [2, 4, 8]
accuracy = [7.1, 10, 8.6]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(number_of_roles, accuracy, marker='o', linestyle='-', color='b')

# Annotating each point with its accuracy
for i, txt in enumerate(accuracy):
    plt.annotate(f"{txt}%", (number_of_roles[i], accuracy[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Title and labels
plt.title('Accuracy vs. Number of Roles')
plt.xlabel('Number of Roles')
plt.ylabel('Accuracy (%)')

# Show plot
plt.grid(True)
plt.show()

