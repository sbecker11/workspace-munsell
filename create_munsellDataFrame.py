
import pandas as pd
import numpy as np
from MunsellDataFrame import MunsellDataFrame

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
    df.drop(columns=['Chip_RGB','Chip_Number'])
        
    # rename and reorder df columns           
    df = df.rename(columns={
        'Page_HueName': 'page_hue_name',
        'Value_Row': 'value_row',
        'Chroma_Column': 'chroma_column',
        'Chip_Color_Key': 'color_key'
    })
    
    # To compute page_hue_number 1 to 40 from page_hue_name
    # Sort the DataFrame by 'page_hue_name'
    df = df.sort_values('page_hue_name')
    # Assign each unique 'page_hue_name' an integer from 1 to number of unique page_hue_names (40)
    df['page_hue_number'] = df.groupby('page_hue_name').ngroup() + 1

    df_columns = df.columns
    print("df_columns:", df_columns)
    mdf = MunsellDataFrame()
    mdf_columns = mdf.columns
    print("mdf_columns:", mdf_columns)
    assert (df_columns == mdf_columns).all(), "DataFrames have different columns"



    munsell_df = MunsellDataFrame(df)
    
    # # Gather the list of page_hue_names from distinct Page_HueName values in cl_df
    # conv_list_page_hue_names =  df['Page_HueName'].unique()
    # print(type(conv_list_page_hue_names))

    # # Read the "HuePages" sheet into a DataFrame
    # huepages_df = excel_file.parse("HuePages")
    # huepages_page_hue_names =  df['Page_HueName'].unique()
    # print(type(huepages_page_hue_names))

    # for huename in huepages_page_hue_names:
    #     print(huename)
    #     hue_lines = huepages_df.
        
    
    # df = MunsellDataFrame()
    
    # rows = [
    #     {'page_hue_number': 1, 'page_hue_name': 'Red', 'value_row': 10, 'chroma_column': 5, 'color_key': '1R10/5', 'r': 255, 'g': 0, 'b': 0},
    #     {'page_hue_number': 2, 'page_hue_name': 'Green', 'value_row': 8, 'chroma_column': 3, 'color_key': '2G8/3', 'r': 0, 'g': 255, 'b': 0},
    #     {'page_hue_number': 3, 'page_hue_name': 'Blue', 'value_row': 6, 'chroma_column': 7, 'color_key': '3B6/7', 'r': 0, 'g': 0, 'b': 255}
    # ]
    # df.append_rows(rows)
    
    # # Save DataFrame to a local parquet file
    # df.to_parquet('test.parquet')

    # # Read DataFrame back from the parquet file
    # df2 = MunsellDataFrame.from_parquet('test.parquet')
    
    # # Convert the data types of the columns in df2 to match those in df
    # for column in df.columns:
    #     df2[column] = df2[column].astype(df[column].dtype)

    # # Verify that the two DataFrames are equal
    # assert df.equals(df2), "DataFrames are not equal"

    # print("DataFrames are equal")

if __name__ == "__main__":
    main()
