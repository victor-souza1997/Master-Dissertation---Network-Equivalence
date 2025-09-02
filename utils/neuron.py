import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')

# Inputs and weights
inputs = [("x₁", "w₁"), ("x₂", "w₂"), ("x₃", "w₃")]
y_positions = [0.7, 0.5, 0.3]

for i, ((x, w), y) in enumerate(zip(inputs, y_positions)):
    ax.text(0.05, y, x, fontsize=12, va='center')
    ax.text(0.15, y + 0.05, "Inputs", fontsize=10, style='italic') if i == 0 else None
    ax.text(0.15, y - 0.05, "Weights", fontsize=10, style='italic') if i == 0 else None
    ax.plot([0.1, 0.4], [y, 0.5], 'k-', lw=1)

# Neuron circle
circle = patches.Circle((0.5, 0.5), 0.1, edgecolor='black', facecolor='none')
ax.add_patch(circle)

# Sum equation inside the neuron
ax.text(0.5, 0.5, r"$z = \sum_i w_i x_i + b$", fontsize=12, ha='center', va='center')

# Activation function area (right semi-circle)
activation_line = plt.Line2D([0.6, 0.6], [0.4, 0.6], color='black', lw=1)
ax.add_line(activation_line)
ax.text(0.65, 0.5, "f(z)", fontsize=12, va='center')

# Output line and label
ax.plot([0.6, 0.85], [0.5, 0.5], 'k-', lw=1)
ax.text(0.88, 0.5, "a", fontsize=12, va='center')
ax.text(0.75, 0.55, "Activation\nfunction", fontsize=10, style='italic')
ax.text(0.88, 0.45, "Output", fontsize=10, style='italic')

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.tight_layout()
plt.show()
