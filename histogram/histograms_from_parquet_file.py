import argparse
import os
from matplotlib import pyplot as plt
from munsell_data_frame import MunsellDataFrame

# Requires a list of colorTuplles like this:
# colorTuples = [
#     (0,255,175),
#     (255,175,0),
#     (175,0,255),
#     ...
# ]
def plot_color_histograms(parquet_file, colorTuples):
    # Convert strings to integers and create separate lists for r, g, b values
    r_values = [int(colorTuple[0]) for colorTuple in colorTuples]
    g_values = [int(colorTuple[1]) for colorTuple in colorTuples]
    b_values = [int(colorTuple[2]) for colorTuple in colorTuples]

    # Create histograms for r, g, b values
    fig = plt.figure(f"histogram of {parquet_file}" ,figsize=(18, 6))
    # fig = plt.figure()

    plt.subplot(131)  # 1 row, 3 columns, plot 1
    plt.hist(r_values, bins=20, color='red', alpha=0.7)
    plt.title('Red Values')

    plt.subplot(132)  # 1 row, 3 columns, plot 2
    plt.hist(g_values, bins=20, color='green', alpha=0.7)
    plt.title('Green Values')

    plt.subplot(133)  # 1 row, 3 columns, plot 3
    plt.hist(b_values, bins=20, color='blue', alpha=0.7)
    plt.title('Blue Values')

    plt.draw()
    plt.pause(1)
    
    input("\nHit any key to continue!\n")
    
    plt.close(fig)

    
def main(parquet_file):
    munsell_df = MunsellDataFrame.from_parquet(parquet_file)
    rgb_tuples = munsell_df.get_rgb_tuples()
    plot_color_histograms(parquet_file, rgb_tuples)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Display a color histogram from a Munsell parquet file.')
    parser.add_argument('--p', required=True, help='Input Munsell Parquet file')

    args = parser.parse_args()
    
    parquet_file = args.p

    # Check if the parquet_file exists and is readable
    if not os.path.isfile(parquet_file) or not os.access(parquet_file, os.R_OK):
        print(f"Error: The file {parquet_file} does not exist or is not readable.")
        exit(1)

    main(parquet_file)
    
    print("done")
