import unittest
from munsell_data_frame.MunsellDataFrame import MunsellDataFrame, SortOrder
import pandas as pd

class TestMunsellDataFrame(unittest.TestCase):
    
    def setUp(self):
        self.data = [
            {'page_hue_number': 1, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0},
            {'page_hue_number': 2, 'page_hue_name': '5.0R', 'value_row': 8, 'chroma_column': 3, 'color_key': 'change', 'r': 0, 'g': 255, 'b': 0},
            {'page_hue_number': 3, 'page_hue_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': 'change', 'r': 0, 'g': 0, 'b': 255},
            {'page_hue_number': 3, 'page_hue_name': '10.0R', 'value_row': 6, 'chroma_column': 8, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 255}
        ]
        self.df = pd.DataFrame(self.data)
        self.munsell_df = MunsellDataFrame(data=self.df)
        
    def test_filter_by_columns(self):
        filters = {
            'page_hue_name': '10.0R',
            'value_row': 6
        }
        filtered_df = self.munsell_df.filter_by_columns(filters)
        # print("\nfiltered:\n", filtered_df)
        
        self.assertEqual(filtered_df.shape[0], 1, "wrong number of rows")
        # print('done')
        
    def test_set_color_key(self):
        self.munsell_df.set_color_key()
        filters = {
            'color_key': 'change'
        }
        filtered_df = self.munsell_df.filter_by_columns(filters)
        # print("\nfiltered:\n", filtered_df)
        # print("\nempty?:\n", filtered_df.empty)
        self.assertEqual(filtered_df.empty, True, "expected empty")
        self.assertEqual(filtered_df.shape[0], 0, "expected zero rows")

    def test_sort_by_columns(self):
        sort_orders = {
            'chroma_column': SortOrder.ASC
        }
        sorted_mdf = self.munsell_df.sort_by_columns(sort_orders)
        
        self.assertEqual(sorted_mdf.df['chroma_column'].tolist(), [3,5,7,8], "wrong chroma_column order")
    
    def test_groupby_color_key(self):
        input_mdf = MunsellDataFrame([
            {'page_hue_number': 1, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': '01-09-05', 'r': 255, 'g': 0, 'b': 0},
            {'page_hue_number': 1, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': '01-09-05', 'r': 0, 'g': 255, 'b': 0},
            {'page_hue_number': 3, 'page_hue_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': '03-06-07', 'r': 0, 'g': 0, 'b': 255},
            {'page_hue_number': 3, 'page_hue_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': '03-06-07', 'r': 255, 'g': 0, 'b': 255}
        ])
        
        expected_mdf = MunsellDataFrame([
            {'color_key': '01-09-05', 'r': 127, 'g': 127, 'b': 0},
            {'color_key': '03-06-07', 'r': 127, 'g': 0, 'b': 255}
        ])

        result_mdf = input_mdf.groupby_color_key()
        
        self.assertTrue(result_mdf.equals(expected_mdf)), "MunsellDataFrames are not equal"
  
                
    def test_append_rows_one_dict(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.shape, (0,8))
        dict1 = {'page_hue_number': 3, 'page_hue_name': '10.0R', 'value_row': 6, 'chroma_column': 8, 'r': 255, 'g': 0, 'b': 255}
        mdf.append_rows([dict1])
        self.assertEqual(mdf.shape, (1,8))
        
    def test_append_rows_one_partial_dict(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.shape, (0,8))
        dict1 = {'page_hue_number': 3}
        with self.assertRaises(pd.errors.IntCastingNaNError):
            mdf.append_rows([dict1])

    def test_append_rows_empty_dict(self):
        df = MunsellDataFrame()
        with self.assertRaises(ValueError):
            df.append_rows([{}])

    def test_sort_by_columns_empty_df(self):
        df = MunsellDataFrame()
        with self.assertRaises(KeyError):
            df.sort_by_columns({'nonexistent_column': SortOrder.ASC})

    def test_sort_by_columns_nonexistent_column(self):
        with self.assertRaises(KeyError):
            self.munsell_df.sort_by_columns({'nonexistent_column': SortOrder.ASC})

    def test_to_from_parquet(self):
        test_filename = '/tmp/test.parquet'
        self.munsell_df.to_parquet(test_filename)
        df2 = MunsellDataFrame.from_parquet(test_filename)
        self.assertEqual(df2.shape, self.munsell_df.shape, 'shapes failure')

    def test_to_from_csv(self):
        test_filename = "/tmp/test.csv"
        self.munsell_df.to_csv(test_filename)
        df2 = MunsellDataFrame.from_csv(test_filename)
        self.assertEqual(df2.shape, self.munsell_df.shape, 'shapes failure')

    def test_to_list_of_dicts_positive(self):
        input = [
            {'page_hue_number': 1, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0}
        ]
        df = MunsellDataFrame(data=input)
        result = df.to_list_of_dicts()

        # Test that the to_dict function returns a list of dictionaries
        # with the correct data and structure
        self.assertEqual(result, input)

    def test_to_list_of_dicts_negative(self):
        # Test that the to_dict function raises a TypeError
        # when an invalid argument is passed
        with self.assertRaises(TypeError):
            self.munsell_df.to_dict(invalid_arg="invalid")

    def test_to_dict_with_orient_list(self):
        data = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data)

        munsell_df = MunsellDataFrame(df)
        output = munsell_df.to_dict(orient='list')

        # expected_output = {'col1': [1, 2], 'col2': [3, 4]}
        self.assertEqual(output, data)
        
    def test_format_color_key(self):
        expected = "09-01-02"
        result = MunsellDataFrame.format_color_key(9, 1, 2)
        self.assertEqual(expected, result)

    def test_get_rgb_tuples(self):
        expected_tuples = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 0, 255)
        ]
        result_tuples = self.munsell_df.get_rgb_tuples()
        self.assertEqual(expected_tuples, result_tuples)

    def test_uniquify_hue_page_rows(self):
        dontcare_int = 0
        dontcare_str = "dontcare"
        page_hue_name = '2.5R'
        value_row = 9
        chroma_column = 2
        hue_page_rows_as_dicts = [
            {'page_hue_number': dontcare_int, 'page_hue_name': page_hue_name, 'value_row': value_row, 'chroma_column': chroma_column, 'color_key': dontcare_str, 'r': 255, 'g': 0, 'b': 0},
            {'page_hue_number': dontcare_int, 'page_hue_name': page_hue_name, 'value_row': value_row, 'chroma_column': chroma_column, 'color_key': dontcare_str, 'r': 0, 'g': 255, 'b': 0},
            {'page_hue_number': dontcare_int, 'page_hue_name': page_hue_name, 'value_row': value_row, 'chroma_column': chroma_column, 'color_key': dontcare_str, 'r': 0, 'g': 0, 'b': 255},
        ]
        # hue_page_rows_mdf is the result of filtering the entire dataframe by page_hue_name and value_row
        hue_page_rows_mdf = MunsellDataFrame(hue_page_rows_as_dicts)
        
        # assert the rgb data of hue_page_rows_mdf
        rgb_tuples_before = hue_page_rows_mdf.get_rgb_tuples()
        self.assertEqual(len(rgb_tuples_before), 3)
        
        # run uniquify on the given params
        unique_hue_page_rows_mdf = MunsellDataFrame.uniquify_hue_page_rows_mdf(page_hue_name, hue_page_rows_mdf)
        
        # assert the shape of the rgb data of the result
        rgb_tuples_after = unique_hue_page_rows_mdf.get_rgb_tuples()
        self.assertEqual(len(rgb_tuples_after), 1)
        
        # assert the rgb values of the result
        rgb_tuples_expected = [(85, 85, 85)]
        self.assertEqual(rgb_tuples_after, rgb_tuples_expected)

    def test_uniqueify_hue_value_chroma_pairs(self):
        dontcare_int = 0
        dontcare_str = "dontcare"
        data = [
            {'page_hue_number': dontcare_int, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': dontcare_str, 'r': 255, 'g': 0, 'b': 0},
            {'page_hue_number': dontcare_int, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': dontcare_str, 'r': 0, 'g': 255, 'b': 0},
            {'page_hue_number': dontcare_int, 'page_hue_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': dontcare_str, 'r': 0, 'g': 0, 'b': 255},
        ]
        mdf = MunsellDataFrame(data)
        
        # verify the shape of the rgb data defined above
        rgb_tuples_before = mdf.get_rgb_tuples()
        self.assertEqual(len(rgb_tuples_before), 3)
        
        # call uniquify on the prepared df
        mdf.uniqueify_hue_value_chroma_pairs()
        
        # verify the shape of the rgb data after the call
        rgb_tuples_after = mdf.get_rgb_tuples()
        self.assertEqual(len(rgb_tuples_after), 1)
        
        # verify the rgb data after the call
        rgb_tuples_expected = [(85, 85, 85)]
        self.assertEqual(rgb_tuples_after, rgb_tuples_expected)
    
    def test_empty(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.empty, True)
        
    def test_shape(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.shape, (0,8))

    def test_max_column(self):
        mdf = MunsellDataFrame(self.data)
        self.assertEqual(mdf.max_column('chroma_column'), 8)
        
            
if __name__ == '__main__':
    unittest.main()
