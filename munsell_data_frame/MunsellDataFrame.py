import pandas as pd
from enum import Enum
import numpy as np 
import math
from .constants import HUE_PAGE_NAMES

# used in the sort_orders dict for sort_by_columns
class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'

class MunsellDataFrame:
    
    # column names and their dtypes
    _dtypes = {
        'hue_page_number': 'UInt8',
        'hue_page_name': 'str',
        'value_row': 'UInt8',
        'chroma_column': 'UInt8',
        'color_key': 'str',
        'r': 'UInt8',
        'g': 'UInt8',
        'b': 'UInt8',
    }

    # called when creating an instance of a MunsellDataFrame 
    # using
    # df = MunsellDataFrame() 
    # or using 
    # df = MunsellDataFrame([
    #     {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0},
    #     {'hue_page_number': 1, 'hue_page_name': '5.0R', 'value_row': 8, 'chroma_column': 3, 'color_key': 'change', 'r': 0, 'g': 255, 'b': 0},
    #     {'hue_page_number': 2, 'hue_page_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': 'change', 'r': 0, 'g': 0, 'b': 255},
    # ]
    # returns None - since self has been altered
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        if data is None:
            data = pd.DataFrame(columns=self._dtypes.keys())
        else:
            data = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self.df = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self._set_dtypes()

    # used to set dataframe columns in __init__
    # returns None - since self has been altered
    def _set_dtypes(self): # pragma: no cover
        for col, dtype in self._dtypes.items():
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(dtype)
        
    # append rows to the dataframe where each row
    # is a MunsellDataFrame-columned dict
    # returns None - since self has been altered.
    #
    # Note that any row with an empty dict will 
    # still be added as a row with empty column values. 
    # for example:
    #     hue_page_number hue_page_name  value_row  chroma_column color_key     r     g     b
    #  0   <NA>           nan            <NA>        <NA>         nan         <NA>  <NA>  <NA>
    def append_rows(self, rows):
        if self.df.empty:
            self.__init__(columns=self._dtypes.keys())
        for row in rows:
            if row: # skip empty rows
                self.df.loc[len(self.df)] = row
        self._set_dtypes()
    
    # handle all to_dict options
    def to_dict(self, *args, **kwargs): # pragma: no cover
        return self.df.to_dict(*args, **kwargs)
    
    # return a list of dicts
    def to_list_of_dicts(self):
        return self.df.to_dict('records')
    
    # return a list of tuples
    def to_list_of_tuples(self):
        return list(self.df.itertuples(index=False, name=None))
    
    # save the values of the dataframe to a csv file
    def to_csv(self, filename):
        return self.df.to_csv(filename)

    @classmethod
    # load the data of the dataframe from a csv file
    # into a newly created MunsellDataFrame
    def from_csv(cls, filename):
        df = pd.read_csv(filename)
        unnamed = 'Unnamed: 0'
        if unnamed in df.columns:
            df = df.drop(columns=[unnamed])
        return cls(data=df.values, columns=df.columns)

    # save the dataframe to a parquet file
    def to_parquet(self, filename):
        self.df.to_parquet(filename, engine='pyarrow')

    @classmethod
    # load the dataframe from a parquet file
    # into a newly created MunsellDataFrame
    def from_parquet(cls, filename):
        filename = filename.strip()
        df = pd.read_parquet(filename, engine='pyarrow')
        return cls(data=df.values, columns=df.columns)

    # return a list of unique values for the given column
    def unique_values(self, column):
        unique_vals = self.df[column].unique()
        return [int(val) if isinstance(val, float) and val.is_integer() else val.item() if isinstance(val, np.generic) else val for val in unique_vals]

    # remove the dataframe's index column
    # return None - since self has been altered
    def reset_index(self):
        self.df = self.df.reset_index(drop=True)

    # return a MunsellDataFrame that contains all rows 
    # that match all of the given column filters, for example:
    # filters = {
    #     "value_row": 7,
    #     "chroma_column": 2
    # }
    # so self has not been altered
    def filter_by_columns(self, filters):
        mask = pd.Series([True]*len(self.df))
        for col, val in filters.items():
            mask = mask & (self.df[col] == val)
        return MunsellDataFrame(self.df[mask])
    
    # Drop columns by their names.
    # Parameters:
    # - columns (str or list of str): Column name or names of the columns to drop.
    # return None, since self has been altered
    def drop_columns(self, columns, reset_index=True):
        self.df = self.df.drop(columns=columns, axis=1)
        if reset_index:
            self.df.reset_index(drop=True, inplace=True)

    # Drop rows by their indices
    # Parameters:
    # - indices (int or list of ints): Index or indices of the rows to drop.
    # return None, since self has been altered
    def drop_rows(self, indices, reset_index=True):
        self.df = self.df.drop(indices)
        if reset_index:
            self.df.reset_index(drop=True, inplace=True)


    # remove all rows in the dataframe that match all of the given column filters., for example:
    # filters = {
    #     "value_row": 7,
    #     "chroma_column": 2
    # }
    # if reset_index is False then the resulting df may have gaps in its index
    # return None - since self has been altered
    def remove_by_columns(self, filters, reset_index=True):
        for col, val in filters.items():
            self.df = self.df[self.df[col] != val]
        if reset_index:
            self.df.reset_index(drop=True, inplace=True)

    # sort the dataframe by multiple columns given a sort_orders dictionary, for example:
    # sort_orders = {
    #     "value_row": SortOrder.ASC,
    #     "chroma_column": SortOrder.DESC
    # }
    # returns a new MunsellDataFrame that contains the sorted rows
    def sort_by_columns(self, sort_orders):
        return MunsellDataFrame(self.df.sort_values(by=list(sort_orders.keys()), ascending=[sort_order == SortOrder.ASC for sort_order in sort_orders.values()]))
    
    # property return True if the dimension columns required for color_key coding exist
    # note: does not check to see if dimension columns have values
    @property
    def is_color_key_encodeable(self):
        if ('hue_page_number' in self.columns) and ('value_row' in self.columns) and ('chroma_column' in self.columns):       
            return True
        return False
    
    # property returns True if the 'color_key' columns is found
    # note: does not check to see if the column has values
    @property
    def has_color_key(self):
        return 'color_key' in self.columns

    # decode the 'color_key into 'hue_page_number', 'value_row', and 'chroma_column'
    # returns None - since self has been altered
    def decode_color_key(self) -> None:
        if self.has_color_key:
            self.df[['hue_page_number', 'value_row', 'chroma_column']] = self.df['color_key'].str.split('-', expand=True).astype(int)
        else:
            print(f"'color_key' is undefined")
    
    # sets 'color_key' column from 'hue_page_number', 'value_row', and 'chroma_column' columns
    # returns None since self may be altered
    def set_color_key(self) -> None:
        if not self.is_color_key_encodeable:
            print(f"'color_key' is not encodeable")
        else:
            self.df['color_key'] = self.df.apply(lambda row: f"{row['hue_page_number']:02d}-{row['value_row']:02d}-{row['chroma_column']:02d}", axis=1)
    
    # return a single color_key string
    @classmethod
    def format_color_key(cls, hue_page_number:int, value_row:int, chroma_column:int) -> str:
        return f"{hue_page_number:02d}-{value_row:02d}-{chroma_column:02d}"
    
    # return a list of all (r,g,b) tuples in the dataframe
    def get_rgb_tuples(self):
        # Select the 'r', 'g', 'b' columns and convert them to numpy array
        rgb_values = self.df[['r', 'g', 'b']].values

        # Convert numpy array to list of tuples
        rgb_tuples = [tuple(row) for row in rgb_values]
        return rgb_tuples

    # return the maximum value for a given column
    def max_column(self, column):
        return self.df[column].max()
        
    @property
    def shape(self):
        return self.df.shape

    @property
    def empty(self):
        return self.df.empty
    
    @property
    def columns(self):
        return self.df.columns
    
    @classmethod
    def format_pair(cls, value_row, chroma_column):
        return f"{value_row}-{chroma_column}"

    @classmethod
    def parse_pair(cls, pair):
        parts = pair.split("-")
        if len(parts) != 2: # pragma: no coverage
            raise ValueError(f"Invalid input: {pair}")
        value_row = None if parts[0] == "None" else int(parts[0])
        chroma_column = None if parts[1] == "None" else int(parts[1])
        return value_row, chroma_column
    
    def equals(self, other_mdf, verbose:bool=False) -> bool:
        same = self.df.equals(other_mdf.df)
        if verbose: # pragma: no coverage
            print(f"self.df:\n{self.df}")
            print("equals" if same else "does not equal") 
            print(f"other.df:\n{other_mdf.df}")
        return same
   
    # returns new MunsellDataFrame with an average r,b,g color per each unique color_key
    def groupby_color_key(self):
        # all MunsellDataFrame coluamns
        #['hue_page_number', 'hue_page_name', 'value_row', 'chroma_column', 'color_key', 'r', 'g', 'b']
        
        # using color_key as the index to group all r,g,b values for all rows with that index
        reduced_mdf = self.get_color_key_reduced()
        reduced_df = reduced_mdf.df
        
        # replace with average color values for each unique eolor_key index
        colors_means_df = reduced_df.groupby('color_key').mean()
        
        # add the color_key index as a column
        colors_means_df.reset_index(inplace=True)
        
        return MunsellDataFrame(colors_means_df)

    # return a version of self that has only columns 'color_key','r','g','b'
    def get_color_key_reduced(self):
        df_reduced = self.df[['color_key','r','g','b']]
        return MunsellDataFrame(df_reduced)
    
    # return an expacted version of self that has all columns - expanded from color_key
    def get_color_key_expanded(self):
        df_copy = self.df.copy(deep=True)

        df_copy[['hue_page_number', 'value_row', 'chroma_column']] = df_copy['color_key'].str.split('-', expand=True).astype(int)
        mapping = {i: name for i, name in enumerate(HUE_PAGE_NAMES)}
        df_copy['hue_page_name'] = df_copy['hue_page_number'].map(mapping)
        
        # reorder to match the original column order
        df_copy = df_copy[['hue_page_number', 'hue_page_name', 'value_row', 'chroma_column', 'color_key', 'r', 'g', 'b']]
        
        return MunsellDataFrame(df_copy)


    @classmethod
    def get_hue_page_name_from_hue_page_number(cls, hue_page_number):
        return HUE_PAGE_NAMES[hue_page_number]
    
    
    # @classmethod
    # def get_hue_page_number_from_color_key(cls, color_key):
    #     parts = color_key.split("-")
    #     return int(parts[0])
    
    # @classmethod
    # def get_value_row_from_color_key(cls, color_key):
    #     parts = color_key.split("-")
    #     return int(parts[1])
    # @classmethod
    
    # def get_chroma_columns_from_color_key(cls, color_key):
    #     parts = color_key.split("-")
    #     return int(parts[2])
