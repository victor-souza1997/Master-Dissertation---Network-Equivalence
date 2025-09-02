import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    """Computes the sigmoid function."""
    return 1 / (1 + np.exp(-x))

def relu(x):
    """Computes the Rectified Linear Unit (ReLU) function."""
    return np.maximum(0, x)

def tanh(x):
    """Computes the hyperbolic tangent (tanh) function."""
    return np.tanh(x)

# --- Plotting Setup ---

# Generate a range of x values
x = np.linspace(-5, 5, 100)

# Calculate the y values for each function
y_sigmoid = sigmoid(x)
y_relu = relu(x)
y_tanh = tanh(x)

# Set a professional style for the plot (optional, but looks good for papers)
plt.style.use('seaborn-v0_8-whitegrid')

# Create a figure and a set of subplots
# 1 row, 3 columns, with a shared y-axis for better comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

# --- Plot 1: Sigmoid ---
axes[0].plot(x, y_sigmoid, color='blue', lw=2)
axes[0].set_title('Sigmoid', fontsize=16)
axes[0].set_xlabel('x', fontsize=12)
axes[0].set_ylabel('f(x)', fontsize=12)
# Add axis lines for clarity
axes[0].axhline(y=0, color='k', linestyle='--', lw=0.5)
axes[0].axvline(x=0, color='k', linestyle='--', lw=0.5)

# --- Plot 2: ReLU ---
axes[1].plot(x, y_relu, color='red', lw=2)
axes[1].set_title('ReLU (Rectified Linear Unit)', fontsize=16)
axes[1].set_xlabel('x', fontsize=12)
# Add axis lines for clarity
axes[1].axhline(y=0, color='k', linestyle='--', lw=0.5)
axes[1].axvline(x=0, color='k', linestyle='--', lw=0.5)

# --- Plot 3: Tanh ---
axes[2].plot(x, y_tanh, color='green', lw=2)
axes[2].set_title('Tanh (Hyperbolic Tangent)', fontsize=16)
axes[2].set_xlabel('x', fontsize=12)
# Add axis lines for clarity
axes[2].axhline(y=0, color='k', linestyle='--', lw=0.5)
axes[2].axvline(x=0, color='k', linestyle='--', lw=0.5)

# --- Final Touches ---

# Improve layout to prevent titles/labels from overlapping
plt.tight_layout()

# Save the figure to a file for your paper
# You can change the format to .pdf, .svg, or .eps for higher quality
plt.savefig('activation_functions.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

print("Plot saved as 'activation_functions.png'")
