
import pandas as pd
import numpy as np
from munsell_data_frame.MunsellDataFrame import MunsellDataFrame, SortOrder
from munsell_data_frame.constants import HUE_PAGE_NAMES
import os
import argparse

# reads an Excel spreadsheet with macros and writes a 
def process_excel_file_macro(excel_file_macro_dir):
    # output
    parquet_file_macro = excel_file_macro_dir + "parqet_file_macro.parquet"

    # input
    excel_file_macro = excel_file_macro_dir + "Munsell-to-RGB-Tables.xlsm"
    sheet = "Conversion Lists"

    # Read the "Conversion Lists" sheet into a DataFrame
    excel_file = pd.ExcelFile(excel_file_macro)
    df = excel_file.parse(sheet)
    
    # df has columns:
    # conv_list_columns = df.columns
    # ['Page_HueName', 'Value_Row', 'Chroma_Column', 'Chip_Color_Key', 'Chip_RGB', 'Chip_Number']
    # MunsellDataFrame has columns:
    # 'hue_page_number', 'hue_page_name', 'value_row',  'chroma_column', 'color_key', 'r', 'g', 'b']
    
    # replace Chip_RGB string column with r,g and b int columns 
    df['Chip_RGB'] = df['Chip_RGB'].str.replace('(', '').str.replace(')', '')
    df[['r', 'g', 'b']] = df['Chip_RGB'].str.split(',', expand=True).astype(int)
    
    # drop unused columns
    df = df.drop(columns=['Chip_RGB','Chip_Number', 'Chip_Color_Key'])
        
    # rename and reorder df columns           
    df.rename(columns={
        'Page_HueName': 'hue_page_name',
        'Value_Row': 'value_row',
        'Chroma_Column': 'chroma_column',
        'R': 'r',
        'G': 'g',
        'B': 'b'
    }, inplace=True)
        
    # Create a mapping dictionary to 
    hue_page_name_to_number = {name: idx for idx, name in enumerate(HUE_PAGE_NAMES)}

    # Map hue_page_name to its corresponding hue_page_number
    df['hue_page_number'] = df['hue_page_name'].map(hue_page_name_to_number)

    # make sure the incoming df is compatible with MunsellDataFrame
    munsell_df = MunsellDataFrame(df)
    
    # set the color_key column
    munsell_df.set_color_key()
    
    # keep these reordered columns
    munsell_df.df = munsell_df.df[["color_key","r","g","b"]]
    print(f"munsell_df shape before groupby_color_key: {munsell_df.shape}")
    
    munsell_df = munsell_df.groupby_color_key()
    print(f"munsell_df shape after groupby_color_key: {munsell_df.shape}")

    
    munsell_df.to_parquet(parquet_file_macro)
    
    check_df = MunsellDataFrame.from_parquet(parquet_file_macro)
    assert( check_df.shape == munsell_df.shape )
    
    print(f"munsell_df.shape: {munsell_df.shape}")
    print("written to ", parquet_file_macro)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert Excel File Macro to Parquet File Macro.')
    parser.add_argument('--dir', required=True, help='excel file macro directory')

    args = parser.parse_args()

    # Check if the excel_file_macro directory exists and is read/writeable
    if not os.path.isdir(args.dir) or not os.access(args.dir, os.R_OK | os.W_OK):
        print(f"Error: The directory {args.dir} does not exist or is not readable.")
        exit(1)
    
    excel_file_macro_dir  = args.dir + "/"
    process_excel_file_macro(excel_file_macro_dir)
    
    print("done")
