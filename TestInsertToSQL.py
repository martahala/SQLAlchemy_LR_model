import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sqlalchemy as db

class TestCSVInsertToSQL(unittest.TestCase):
    @patch('pandas.read_csv')
    @patch('sqlalchemy.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_CSV_insert_to_SQL(self, mock_to_sql, mock_create_engine, mock_read_csv):
        #Seting up DataFrame mock 
        df_mock = pd.DataFrame({
            'X': [1, 2, 3],
            'Y1(training func)': ['a', 'b', 'c'],
            'Y2(training func)': ['d', 'e', 'f'],
            'Y3(training func)': ['g', 'h', 'i'],
            'Y4(training func)': ['j', 'k', 'l']
        })
        mock_read_csv.return_value = df_mock   
        #Calling the function
        CSV_insert_to_SQL()
        
        #Assertions
        mock_read_csv.assert_called_with('/Users/marththe/Desktop/Python/test.csv')
        mock_to_sql.assert_called()
        self.assertTrue(mock_create_engine.called)

#Running the tests 
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCSVInsertToSQL))
runner = unittest.TextTestRunner()
runner.run(suite)