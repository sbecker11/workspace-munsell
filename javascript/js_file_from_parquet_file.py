import os
import pandas as pd
from pathlib import Path
from munsell_data_frame import MunsellDataFrame
import argparse
import json

def main(js_file, parquet_file):

    # parquet_file input
    parquet_filename = parquet_file
    munsell_df = MunsellDataFrame.from_parquet(parquet_filename)
    munsell_records = munsell_df.to_dict('records')

    # js_file output
    js_filename = js_file
    js_file = Path(js_filename)
    if js_file.exists():
        js_file.unlink()
    with open(js_file, "w") as js:
        num_objects = 0
        js.write("export const flatColorChips = [\n")
        for record in munsell_records:
            js.write(json.dumps(record) + ',\n')
            num_objects += 1
        js.write("\n];\n")
        
    print(f"{js_filename} written as a javascript array with {num_objects} objects")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert Munsell Parquet file to JS.')
    parser.add_argument('--dir', required=True, help='parent dir')
    parser.add_argument('--p', required=True, help='Input Munsell Parquet file')
    parser.add_argument('--j', required=True, help='Output Munsell JS file')

    args = parser.parse_args()
    
    excel_file_dir = args.dir + "/"
    js_file = excel_file_dir + args.j
    parquet_file = excel_file_dir + args.p

    
    # Check if the directory exists and is read/writeable
    if not os.path.isdir(excel_file_dir) or not os.access(excel_file_dir, os.R_OK | os.W_OK):
        print(f"Error: The directory {excel_file_dir} does not exist or is not read/writeable.")
        exit(1)

    # Check if the parquet_file exists and is readable
    if not os.path.isfile(parquet_file) or not os.access(parquet_file, os.R_OK):
        print(f"Error: The file {parquet_file} does not exist or is not readable.")
        exit(1)
        
    
    main(js_file, parquet_file)

    print("done")
