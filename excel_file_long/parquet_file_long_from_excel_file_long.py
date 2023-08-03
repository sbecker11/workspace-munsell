import re
import pandas as pd
import openpyxl
import os
import argparse

# from create_js_color_chips import create_js_file
from munsell_data_frame import MunsellDataFrame

# read_lines_from_excel_spreadsheet
# parse the lines into pages and tables
# parse each 'Hue Name' table into V,C,R,G,B values to create a MunsellDataFrame
# save the MunsellDataFrame as a parquet file 

def process_long_excel_file(excel_file_long_dir):
    # output
    parquet_file_long = excel_file_long_dir + "parquet_file_long.parquet"
    
    # input
    excel_file_long = excel_file_long_dir + "Munsell_to_RGB_long.xlsx"
    sheet_name = "munsell2rgb"
    
    lines = read_lines_from_excel_spreadsheet(excel_file_long, sheet_name)
    
    # parse the lines into one dataframe per table
    df_list = parse_pages(lines)
    
    # Print the number of dataframes
    print(f"parsed {len(df_list)} tables")
    
    # Print the first and last rows of each dataframe
    for df in df_list:
        page_number = df['Page Number'].iloc[0]
        table_number = df['Table Number'].iloc[0]
        hue_name = df['Hue Name'].iloc[0]
        num_rows = len(df)
        print(f"Page Number: {page_number}, Table Number: {table_number}, Hue Name: {hue_name}, Number of Rows: {num_rows}")
    
    # Combine all dataframes into one for exporting to a CSV file
    final_df = pd.concat(df_list)
    
    # Sort by these columns
    final_df = final_df.sort_values(by=["Table Number", "V", "C"])

    # Choose order of columns to keep
    df = final_df[["Table Number","Hue Name", "V", "C", "R", "G", "B"]]
    
    print("df.columns:", df.columns)
    # df.columnns: Index(['Table Number', 'Hue Name', 'V', 'C', 'R', 'G', 'B'], dtype='object')
    
    df = df.rename(columns={
        'Table Number': 'page_hue_number',
        'Hue Name': 'page_hue_name',
        'V': 'value_row',
        'C': 'chroma_column',
        'R': 'r',
        'G': 'g',
        'B': 'b'
    })
    print("pre-munsell:", df.columns)

    munsell_df = MunsellDataFrame(df)
    munsell_df.create_color_key()

    print("munsell_df.columes:", munsell_df.columns)
    
    munsell_df.to_parquet(parquet_file_long)
    
    print(f"munsell_df.shape: {munsell_df.shape}")
    print("written to ", parquet_file_long)

def quintext_to_quindict(quintext):
    match = re.search(r'(\d+) (\d+) (\d+) (\d+) (\d+)', quintext)
    if match:
        return {"V":int(match.group(1)), "C":int(match.group(2)), "R":int(match.group(3)), "G":int(match.group(4)), "B":int(match.group(5))}
    else:
        return None

def df_dump(df):
    df = df.sort_values(by=["Table Number", "V", "C"])
    df = df.reset_index(drop=True)
    for i, row in enumerate(df.itertuples(index=False), start=1):
        print(f'Row {i}:', row)

def parse_pages(lines):
    df_list = []
    page_dfs = []
    table_number = None
    hue = None
    author_name = None
    copyright_year = None
    page_number = None

    df = pd.DataFrame()

    for line in lines:
        if len(line.strip()) == 0:
            continue
        elif line.strip().startswith('CONVERSIONS'):
            continue
        if line.strip().startswith('CONVERSIONS'):
            continue
        elif line.strip().startswith('PAUL CENTORE'):
            continue
        elif line.strip().startswith('V C sRGB'):
            continue
        elif line.strip().startswith('Table'):
            match = re.search(r'Table (\d+): Munsell to sRGB Conversions for Hue (.+)', line)
            if match:
                table_number = int(match.group(1))
                hue = match.group(2)
                if not df.empty:
                    df['Table Number'] = table_number
                    df['Hue Name'] = hue
                    page_dfs.append(df)
                    df = pd.DataFrame()
        elif re.search(r'^c (\d+) Paul Centore (\d+)$', line) or re.search(r'^(\d+) c (\d+) Paul Centore$', line):
            match1 = re.search(r'^c (\d+) Paul Centore (\d+)$', line)
            match2 = re.search(r'^(\d+) c (\d+) Paul Centore$', line)
            if match1:
                copyright_year = int(match1.group(1))
                author_name = "Paul Centore"
                page_number = int(match1.group(2))
            elif match2:
                page_number = int(match2.group(1))
                copyright_year = int(match2.group(2))
                author_name = "Paul Centore"
            for df in page_dfs:
                # hue_name = df["Hue Name"].iloc[0]
                # if hue_name == "5.0B":
                #     df_dump(df)
                df['Author Name'] = author_name
                df['Copyright Year'] = copyright_year
                df['Page Number'] = page_number

            df_list.extend(page_dfs)
            print(f"{len(df_list)} page:{page_number}")
            page_dfs = []
        else:
            line = line.replace(',', ' ').replace('[', ' ').replace(']', ' ')
            words = line.split()
            for i in range(0, len(words), 5):
                quintext = ' '.join(words[i:i+5])
                quindict = quintext_to_quindict(quintext)
                if quindict is not None:
                    df = pd.concat([df, pd.DataFrame([quindict])])


    return df_list

def read_lines_from_excel_spreadsheet(excel_file_long, sheet_name='munsell2rgb'):
    
    # Load the workbook
    workbook = openpyxl.load_workbook(excel_file_long)
    
    # Get the sheet named 'munsell2rgb'
    sheet_data = workbook[sheet_name]
    
    # Read the lines from the first column
    lines = [cell.value for cell in sheet_data['A'] if cell.value is not None]
    
    return lines


def main(excel_file_long_dir):
    process_long_excel_file(excel_file_long_dir)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert Excel File Long to Parquet File Long.')
    parser.add_argument('--dir', required=True, help='excel file long directory')

    args = parser.parse_args()

    # Check if the excel_file_long directory exists and is read/writeable
    if not os.path.isdir(args.dir) or not os.access(args.dir, os.R_OK | os.W_OK):
        print(f"Error: The directory {args.dir} does not exist or is not readable.")
        exit(1)
    
    excel_file_long_dir = args.dir + "/"

    main( excel_file_long_dir )
    
    print("done")