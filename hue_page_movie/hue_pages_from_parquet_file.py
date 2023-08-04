import os
import pandas as pd
from PIL import Image, ImageDraw
import argparse
from munsell_data_frame import MunsellDataFrame
from munsell_data_frame.constants import PAGE_HUE_NAMES
import math

chip_size = 75
chip_gap = 10

max_rows = None
max_cols = None

hue_page_image_width = None
hue_page_image_height = None

def format_pair(value_row, chroma_column):
    return f"{value_row}-{chroma_column}"

def parse_pair(pair):
    value_row, chroma_column = map(int, pair.split("-"))
    return value_row, chroma_column

# given a pair tuplet with values (pair, r, g, b)
def get_page_geometry(value_row, chroma_column):
    row_idx = value_row - 1
    col_idx = chroma_column // 2 - 1
    x1 = chip_gap // 2 + col_idx * (chip_size + chip_gap)
    y1 = chip_gap // 2 + row_idx * (chip_size + chip_gap) 
    
    assert (x1 >= chip_gap // 2), "x1 out of range"
    assert (y1 >= chip_gap // 2), "y1 out of range"
    x2 = x1 + chip_size
    y2 = y1 + chip_size
    assert (x2 <= hue_page_image_width - chip_gap // 2), "x2 out of range"
    assert (y2 <= hue_page_image_height - chip_gap // 2), "y2 out of range" 
    return (x1, y1, x2, y2)

# find all value-chroma quintgs in the given page_hue_name from munsell_df
# where a quint is a tuplet with values (value_row, chroma_column, r, g, b)
def get_page_hue_quints(page_hue_name, munsell_df):
    selected_rows = munsell_df.filter_by_columns({'page_hue_name': page_hue_name })
    page_hue_quints = []
    rows = [item[1] for item in selected_rows.iterrows()]
    for row in rows:
        value_row = int(row['value_row'])
        chroma_column = int(row['chroma_column']) # Use .iloc[0] to get the first (and only) value as an integer
        pair = format_pair(value_row, chroma_column)
        r = row['r']
        g = row['g']
        b = row['b']
        page_hue_quint = (value_row, chroma_column, r, g, b)
        page_hue_quints.append(page_hue_quint)
    return page_hue_quints

# there are multiple samples for each value-chroma pair
# return the unique nints and their average r,g,b values
# a nint is a 9-tuplet with thse components: 
# (x1,y1,x2,y2,value_row, chroma_column, r, g, b) 
# a quint is a 5-tuplet with componentes:
# (value_row, chroma_column, r, g, b) 
# a pair is a 2-tuplet with components:
# (value_row, chroma_column) and is commonly string formatted as 
# f"{value_row}-{chroma_column}"
def get_normalized_page_hue_nints(page_hue_quints):
    normalized_page_hue_nints = []
    num_pairs = 0
    pair_cnts = {}
    pair_r_sum = {}
    pair_g_sum = {}
    pair_b_sum = {}
    pair_cnts = {}
    for value_row, chroma_column, r, g, b in page_hue_quints:
        pair = format_pair(value_row, chroma_column)
        if pair not in pair_cnts:
            pair_cnts[pair] = 0
            pair_r_sum[pair] = 0
            pair_g_sum[pair] = 0
            pair_b_sum[pair] = 0
        pair_cnts[pair] += 1
        pair_r_sum[pair] += r
        pair_g_sum[pair] += g
        pair_b_sum[pair] += b
        num_pairs += 1
    
    # get mean r,g,b for each unique pair
    for unique_pair in pair_cnts:
        cnt = 1.0 * pair_cnts[unique_pair]
        # compute average r,g,b
        r = math.floor(1.0 * pair_r_sum[unique_pair] / cnt)
        g = math.floor(1.0 * pair_g_sum[unique_pair] / cnt)
        b = math.floor(1.0 * pair_b_sum[unique_pair] / cnt)
        value_row, chroma_column = parse_pair(unique_pair)
        # create the normalized page_hue_nonts (9-tuples)
        (x1,y1,x2,y2) = get_page_geometry(value_row, chroma_column)
        normalized_page_hue_nint = (x1,y1,x2,y2, value_row, chroma_column, r, g, b)
        normalized_page_hue_nints.append(normalized_page_hue_nint)
        
    return normalized_page_hue_nints
   

def main(output_image_folder, parquet_file):
    
    munsell_df = MunsellDataFrame.from_parquet(parquet_file)
    
    # create the image folder if it doesn't exist
    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)
    
    # get the max cols and rows
    global max_cols
    max_cols = munsell_df.max_column('chroma_column')
    global max_rows
    max_rows = munsell_df.max_column('value_row')

    # compute the image size
    global hue_page_image_width
    hue_page_image_width = max_cols//2 * (chip_size + chip_gap) 
    global hue_page_image_height
    hue_page_image_height = max_rows * (chip_size + chip_gap) 

    # render a page_hue image file for each page_hue_name
    page_hue_number = 1
    for page_hue_name in PAGE_HUE_NAMES:
        print(f"page_hue_name: {page_hue_name}")
        page_hue_quints = get_page_hue_quints(page_hue_name, munsell_df)
        print(f"num_page_hue_quints: {len(page_hue_quints)}")
        normalized_page_hue_nints = get_normalized_page_hue_nints(page_hue_quints)
        print(f"num_normalized_page_hue_nints: {len(normalized_page_hue_nints)}")
        
        image = Image.new('RGBA', (hue_page_image_width, hue_page_image_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # Draw a filled rectangles on the image for each normalized_page_hue_pair
        for x1, y1, x2, y2, value_row, chroma_column, r, g, b in normalized_page_hue_nints:
            color = (r,g,b)
            draw.rectangle([x1, y1, x2, y2], fill=color + (255,))  # Set alpha channel to 255 (opaque)

        # Save the image to a PNG file
        image_file_name = f"{page_hue_number:02.1f}-{page_hue_name}.png"
        image_path = os.path.join(output_image_folder, image_file_name)
        image.save(image_path)

        print(f"Saved image for {page_hue_number} {page_hue_name}: {image_path}")
        page_hue_number += 1

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Create a folder of Munsell Hue Pages from a Munsell Parquet file.')
    parser.add_argument('--o', required=True, help='output Hue Pages image folder')
    parser.add_argument('--p', required=True, help='Input Munsell Parquet file')

    args = parser.parse_args()
    
    output_image_folder = args.o
    parquet_file = args.p

    # Check if the parquet_file exists and is readable
    if not os.path.isfile(parquet_file) or not os.access(parquet_file, os.R_OK):
        print(f"Error: The file {parquet_file} does not exist or is not readable.")
        exit(1)

    main(output_image_folder, parquet_file)
    
    print("done")
