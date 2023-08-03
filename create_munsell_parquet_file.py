
import pandas as pd
import numpy as np
from munsell_data_frame import MunsellDataFrame, SortOrder

# reads an Excel spreadsheet with macros and writes a 
def main():
    
    excel_colorChipFile = "Munsell-to-RGB-Tables.xlsm"

    # Read the "Conversion Lists" sheet into a DataFrame
    excel_file = pd.ExcelFile(excel_colorChipFile)
    df = excel_file.parse("Conversion Lists")
    
    # df has columns:
    # conv_list_columns = df.columns
    # ['Page_HueName', 'Value_Row', 'Chroma_Column', 'Chip_Color_Key', 'Chip_RGB', 'Chip_Number']
    # MunsellDataFrame has columns:
    # 'page_hue_number', 'page_hue_name', 'value_row',  'chroma_column', 'color_key', 'r', 'g', 'b']
    
    # replace Chip_RGB string column with r,g and b int columns 
    df['Chip_RGB'] = df['Chip_RGB'].str.replace('(', '').str.replace(')', '')
    df[['r', 'g', 'b']] = df['Chip_RGB'].str.split(',', expand=True).astype(int)
    
    # drop unused columns
    df = df.drop(columns=['Chip_RGB','Chip_Number'])
        
    # rename and reorder df columns           
    df = df.rename(columns={
        'Page_HueName': 'page_hue_name',
        'Value_Row': 'value_row',
        'Chroma_Column': 'chroma_column',
        'Chip_Color_Key': 'color_key'
    })
    

    # To compute page_hue_number 1 to 40 from page_hue_name
    # Sort the DataFrame by 'page_hue_name'
    sort_orders = {
        'page_hue_name': SortOrder.ASC
    }
    sorted_df = df.sort_values(by=list(sort_orders.keys()), ascending=[sort_order == SortOrder.ASC for sort_order in sort_orders.values()])
    
    # Assign each unique 'page_hue_name' an integer from 1 to number of unique page_hue_names (40)
    df['page_hue_number'] = df.groupby('page_hue_name').ngroup() + 1

    # make sure the incoming df is compatible with MunsellDataFrame
    empty_mdf = MunsellDataFrame()
    
    assert (len(df.columns) == len(empty_mdf.columns)), "DataFrames must have same number of columns"
    assert (set(df.columns) == set(empty_mdf.columns)), "DataFrames have different columns"

    munsell_df = MunsellDataFrame(df)
    
    parquet_filename = "munsell.parquet"
    munsell_df.to_parquet(parquet_filename)
    
    check_df = MunsellDataFrame.from_parquet(parquet_filename)
    assert( check_df.shape == munsell_df.shape )
    
    print(f"munsell_df.shape: {munsell_df.shape}")
    print("written to ", parquet_filename)

if __name__ == "__main__":
    main()
    print("done")
