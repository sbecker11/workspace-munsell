import os
import pandas as pd
from PIL import Image, ImageDraw
import argparse
from munsell_data_frame import MunsellDataFrame
from munsell_data_frame.constants import hue_page_nameS

chip_size = 75
chip_gap = 10

max_rows = None
max_cols = None

page_hue_image_width = None
page_hue_image_height = None

# get the render geometry for the given row/col
def get_chip_geometry(value_row, chroma_column):
    row_idx = value_row - 1
    col_idx = chroma_column // 2 - 1
    x1 = chip_gap // 2 + col_idx * (chip_size + chip_gap)
    y1 = chip_gap // 2 + row_idx * (chip_size + chip_gap) 
    
    assert (x1 >= chip_gap // 2), "x1 out of range"
    assert (y1 >= chip_gap // 2), "y1 out of range"
    x2 = x1 + chip_size
    y2 = y1 + chip_size
    assert (x2 <= page_hue_image_width - chip_gap // 2), "x2 out of range"
    assert (y2 <= page_hue_image_height - chip_gap // 2), "y2 out of range" 
    return (x1, y1, x2, y2)

# render an image for every page_hue
def main(output_image_folder, parquet_file):
    test_df = MunsellDataFrame()
    
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
    global page_hue_image_width
    page_hue_image_width = max_cols//2 * (chip_size + chip_gap) 
    global page_hue_image_height
    page_hue_image_height = max_rows * (chip_size + chip_gap) 
    
    total_tuples = 0
    for hue_page_name in hue_page_nameS:
        hue_page_number = None
        
        # create an image fore each hue page
        image = Image.new('RGBA', (page_hue_image_width, page_hue_image_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # draw a color chip in the image for each page_hue_tuple
        # ['hue_page_number', 'hue_page_name', 'value_row', 'chroma_column', 'color_key', 'r', 'g', 'b']
        page_hue_tuples = munsell_df.get_hue_page_tuples(hue_page_name)
        for tuplet_hue_page_number, _, value_row, chroma_column, _, r, g, b in page_hue_tuples:
            hue_page_number = tuplet_hue_page_number
            (x1,y1,x2,y2) = get_chip_geometry(value_row, chroma_column)
            color = (r,g,b)
            draw.rectangle([x1, y1, x2, y2], fill=color + (255,))  # Set alpha channel to 255 (opaque)
            total_tuples += 1

        # Save the image to a PNG file
        image_file_name = f"{hue_page_number:02.1f}-{hue_page_name}.png"
        image_path = os.path.join(output_image_folder, image_file_name)
        image.save(image_path)
            
    # output the total overage
    print(f"{output_image_folder} total_tuples:{total_tuples}")


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
