import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

class TestSpecificDataLoader(unittest.TestCase):
    def setUp(self):
        #Providing a mock db_url
        self.loader = SpecificDataLoader('sqlite:///:memory:')  #Using in-memory SQLite database for testing
        self.loader.engine = MagicMock()  #Mocking the engine attribute

    @patch('pandas.read_sql')
    def test_load_train_data(self, mock_read_sql):
        expected_df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']}) 
        mock_read_sql.return_value = expected_df
        
        result_df = self.loader.load_train_data()
        
        mock_read_sql.assert_called_once_with('SELECT * FROM Train_data', con=self.loader.engine)
        pd.testing.assert_frame_equal(result_df, expected_df)

#Running the tests 
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSpecificDataLoader)
    runner = unittest.TextTestRunner()
    runner.run(suite)


import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np


class TestIdealFunctionFinder(unittest.TestCase):
    def setUp(self):
        #Setting up mock data
        self.ideal_df = pd.DataFrame({
            'X': np.linspace(0, 10, 5),
            'func1': np.sin(np.linspace(0, 10, 5)),
            'func2': np.cos(np.linspace(0, 10, 5)),
            'func3': np.linspace(0, 10, 5) ** 2
        })

        self.train_df = pd.DataFrame({
            'X': np.linspace(0, 10, 5),
            'train_col': np.sin(np.linspace(0, 10, 5)) + np.random.normal(0, 0.1, 5)
        })

    def test_find_ideal_function(self):
        #Testing that the ideal function is correctly identified 
        ideal_func = find_ideal_function(self.train_df['train_col'], self.ideal_df)
        self.assertEqual(ideal_func, 'func1', "The ideal function should be 'func1'")

    def test_create_new_data(self):
        #Testing that the new data is created correctly with the ideal function 
        new_data = create_new_data(self.train_df, self.ideal_df)
        self.assertTrue('train_col(Ideal Func)' in new_data.columns)
        np.testing.assert_array_almost_equal(new_data['train_col(Ideal Func)'], self.ideal_df['func1'], decimal=5)

#Running the tests 
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIdealFunctionFinder)
    runner = unittest.TextTestRunner()
    runner.run(suite)


import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd

class TestMatchTestWithIdeal(unittest.TestCase):
    def test_match_test_with_ideal(self):
        #Mocking the DataFrame creation
        with patch('pandas.DataFrame') as mock_df:
            #Seting up the mock to return a DataFrame when called
            mock_df.return_value = pd.DataFrame({
                'X': np.linspace(0, 10, 100),
                'Y1(training func)(Ideal Func)': np.sin(np.linspace(0, 10, 100)),
                'Y2(training func)(Ideal Func)': np.cos(np.linspace(0, 10, 100)),
                'Y3(training func)(Ideal Func)': np.tan(np.linspace(0, 10, 100)),
                'Y4(training func)(Ideal Func)': np.log1p(np.linspace(0, 10, 100)),
                'X(test func)': np.linspace(0, 10, 100),
                'Y(test func)': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.1, 100)
            })

            #Importing the module that contains the function to test
            import SQLproject
            SQLproject.match_test_with_ideal()
            mock_df.assert_called()  

#Running the tests 
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMatchTestWithIdeal)
    runner = unittest.TextTestRunner()
    runner.run(suite)
