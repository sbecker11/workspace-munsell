import pandas as pd
from enum import Enum
import numpy as np 
import math
from .constants import PAGE_HUE_NAMES

# used in the sort_orders dict for sort_by_columns
class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'

class MunsellDataFrame:
    
    # column names and their dtypes
    _dtypes = {
        'page_hue_number': 'int',
        'page_hue_name': 'str',
        'value_row': 'int',
        'chroma_column': 'int',
        'color_key': 'str',
        'r': 'int',
        'g': 'int',
        'b': 'int',
    }

    # called when creating an instance of a MunsellDataFrame 
    # using
    # df = MunsellDataFrame() 
    # or using 
    # df = MunsellDataFrame([
    #     {'page_hue_number': 1, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0},
    #     {'page_hue_number': 2, 'page_hue_name': '5.0R', 'value_row': 8, 'chroma_column': 3, 'color_key': 'change', 'r': 0, 'g': 255, 'b': 0},
    #     {'page_hue_number': 3, 'page_hue_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': 'change', 'r': 0, 'g': 0, 'b': 255},
    # ]
    # returns None - so self has been altered
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        if data is None:
            data = pd.DataFrame(columns=self._dtypes.keys())
        else:
            data = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self.df = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self._set_dtypes()

    # used to set dataframe columns in __init__
    # returns None - so self has been altered
    def _set_dtypes(self): # pragma: no cover
        for col, dtype in self._dtypes.items():
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(dtype)
        
    # append rows to the dataframe where each row
    # is a MunsellDataFrame-columned dict
    # returns None - so self has been altered
    def append_rows(self, rows):
        if self.df.empty:
            self.__init__(columns=self._dtypes.keys())
        for row in rows:
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
        return self.df[column].unique()

    # remove the dataframe's index column
    # return None - so self has been altered
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
    
    # remove all rows in the dataframe that match all of the given column filters., for example:
    # filters = {
    #     "value_row": 7,
    #     "chroma_column": 2
    # }
    # return None - so self has been altered
    def remove_by_columns(self, filters):
        for col, val in filters.items():
            self.df = self.df[self.df[col] != val]

    # sort the dataframe by multiple columns given a sort_orders dictionary, for example:
    # sort_orders = {
    #     "value_row": SortOrder.ASC,
    #     "chroma_column": SortOrder.DESC
    # }
    # returns a new MunsellDataFrame that contains the sorted rows
    def sort_by_columns(self, sort_orders):
        return MunsellDataFrame(self.df.sort_values(by=list(sort_orders.keys()), ascending=[sort_order == SortOrder.ASC for sort_order in sort_orders.values()]))

    # sets the color_key column for all rows
    # returns None - so self has been updated
    def set_color_key(self) -> None:
        self.df['color_key'] = self.df.apply(lambda row: f"{row['page_hue_number']:2d}-{row['value_row']:2d}-{row['chroma_column']:2d}", axis=1)
    
    # return a single color_key string
    @classmethod
    def format_color_key(cls, page_hue_number:int, value_row:int, chroma_column:int) -> str:
        return f"{page_hue_number:02d}-{value_row:02d}-{chroma_column:02d}"
    
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
        value_row, chroma_column = map(int, pair.split("-"))
        return value_row, chroma_column

    # replace each page_hue with rows of unique row/col pairs.
    # this should always be called after creating a dataset from a raw source
    # returns None - so self has been altered
    def uniqueify_hue_value_chroma_pairs(self):
        # print(f"uniqueify_hue_value_chroma_pairs starting with shape {self.shape}")
        for page_hue_name in PAGE_HUE_NAMES:
            hue_page_rows_mdf = self.filter_by_columns({'page_hue_name': page_hue_name})
            if hue_page_rows_mdf.shape[0] > 0:
                unique_hue_page_rows_mdf = self.uniquify_hue_page_rows_mdf(page_hue_name, hue_page_rows_mdf)

                scols = str(self.df.columns)
                ucols = str(unique_hue_page_rows_mdf.df.columns)
                assert ucols == scols, "num columns don't match"

                # if the number of unique rows differs from the original rows ...
                if unique_hue_page_rows_mdf.shape[0] != hue_page_rows_mdf.shape[0]:

                    # remove the original hue_page_rows ... 
                    self.remove_by_columns({'page_hue_name': page_hue_name})
                    
                    # ... and append the unique rows using vertical concat 
                    new_df = pd.concat([self.df, unique_hue_page_rows_mdf.df], axis=0)
                    self.df = new_df

        # print(f"uniqueify_hue_value_chroma_pairs done with shape {self.shape}")
    
    # there are multiple samples for each value-chroma pair in a hue_page.
    # this classmethod returns the unique pairs and their average r,g,b values
    # found in the given hue_page_rows_mdf that have the same values and chroma.
    @classmethod
    def uniquify_hue_page_rows_mdf(cls, page_hue_name:str, hue_page_rows_mdf):
        unique_hue_page_rows_mdf = MunsellDataFrame()
        num_pairs = 0
        pair_cnts = {}
        pair_r_sum = {}
        pair_g_sum = {}
        pair_b_sum = {}
        num_pairs = 0
        list_of_tuples = hue_page_rows_mdf.to_list_of_tuples()
        #['page_hue_number', 'page_hue_name', 'value_row', 'chroma_column', 'color_key', 'r', 'g', 'b']
        for page_hue_number, _, value_row, chroma_column, _, r, g, b in list_of_tuples:
            tuple = (page_hue_number, value_row, chroma_column, r, g, b)
            pair = MunsellDataFrame.format_pair(value_row, chroma_column)

            if pair not in pair_cnts:
                pair_cnts[pair] = 0
                pair_r_sum[pair] = 0
                pair_g_sum[pair] = 0
                pair_b_sum[pair] = 0

            pair_cnts[pair] += 1
            pair_r_sum[pair] += r
            pair_g_sum[pair] += g
            pair_b_sum[pair] += b
            num_pairs += 1
        
        # get mean r,g,b for each unique pair
        for unique_pair in pair_cnts:
            cnt = 1.0 * pair_cnts[unique_pair]
            # compute average r,g,b
            r = math.floor(1.0 * pair_r_sum[unique_pair] / cnt)
            g = math.floor(1.0 * pair_g_sum[unique_pair] / cnt)
            b = math.floor(1.0 * pair_b_sum[unique_pair] / cnt)
            value_row, chroma_column = MunsellDataFrame.parse_pair(unique_pair)
            color_key = MunsellDataFrame.format_color_key(page_hue_number, value_row, chroma_column)
            
            #['page_hue_number', 'page_hue_name', 'value_row', 'chroma_column', 'color_key', 'r', 'g', 'b']
            unique_hue_page_row_dict = {
                "page_hue_number":page_hue_number, 
                "page_hue_name":page_hue_name, 
                "value_row":value_row, 
                "chroma_column":chroma_column, 
                "color_key": color_key,  
                "r":r, "g":g, "b": b }
            unique_hue_page_row_mdf = MunsellDataFrame([unique_hue_page_row_dict])
            
            # vertical concat each unique row 
            unique_hue_page_rows_mdf.df = pd.concat([unique_hue_page_rows_mdf.df, unique_hue_page_row_mdf.df], axis=0)
            
        return unique_hue_page_rows_mdf
    
    def groupby_color_key(self):
        # all MunsellDataFrame coluamns
        #['page_hue_number', 'page_hue_name', 'value_row', 'chroma_column', 'color_key', 'r', 'g', 'b']
        
        # using color_key as the index to group all r,g,b values for all rows with that index
        reduced_df = self.df[['color_key','r','g','b']]        
        
        # replace with average color values for each unique eolor_key index
        colors_means_df = reduced_df.groupby('color_key').mean()
        
        # add the color_key index as a column
        colors_means_df.reset_index(inplace=True)
        return MunsellDataFrame(colors_means_df)

    
    def equals(self, other_mdf, verbose:bool=False) -> bool:
        same = self.df.equals(other_mdf.df)
        if verbose:
            print(f"self.df:\n{self.df}")
            print("equals" if same else "does not equal")
            print(f"other.df:\n{other_mdf.df}")
        return same
   