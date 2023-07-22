import os
import pandas as pd
from PIL import Image, ImageDraw

width = 75
height = 75
gap = 10
max_rows = 9
max_cols = 19

def create_hue_page(page_hue_name, cl_df, huepages_df):
    selected_rows = cl_df.loc[cl_df['Page_HueName'] == page_hue_name, ['Value_Row', 'Chroma_Column', 'Chip_RGB']]
    rows_data = []

    for _, row in selected_rows.iterrows():
        value_row = int(row['Value_Row']) - 1
        chroma_column = int(row['Chroma_Column']) // 2 - 1
        x1 = gap // 2 + chroma_column * (width + gap)
        y1 = gap // 2 + (max_rows - value_row - 1) * (height + gap)
        x2 = x1 + width
        y2 = y1 + height
        r, g, b = map(int, row['Chip_RGB'].split(','))
        rows_data.append((x1, y1, x2, y2, (r, g, b)))

    image_file = huepages_df.loc[huepages_df.index == page_hue_name, 'Page_Image_File'].values[0]
    return rows_data, image_file

def main():
    excel_file_path = "Munsell-to-RGB-Tables.xlsm"
    image_folder = "HuePagesRendered"

    # Read the "Conversion Lists" sheet into a DataFrame
    xl = pd.ExcelFile(excel_file_path)
    cl_df = xl.parse("Conversion Lists")
    
    # Read the "HuePages" sheet into a DataFrame
    huepages_df = xl.parse("HuePages")
    huepages_df.set_index('Page_HueName', inplace=True)

    # Create the image folder if it doesn't exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Gather the list of page_hue_names from distinct Page_HueName values in cl_df
    page_hue_names = cl_df['Page_HueName'].unique()

    # Process each page_hue_name and create the images
    for page_hue_name in page_hue_names:
        rows_data, image_file = create_hue_page(page_hue_name, cl_df, huepages_df)

        # Create a 720x800 pixel image with transparent background
        image_height = gap // 2 + max_rows * (height + gap)
        image_width = gap // 2 + max_cols * (width + gap)
        image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # Draw the filled rectangles on the image
        for x1, y1, x2, y2, color in rows_data:
            draw.rectangle([x1, y1, x2, y2], fill=color + (255,))  # Set alpha channel to 255 (opaque)

        # Save the image to a PNG file
        image_path = os.path.join(image_folder, f'{image_file}.png')
        image.save(image_path)

        print(f"Saved image for {page_hue_name}: {image_path}")

if __name__ == "__main__":
    main()
