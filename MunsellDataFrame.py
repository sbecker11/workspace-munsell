import pandas as pd
from enum import Enum

class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'

class MunsellDataFrame:
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

    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        data = data if data is not None else []
        self.df = pd.DataFrame(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self._set_dtypes()

    def _set_dtypes(self):
        for col, dtype in self._dtypes.items():
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(dtype)

    def append_rows(self, rows):
        if self.df.empty:
            self.__init__(columns=self._dtypes.keys())
        for row in rows:
            self.df.loc[len(self.df)] = row
        self._set_dtypes()

    def to_csv(self, filename):
        self.df.to_csv(filename, index=False)

    @classmethod
    def from_csv(cls, filename):
        df = pd.read_csv(filename)
        return cls(data=df.values, columns=df.columns)

    def to_parquet(self, filename):
        self.df.to_parquet(filename, engine='pyarrow')

    @classmethod
    def from_parquet(cls, filename):
        df = pd.read_parquet(filename, engine='pyarrow')
        return cls(data=df.values, columns=df.columns)

    def unique_values(self, column):
        return self.df[column].unique()

    def reset_index(self):
        self.df = self.df.reset_index(drop=True)

    def filter_by_column_values(self, filters):
        mask = pd.Series([True]*len(self.df))
        for col, val in filters.items():
            mask = mask & (self.df[col] == val)
        return self.df[mask]

    def sort_by_columns(self, sort_orders):
        return self.df.sort_values(by=list(sort_orders.keys()), ascending=[sort_order == SortOrder.ASC for sort_order in sort_orders.values()])

    def create_color_key(self):
        self.df['color_key'] = self.df.apply(lambda row: f"{row['page_hue_name']}-{row['value_row']}-{row['chroma_column']}", axis=1)
        
    @property
    def shape(self):
        return self.df.shape

    @property
    def empty(self):
        return self.df.empty

