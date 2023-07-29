import matplotlib.pyplot as plt

# Assuming colorTuples is a list of dictionaries like:
# colorTuples = [
#     {"r": "0", "g": "0", "b": "0"},
#     {"r": "255", "g": "255", "b": "255"},
#     {"r": "128", "g": "128", "b": "128"},
#     ...
# ]

def plot_color_histograms(colorTuples: list[tuple]) -> None:
    # Convert strings to integers and create separate lists for r, g, b values
    r_values = [int(colorTuple[0]) for colorTuple in colorTuples]
    g_values = [int(colorTuple[1]) for colorTuple in colorTuples]
    b_values = [int(colorTuple[2]) for colorTuple in colorTuples]

    # Create histograms for r, g, b values
    plt.figure(figsize=(18, 6))

    plt.subplot(131)  # 1 row, 3 columns, plot 1
    plt.hist(r_values, bins=20, color='red', alpha=0.7)
    plt.title('Red Values')

    plt.subplot(132)  # 1 row, 3 columns, plot 2
    plt.hist(g_values, bins=20, color='green', alpha=0.7)
    plt.title('Green Values')

    plt.subplot(133)  # 1 row, 3 columns, plot 3
    plt.hist(b_values, bins=20, color='blue', alpha=0.7)
    plt.title('Blue Values')

    plt.show()


