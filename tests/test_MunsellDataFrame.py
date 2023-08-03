import unittest
from MunsellDataFrame import MunsellDataFrame, SortOrder

class TestMunsellDataFrame(unittest.TestCase):
    
    def create_test_df(self):
        rows = [
            {'page_hue_number': 1, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0},
            {'page_hue_number': 2, 'page_hue_name': '5.0R', 'value_row': 8, 'chroma_column': 3, 'color_key': 'change', 'r': 0, 'g': 255, 'b': 0},
            {'page_hue_number': 3, 'page_hue_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': 'change', 'r': 0, 'g': 0, 'b': 255},
            {'page_hue_number': 3, 'page_hue_name': '10.0R', 'value_row': 6, 'chroma_column': 8, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 255}
        ]
        df = MunsellDataFrame(rows)
        return df
        
    def test_filter_by_column_values(self):
        
        df = self.create_test_df()
        # print("\noriginal:\n", df)

        filters = {
            'page_hue_name': '10.0R',
            'value_row': 6
        }

        filtered_df = df.filter_by_column_values(filters)
        # print("\nfiltered:\n", filtered_df)
        
        self.assertEqual(filtered_df.shape[0], 1, "wrong number of rows")
        # print('done')
        
    def test_apply_row_lambda_function(self):
        
        df = self.create_test_df()
        # print("\noriginal:\n", df)

        df['color_key'] = df.apply(lambda row: f"{row['page_hue_name']}-{row['value_row']}-{row['chroma_column']}", axis=1)
        # print("\ncolor_key updated:\n", df)
        
        filters = {
            'color_key': 'change'
        }
        filtered_df = df.filter_by_column_values(filters)
        # print("\nfiltered:\n", filtered_df)
        # print("\nempty?:\n", filtered_df.empty)

        self.assertEqual(filtered_df.empty, True, "expected empty")
        self.assertEqual(filtered_df.shape[0], 0, "expected zero rows")

    def test_sort_by_columns(self):
        df = self.create_test_df()
        sort_orders = {
            'chroma_column': SortOrder.ASC
        }
        sorted_df = df.sort_by_columns(sort_orders)
        self.assertEqual(sorted_df['chroma_column'].tolist(), [3,5,7,8], "wrong chroma_column order")

    def test_append_rows_empty_dict(self):
        df = MunsellDataFrame()
        with self.assertRaises(ValueError):
            df.append_rows([{}])

    def test_sort_by_columns_empty_df(self):
        df = MunsellDataFrame()
        with self.assertRaises(KeyError):
            df.sort_by_columns({'nonexistent_column': SortOrder.ASC})

    # def test_sort_by_columns_nonexistent_column(self):
    #     df = MunsellDataFrame()
    #     rows = [
    #         {'page_hue_number': 1, 'page_hue_name': 'Red', 'value_row': 10, 'chroma_column': 5, 'color_key': '1R10/5', 'r': 255, 'g': 0, 'b': 0},
    #         {'page_hue_number': 2, 'page_hue_name': 'Green', 'value_row': 8, 'chroma_column': 3, 'color_key': '2G8/3', 'r': 0, 'g': 255, 'b': 0},
    #         {'page_hue_number': 3, 'page_hue_name': 'Blue', 'value_row': 6, 'chroma_column': 7, 'color_key': '3B6/7', 'r': 0, 'g': 0, 'b': 255}
    #     ]
    #     df.append_rows(rows)
    #     with self.assertRaises(KeyError):
    #         df.sort_by_columns({'nonexistent_column': SortOrder.ASC})

    # def test_to_from_parquet(self):
    #     df = MunsellDataFrame()
    #     rows = [
    #         {'page_hue_number': 1, 'page_hue_name': 'Red', 'value_row': 10, 'chroma_column': 5, 'color_key': '1R10/5', 'r': 255, 'g': 0, 'b': 0},
    #         {'page_hue_number': 2, 'page_hue_name': 'Green', 'value_row': 8, 'chroma_column': 3, 'color_key': '2G8/3', 'r': 0, 'g': 255, 'b': 0},
    #         {'page_hue_number': 3, 'page_hue_name': 'Blue', 'value_row': 6, 'chroma_column': 7, 'color_key': '3B6/7', 'r': 0, 'g': 0, 'b': 255}
    #     ]
    #     df.append_rows(rows)
    #     df.to_parquet('/tmp/test.parquet')
    #     df2 = MunsellDataFrame.from_parquet('/tmp/test.parquet')
    #     self.assertEqual(len(df2), 3)

if __name__ == '__main__':
    unittest.main()
