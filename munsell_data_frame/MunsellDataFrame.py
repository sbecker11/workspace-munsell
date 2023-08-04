import pandas as pd
from enum import Enum

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
    #
    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        if data is None:
            data = pd.DataFrame(columns=self._dtypes.keys())
        else:
            data = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self.df = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self._set_dtypes()

    # used to set dataframe columns in __init__
    def _set_dtypes(self):
        for col, dtype in self._dtypes.items():
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(dtype)
        
    # append rows to the dataframe
    def append_rows(self, rows):
        if self.df.empty:
            self.__init__(columns=self._dtypes.keys())
        for row in rows:
            self.df.loc[len(self.df)] = row
        self._set_dtypes()
    
    # save the dataframe to a list of dicts
    def to_dict(self, *args, **kwargs):
        return self.df.to_dict(*args, **kwargs)
    
    # save the values of the dataframe to a csv file
    def to_csv(self, filename):
        return self.df.to_csv(filename)

    @classmethod
    # load the data of the dataframe from a csv file
    def from_csv(cls, filename):
        df = pd.read_csv(filename)
        return cls(data=df.values, columns=df.columns)

    # save the dataframe to a parquet file
    def to_parquet(self, filename):
        self.df.to_parquet(filename, engine='pyarrow')

    @classmethod
    # load the dataframe from a parquet file
    def from_parquet(cls, filename):
        filename = filename.strip()
        df = pd.read_parquet(filename, engine='pyarrow')
        return cls(data=df.values, columns=df.columns)

    # return a list of unique values for the given column
    def unique_values(self, column):
        return self.df[column].unique()

    # remove the dataframe's index column
    def reset_index(self):
        self.df = self.df.reset_index(drop=True)

    # sort the dataframe by multiple columns given a filters dictionary, for example:
    # filters = {
    #     "value_row": 7,
    #     "chroma_column": 2
    # }
    def filter_by_columns(self, filters):
        mask = pd.Series([True]*len(self.df))
        for col, val in filters.items():
            mask = mask & (self.df[col] == val)
        return self.df[mask]

    # sort the dataframe by multiple columns given a sort_orders dictionary, for example:
    # sort_orders = {
    #     "value_row": SortOrder.ASC,
    #     "chroma_column": SortOrder.DESC
    # }
    def sort_by_columns(self, sort_orders):
        return self.df.sort_values(by=list(sort_orders.keys()), ascending=[sort_order == SortOrder.ASC for sort_order in sort_orders.values()])

    # create the color_key column
    # returns None
    def create_color_key(self) -> None:
        self.df['color_key'] = self.df.apply(lambda row: f"{row['page_hue_name']}-{row['value_row']}-{row['chroma_column']}", axis=1)
    
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

