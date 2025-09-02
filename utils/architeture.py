import matplotlib.pyplot as plt

def draw_neural_net(ax, left, right, bottom, top, layer_sizes):
    '''
    Draws a neural network cartoon using matplotlib.
    
    Parameters:
        ax: matplotlib.axes.AxesSubplot - the axes on which to plot the cartoon.
        left: float - the leftmost x-coordinate of the network.
        right: float - the rightmost x-coordinate of the network.
        bottom: float - the bottom y-coordinate.
        top: float - the top y-coordinate.
        layer_sizes: list of int - list containing the number of nodes in each layer.
    '''
    n_layers = len(layer_sizes)
    v_spacing = (top - bottom)/float(max(layer_sizes))
    h_spacing = (right - left)/float(n_layers - 1)

    # Nodes
    for i, n_nodes in enumerate(layer_sizes):
        layer_top = v_spacing*(n_nodes - 1)/2. + (top + bottom)/2.
        for j in range(n_nodes):
            circle = plt.Circle((left + i*h_spacing, layer_top - j*v_spacing), 0.05,
                                color='w', ec='k', zorder=4)
            ax.add_artist(circle)

    # Edges
    for i, (n_nodes_a, n_nodes_b) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        layer_top_a = v_spacing*(n_nodes_a - 1)/2. + (top + bottom)/2.
        layer_top_b = v_spacing*(n_nodes_b - 1)/2. + (top + bottom)/2.
        for j in range(n_nodes_a):
            for k in range(n_nodes_b):
                line = plt.Line2D([left + i*h_spacing, left + (i+1)*h_spacing],
                                  [layer_top_a - j*v_spacing, layer_top_b - k*v_spacing],
                                  c='k', alpha=0.3)
                ax.add_artist(line)

def show_nn_topology(layer_sizes):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    draw_neural_net(ax, .1, .9, .1, .9, layer_sizes)

    # Labels
    positions = ['Input', 'Hidden', 'Output']
    for i, name in enumerate(positions[:len(layer_sizes)]):
        x = 0.1 + i * (0.8 / (len(layer_sizes) - 1))
        ax.text(x, 0.95, name + ' Layer', fontsize=12, ha='center')

    plt.show()

# Example: 3 input neurons, 4 hidden, 2 output
show_nn_topology([3, 4, 2])

