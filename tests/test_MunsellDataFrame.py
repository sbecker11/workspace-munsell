import unittest
from munsell_data_frame.MunsellDataFrame import MunsellDataFrame, SortOrder
import pandas as pd
from munsell_data_frame.constants import *
import numpy as np
import math


class TestMunsellDataFrame(unittest.TestCase): # pragma: no cover
    
    def setUp(self):
        self.data = [
            {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0},
            {'hue_page_number': 1, 'hue_page_name': '5.0R', 'value_row': 8, 'chroma_column': 3, 'color_key': 'change', 'r': 0, 'g': 255, 'b': 0},
            {'hue_page_number': 2, 'hue_page_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': 'change', 'r': 0, 'g': 0, 'b': 255},
            {'hue_page_number': 2, 'hue_page_name': '10.0R', 'value_row': 6, 'chroma_column': 8, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 255}
        ]
        self.df = pd.DataFrame(self.data)
        self.munsell_df = MunsellDataFrame(data=self.df)
        
    def test_filter_by_columns(self):
        filters = {
            'hue_page_name': '10.0R',
            'value_row': 6
        }
        filtered_df = self.munsell_df.filter_by_columns(filters)
        # print("\nfiltered:\n", filtered_df)
        
        self.assertEqual(filtered_df.shape[0], 1, "wrong number of rows")
        # print('done')
        
    def test_filter_by_invalid_column_value(self):
        self.munsell_df.set_color_key()
        filters = {
            'color_key': 'change'
        }
        filtered_df = self.munsell_df.filter_by_columns(filters)
        self.assertEqual(filtered_df.empty, True, "expected empty")
        self.assertEqual(filtered_df.shape[0], 0, "expected zero rows")

    def test_set_color_key(self):
        # Create a sample dataframe
        data = {
            'hue_page_number': [1, 10, 99, 3],
            'value_row': [2, 20, 5, 0],
            'chroma_column': [3, 30, 8, 1]
        }
        df = pd.DataFrame(data)
        mdf = MunsellDataFrame(df)

        # Call the function
        mdf.set_color_key()

        # Check the results
        expected_values = ['01-02-03', '10-20-30', '99-05-08', '03-00-01']
        for idx, expected in enumerate(expected_values):
            actual = mdf.df.loc[idx, 'color_key']
            self.assertEqual( actual, expected, f"Expected {expected}, but got {actual}")

    def test_sort_by_columns(self):
        sort_orders = {
            'chroma_column': SortOrder.ASC
        }
        sorted_mdf = self.munsell_df.sort_by_columns(sort_orders)
        
        self.assertEqual(sorted_mdf.df['chroma_column'].tolist(), [3,5,7,8], "wrong chroma_column order")
    
    def test_groupby_color_key(self):
        input_mdf = MunsellDataFrame([
            {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': '00-09-05', 'r': 255, 'g': 0, 'b': 0},
            {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': '00-09-05', 'r': 0, 'g': 255, 'b': 0},
            {'hue_page_number': 2, 'hue_page_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': '02-06-07', 'r': 0, 'g': 0, 'b': 255},
            {'hue_page_number': 2, 'hue_page_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': '02-06-07', 'r': 255, 'g': 0, 'b': 255}
        ])
        
        expected_mdf = MunsellDataFrame([
            {'color_key': '00-09-05', 'r': 127, 'g': 127, 'b': 0},
            {'color_key': '02-06-07', 'r': 127, 'g': 0, 'b': 255}
        ])

        result_mdf = input_mdf.groupby_color_key()
        
        self.assertTrue(result_mdf.equals(expected_mdf)), "MunsellDataFrames are not equal"
  
    def test_get_color_key_reduced_expanded(self):
        input_mdf = MunsellDataFrame([
            {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': '00-09-05', 'r': 255, 'g': 0, 'b': 0},
            {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': '00-09-05', 'r': 0, 'g': 255, 'b': 0},
            {'hue_page_number': 2, 'hue_page_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': '02-06-07', 'r': 0, 'g': 0, 'b': 255},
            {'hue_page_number': 2, 'hue_page_name': '7.5R', 'value_row': 6, 'chroma_column': 7, 'color_key': '02-06-07', 'r': 255, 'g': 0, 'b': 255}
        ])
        reduced_expected_mdf = MunsellDataFrame([
            {'color_key': '00-09-05', 'r': 255, 'g': 0, 'b': 0},
            {'color_key': '00-09-05', 'r': 0, 'g': 255, 'b': 0},
            {'color_key': '02-06-07', 'r': 0, 'g': 0, 'b': 255},
            {'color_key': '02-06-07', 'r': 255, 'g': 0, 'b': 255}
        ])
        
        reduced_mdf = input_mdf.get_color_key_reduced()
        self.assertTrue(reduced_expected_mdf.equals(reduced_mdf)), "reduced != expected"

        expanded_mdf = reduced_mdf.get_color_key_expanded()
        self.assertTrue(expanded_mdf.equals(input_mdf)), "expanded != input"

                
    def test_append_rows_one_dict(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.shape, (0,8))
        dict1 = {'hue_page_number': 2, 'hue_page_name': '10.0R', 'value_row': 6, 'chroma_column': 8, 'r': 255, 'g': 0, 'b': 255}
        mdf.append_rows([dict1])
        self.assertEqual(mdf.shape, (1,8))
        
    def test_append_rows_one_partial_dict(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.shape, (0,8))
        dict1 = {'hue_page_number': 2}
        mdf.append_rows([dict1])
        self.assertEqual(mdf.shape, (1,8), "append partial dict should still add a new row")

    def test_append_rows_empty_dict(self):
        mdf = MunsellDataFrame()
        initial_rows = mdf.shape[0]
        mdf.append_rows([{}])
        new_rows = mdf.shape[0]
        self.assertEqual(new_rows, initial_rows, "append empty dict should not add a new row ")

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
            {'hue_page_number': 0, 'hue_page_name': '2.5R', 'value_row': 9, 'chroma_column': 5, 'color_key': 'change', 'r': 255, 'g': 0, 'b': 0}
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

    def test_to_list_of_tuples(self):
        # Test with an empty dataframe
        mdf = MunsellDataFrame()
        result = mdf.to_list_of_tuples()
        self.assertEqual(result, [], "Failed for empty dataframe scenario")

        # Test with a dataframe with a single row
        data_single_row = {'column1': [1], 'column2': ['a']}
        mdf = MunsellDataFrame(data_single_row)
        result = mdf.to_list_of_tuples()
        self.assertEqual(result, [(1, 'a')], "Failed for single row scenario")

        # Test with a dataframe with multiple rows
        data_multiple_rows = {'column1': [1, 2], 'column2': ['a', 'b']}
        mdf = MunsellDataFrame(data_multiple_rows)
        result = mdf.to_list_of_tuples()
        self.assertEqual(result, [(1, 'a'), (2, 'b')], "Failed for multiple rows scenario")

    def test_format_color_key(self):
        expected = "08-01-02"
        result = MunsellDataFrame.format_color_key(8, 1, 2)
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
    
    def test_empty(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.empty, True)
        
    def test_shape(self):
        mdf = MunsellDataFrame()
        self.assertEqual(mdf.shape, (0,8))

    def test_max_column(self):
        mdf = MunsellDataFrame(self.data)
        self.assertEqual(mdf.max_column('chroma_column'), 8)
        
    def test_get_hue_page_name_from_hue_page_number(self):
        for i in range(len(HUE_PAGE_NAMES)):
            self.assertEqual(MunsellDataFrame.get_hue_page_name_from_hue_page_number(i), HUE_PAGE_NAMES[i])
            
    def test_unique_values(self):
        # Test with a column with no duplicates
        mdf = MunsellDataFrame({'column1': [1, 2, 3, 4]})
        result = mdf.unique_values('column1')
        self.assertListEqual(list(result), [1, 2, 3, 4], "Failed for column with no duplicates")

        # Test with a column with duplicates
        mdf = MunsellDataFrame({'column1': [1, 2, 2, 3, 3, 3]})
        result = mdf.unique_values('column1')
        self.assertListEqual(list(result), [1, 2, 3], "Failed for column with duplicates")

        # Test with a column containing NaN values
        mdf = MunsellDataFrame({'column1': [1, 2, np.nan, 3]})
        result = mdf.unique_values('column1')
        expected = [1, 2, np.nan, 3]
        result_series = pd.Series(result) # pd.Series.equals handles NAN values
        expected_series = pd.Series(expected)
        self.assertTrue(result_series.equals(expected_series), "Failed for column with NaN values")

        # Test for a non-existent column
        mdf = MunsellDataFrame({'column1': [1, 2, 3]})
        with self.assertRaises(KeyError, msg="Failed for non-existent column"):
            mdf.unique_values('column_not_exist')

    def test_reset_index(self):
        # Scenario 1: Existing Index
        mdf = MunsellDataFrame({'A': [1, 2, 3]})
        mdf.reset_index()
        expected_mdf = MunsellDataFrame({'A': [1, 2, 3]})
        self.assertTrue(mdf.equals(expected_mdf), "Existing Index test fails")

        # Scenario 2: Custom Index
        mdf = MunsellDataFrame({'A': [1, 2, 3]}, index=['a', 'b', 'c'])
        mdf.reset_index()
        expected_mdf = MunsellDataFrame({'A': [1, 2, 3]})
        self.assertTrue(mdf.equals(expected_mdf), "Custom Index test fails")

        # Scenario 3: Dropped Rows
        mdf = MunsellDataFrame({'A': [1, 2, 3, 4]})
        mdf.drop_rows(1) 
        mdf.reset_index()
        expected_mdf = MunsellDataFrame({'A': [1, 3, 4]})
        self.assertTrue(mdf.equals(expected_mdf), "Dropped Rows test fails")

    def test_drop_rows(self):
        # Scenario 1: Dropping a Single Row
        mdf = MunsellDataFrame({'A': [1, 2, 3, 4]})
        mdf.drop_rows(1)
        expected_mdf = MunsellDataFrame({'A': [1, 3, 4]})
        self.assertTrue(mdf.equals(expected_mdf), "Dropping single row failed")

        # Scenario 2: Dropping Multiple Rows
        mdf = MunsellDataFrame({'A': [1, 2, 3, 4]})
        mdf.drop_rows([0, 2])
        expected_mdf = MunsellDataFrame({'A': [2, 4]})
        self.assertTrue(mdf.equals(expected_mdf), "Dropping multiple rows failed")

        # Scenario 3: Dropping Non-existent Row
        mdf = MunsellDataFrame({'A': [1, 2, 3]})
        with self.assertRaises(KeyError):  # Assuming a KeyError is raised for non-existent rows
            mdf.drop_rows(5)
        expected_mdf = MunsellDataFrame({'A': [1, 2, 3]})
        self.assertTrue(mdf.equals(expected_mdf), "Handling non-existent row failed")

        # Scenario 4: Dropping All Rows
        mdf = MunsellDataFrame({'A': [1, 2, 3, 4]})
        original_num_cols = mdf.shape[1]
        mdf.drop_rows([0, 1, 2, 3])
        new_num_cols = mdf.shape[1]
        self.assertEqual(mdf.shape, (0,1), "dropping all rows should  results in zero rows")
        self.assertEqual(original_num_cols, new_num_cols, "dropping all rows should maintain number of columns")
        
    def test_drop_all_columns(self):
        mdf = MunsellDataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        mdf.drop_columns(['A', 'B', 'C'], reset_index=True)
        expected_mdf = MunsellDataFrame([])
        expected_mdf.df.index = [0, 1]  # Explicitly setting the index to [0, 1]
        self.assertTrue(mdf.equals(expected_mdf), "Dropping all columns failed")

    def test_drop_columns(self):
        # Scenario 1: Dropping a Single Column
        mdf = MunsellDataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        mdf.drop_columns('A')
        expected_mdf = MunsellDataFrame({'B': [3, 4], 'C': [5, 6]})
        self.assertTrue(mdf.equals(expected_mdf), "Dropping single column failed")

        # Scenario 2: Dropping Multiple Columns
        mdf = MunsellDataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        mdf.drop_columns(['A', 'C'])
        expected_mdf = MunsellDataFrame({'B': [3, 4]})
        self.assertTrue(mdf.equals(expected_mdf), "Dropping multiple columns failed")

        # Scenario 3: Dropping Non-existent Column
        mdf = MunsellDataFrame({'A': [1, 2], 'B': [3, 4]})
        with self.assertRaises(KeyError):  # Assuming a KeyError is raised for non-existent columns
            mdf.drop_columns('Z')
        expected_mdf = MunsellDataFrame({'A': [1, 2], 'B': [3, 4]})
        self.assertTrue(mdf.equals(expected_mdf), "Handling non-existent column failed")

    def test_remove_by_columns(self):
        # Scenario 1: Single Column Filter
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mdf.remove_by_columns({'A': 2})
        expected_mdf = MunsellDataFrame({'A': [1, 3], 'B': [4, 6]})
        self.assertTrue(mdf.equals(expected_mdf), "Single column filter failed")

        # Scenario 2: Multiple Column Filter
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mdf.remove_by_columns({'A': 2, 'B': 6})
        expected_mdf = MunsellDataFrame({'A': [1], 'B': [4]})
        self.assertTrue(mdf.equals(expected_mdf), "Multiple column filter failed")

        # Scenario 3: Non-existent Column
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        with self.assertRaises(KeyError):  # Assuming a KeyError is raised for non-existent columns
            mdf.remove_by_columns({'Z': 2})

        # Scenario 4: Value Not Present
        mdf = MunsellDataFrame({'A': [1, 2, 3]})
        mdf.remove_by_columns({'A': 10})  # Value 10 is not in column A
        expected_mdf = MunsellDataFrame({'A': [1, 2, 3]})
        self.assertTrue(mdf.equals(expected_mdf), "Filtering by non-present value failed")

        # Scenario 5: Remove All Rows
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mdf.remove_by_columns({'A': 1, 'B': 5})
        expected_mdf = MunsellDataFrame({'A': [3], 'B': [6]})
        self.assertTrue(mdf.equals(expected_mdf), "removing the two rows with column values should leave 1 row")
        mdf.remove_by_columns({'A': 3})
        self.assertEqual(mdf.shape, (0,2), "removing last row by column value should leave zero rows but same columns")
        
        # Scenario 1: Single Column Filter with reset_index=True (default)
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mdf.remove_by_columns({'A': 2})
        expected_mdf = MunsellDataFrame({'A': [1, 3], 'B': [4, 6]})
        self.assertTrue(mdf.equals(expected_mdf), "Single column filter with reset_index=True failed")

        # Scenario 2: Single Column Filter with reset_index=False
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        mdf.remove_by_columns({'A': 2}, reset_index=False)
        expected_df = pd.DataFrame({'A': [1, 3], 'B': [4, 6]}, index=[0, 2])
        self.assertTrue(mdf.df.equals(expected_df), "Single column filter with reset_index=False failed")

    def test_columns_property(self):
        mdf = MunsellDataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        expected_columns = ['A', 'B']
        self.assertListEqual(list(mdf.columns), expected_columns, "Columns property does not return expected columns")

    def test_format_pair(self):
        
        # Single digit values
        result = MunsellDataFrame.format_pair(1, 2)
        expected = "1-2"
        self.assertEqual(result, expected, f"Failed for single digit values. Got: {result}, Expected: {expected}")

        # Double digit values
        result = MunsellDataFrame.format_pair(10, 20)
        expected = "10-20"
        self.assertEqual(result, expected, f"Failed for double digit values. Got: {result}, Expected: {expected}")

        # Scenario 6: Both value_row and chroma_column are None
        result = MunsellDataFrame.format_pair(None, None)
        expected = "None-None"
        self.assertEqual(result, expected, f"Failed when both value_row and chroma_column are None. Got: {result}, Expected: {expected}")

    def test_parse_pair(self):
        
        # Single digit values
        result = MunsellDataFrame.parse_pair("1-2")
        expected = (1, 2)
        self.assertEqual(result, expected, f"Failed for single digit values. Got: {result}, Expected: {expected}")

        # Double digit values
        result = MunsellDataFrame.parse_pair("10-20")
        expected = (10, 20)
        self.assertEqual(result, expected, f"Failed for double digit values. Got: {result}, Expected: {expected}")

        # Scenario 6: Both value_row and chroma_column are None
        result = MunsellDataFrame.parse_pair("None-None")
        expected = (None, None) 
        self.assertEqual(result, expected, f"Failed when both value_row and chroma_column are None. Got: {result}, Expected: {expected}")


    
if __name__ == '__main__':
    unittest.main() # pragma: no cover
