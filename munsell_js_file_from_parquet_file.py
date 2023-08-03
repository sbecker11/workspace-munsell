import os
import pandas as pd
from pathlib import Path
from munsell_data_frame import MunsellDataFrame
import json

def main():

    parquet_filename = " munsell.parquet"
    munsell_df = MunsellDataFrame.from_parquet(parquet_filename)
    munsell_records = munsell_df.to_dict('records')

    js_filename = "munsell.js"
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
    main()
    print("done")
