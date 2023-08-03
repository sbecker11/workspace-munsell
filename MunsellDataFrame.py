import pandas as pd
from enum import Enum

class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'

class MunsellDataFrame(pd.DataFrame):
    _metadata = ['_dtypes']
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
        super().__init__(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
        self._set_dtypes()

    def _set_dtypes(self):
        for col, dtype in self._dtypes.items():
            if col in self.columns:
                self[col] = self[col].astype(dtype)

    def append_rows(self, rows):
        if self.empty:
            self.__init__(columns=self._dtypes.keys())
        for row in rows:
            self.loc[len(self)] = row
        self._set_dtypes()

    def to_parquet(self, filename):
        self.to_parquet(filename, engine='pyarrow')

    @classmethod
    def from_csv(cls, filename):
        df = pd.read_csv(filename)
        return cls(data=df.values, columns=df.columns)

    @classmethod
    def from_parquet(cls, filename):
        df = pd.read_parquet(filename, engine='pyarrow')
        return cls(data=df.values, columns=df.columns)

    def unique_values(self, column):
        return self[column].unique()

    def filter_by_column_values(self, filters):
        mask = pd.Series([True]*len(self))
        for col, val in filters.items():
            mask = mask & (self[col] == val)
        return self[mask]

    def sort_by_columns(self, sort_orders):
        return self.sort_values(by=list(sort_orders.keys()), ascending=[sort_order == SortOrder.ASC for sort_order in sort_orders.values()])
