import os
import pandas as pd
from PIL import Image, ImageDraw

width = 75
height = 75
gap = 10
max_rows = 11
max_cols = 20

def create_hue_page(page_hue_name, cl_df, gr_df, huepages_df):
    # selected_rows = cl_df.loc[cl_df['Page_HueName'] == page_hue_name, ['Value_Row', 'Chroma_Column', 'Chip_RGB', 'Chip_Color_Key']]
    selected_rows = cl_df.loc[cl_df['Page_HueName'] == page_hue_name]
    rows_data = []
    rows = [item[1] for item in selected_rows.iterrows()]
    rows.append(gr_df.loc[0])
    rows.append(gr_df.loc[10])
    for row in rows:
        value_row = int(row['Value_Row'])
        col_suffixes =['','_x'] if (value_row > 0 and value_row < 10) else ['']
        # rgb_counter = {}
        for suffix in col_suffixes:
            chroma_column = row['Chroma_Column'+suffix]  # Use .iloc[0] to get the first (and only) value as an integer
            row_idx = value_row - 1
            col_idx = chroma_column // 2
            x1 = gap // 2 + (col_idx + 1 - 1) * (width + gap)
            y1 = gap // 2 + (max_rows - row_idx - 1 - 1) * (height + gap)
            x2 = x1 + width
            y2 = y1 + height
            rgb = str(row['Chip_RGB'+suffix])
            # if rgb not in rgb_counter:
            #     rgb_counter[rgb] = 0
            # rgb_counter[rgb] += 1
            r, g, b = map(int, rgb.split(','))
            key = str(row['Chip_Color_Key'+suffix])
            rows_data.append((x1, y1, x2, y2, (r, g, b), key))

        # print("value_row:", value_row, "rgb_counter:", rgb_counter);
    image_file = huepages_df.loc[huepages_df.index == page_hue_name, 'Page_Image_File'].values[0]
    return rows_data, image_file

def main():
    excel_file_path = "Munsell-to-RGB-Tables.xlsm"
    image_folder = "HuePagesRendered"

    # Read the "Conversion Lists" sheet into a DataFrame
    xl = pd.ExcelFile(excel_file_path)
    cl_df = xl.parse("Conversion Lists")

    # Calculate the before_cols before the merge
    before_cols = sorted([str(c) for c in cl_df.columns])
    before_length = len(before_cols)
    before_set = set(before_cols)

    # Read the "HuePages" sheet into a DataFrame
    huepages_df = xl.parse("HuePages")
    huepages_df.set_index('Page_HueName', inplace=True)

    # Read the "Gray" sheet into a separate DataFrame
    gr_df = xl.parse("Gray")

    # Merge gr_df with cl_df using a left join on "Value_Row"
    cl_df = cl_df.merge(gr_df, on="Value_Row", how="left", suffixes=('', '_x'))

    # identical to rename(columns)
    # cols_x_map = [(cx,cx.replace('_x','')) for cx in cl_df.columns if cx.endswith('_x')]
    # for cx in cols_x_map:
    #     cl_df[cx[0]] = cl_df[cx[1]]

    # Rename col_x and col_y to col after the merge
    # cl_df.rename(columns={col + '_x': col for col in before_set}, inplace=True)

    # Calculate the after_cols after the merge and renaming
    # after_cols = sorted([str(c) for c in cl_df.columns])
    # after_length = len(after_cols)
    # after_set = set(after_cols)

    # # Check if column names are altered after the merge and renaming
    # if not before_cols == after_cols:
    #     print(f"Error: Column names before:{before_length} after:{after_length} in cl_df have been altered after the merge and rename.")
    #     exit(1)

    # Create the image folder if it doesn't exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Gather the list of page_hue_names from distinct Page_HueName values in cl_df
    page_hue_names = cl_df['Page_HueName'].unique()

    # Process each page_hue_name and create the images
    for page_hue_name in page_hue_names:
        rows_data, image_file = create_hue_page(page_hue_name, cl_df, gr_df, huepages_df)

        # Create a 720x800 pixel image with transparent background
        image_height = gap // 2 + max_rows * (height + gap)
        image_width = gap // 2 + max_cols * (width + gap)
        image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # Draw the filled rectangles on the image
        for x1, y1, x2, y2, color, key in rows_data:
            draw.rectangle([x1, y1, x2, y2], fill=color + (255,))  # Set alpha channel to 255 (opaque)

        # Save the image to a PNG file
        image_path = os.path.join(image_folder, image_file)
        image.save(image_path)

        print(f"Saved image for {page_hue_name}: {image_path}")

if __name__ == "__main__":
    main()
