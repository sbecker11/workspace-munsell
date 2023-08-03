import os
import pandas as pd
from PIL import Image, ImageDraw
import color_chip_module
from histogram.plot_color_histograms import plot_color_histograms

width = 75
height = 75
gap = 10
max_rows = 11
max_cols = 20

def create_hue_page(page_hue_name, cl_df, huepages_df):
    # selected_rows = cl_df.loc[cl_df['Page_HueName'] == page_hue_name, ['Value_Row', 'Chroma_Column', 'Chip_RGB', 'Chip_Color_Key']]
    selected_rows = cl_df.loc[cl_df['Page_HueName'] == page_hue_name]
    rows_data = []
    rows = [item[1] for item in selected_rows.iterrows()]
    for row in rows:
        value_row = int(row['Value_Row'])
        chroma_column = row['Chroma_Column']  # Use .iloc[0] to get the first (and only) value as an integer
        row_idx = value_row - 1
        col_idx = chroma_column // 2
        x1 = gap // 2 + (col_idx + 1 - 1) * (width + gap)
        y1 = gap // 2 + (max_rows - row_idx - 1 - 1) * (height + gap) # use max_rows to invert the y values
        x2 = x1 + width
        y2 = y1 + height
        rgb = str(row['Chip_RGB'])
        r, g, b = map(int, rgb.split(','))
        color_key = str(row['Chip_Color_Key'])
        rows_data.append((x1, y1, x2, y2, (r, g, b), color_key, chroma_column, value_row))

    # print("value_row:", value_row, "rgb_counter:", rgb_counter);
    image_file = huepages_df.loc[huepages_df.index == page_hue_name, 'Page_Image_File'].values[0]
    return rows_data, image_file

color_chip_module.createFile('color_chips.js')
color_chip_module.addLine("export const flatColorChips = [")

def main():
    excel_colorChipFile = "Munsell-to-RGB-Tables.xlsm"
    image_folder = "HuePagesRendered"

    # Read the "Conversion Lists" sheet into a DataFrame
    xl = pd.ExcelFile(excel_colorChipFile)
    cl_df = xl.parse("Conversion Lists")

    # Calculate the before_cols before the merge
    before_cols = sorted([str(c) for c in cl_df.columns])
    before_length = len(before_cols)
    before_set = set(before_cols)

    # Read the "HuePages" sheet into a DataFrame
    huepages_df = xl.parse("HuePages")
    huepages_df.set_index('Page_HueName', inplace=True)

    # Create the image folder if it doesn't exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Gather the list of page_hue_names from distinct Page_HueName values in cl_df
    page_hue_names = cl_df['Page_HueName'].unique()
    page_hue_number = 1;
    colors = []
    # Process each page_hue_name and create the images
    for page_hue_name in page_hue_names:
        rows_data, image_file = create_hue_page(page_hue_name, cl_df, huepages_df)

        # Create a 720x800 pixel image with transparent background
        image_height = gap // 2 + max_rows * (height + gap)
        image_width = gap // 2 + max_cols * (width + gap)
        image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # Draw the filled rectangles on the image
        # rows_data.append((x1, y1, x2, y2, (r, g, b), color_key, chroma_column, value_row))
        for x1, y1, x2, y2, color, color_key, chroma_column, value_row in rows_data:
            draw.rectangle([x1, y1, x2, y2], fill=color + (255,))  # Set alpha channel to 255 (opaque)
            r,g,b = color
            obj = {
                "x1": x1, "y1":y1, "x2":x2, "y2":y2,
                "page_hue_number": page_hue_number,
                "page_hue_name": page_hue_name, 
                "value_row": value_row, 
                "chroma_column": chroma_column,
                "color_key": color_key,
                "r": r, "g":g, "b":b 
            }
            js_object_str = "{ " + ', '.join(f"{key}: '{value}'" for key, value in obj.items()) + " },"
            color_chip_module.addLine(js_object_str)
            colors.append(color)

        # Save the image to a PNG file
        image_path = os.path.join(image_folder, image_file)
        image.save(image_path)

        print(f"Saved image for {page_hue_number} {page_hue_name}: {image_path}")
        page_hue_number += 1
    color_chip_module.addLine("];")
    plot_color_histograms(colors)

if __name__ == "__main__":
    main()
    print("done")
