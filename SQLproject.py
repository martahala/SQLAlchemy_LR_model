import pandas as pd
import sqlalchemy as db
from sqlalchemy import create_engine
import numpy as np 

class BaseDataLoader:
    
    def __init__(self, db_url):
        self.engine = create_engine(db_url) #Create a database engine
        
    def load_data(self, query):
        """
        Load data from the SQL database into a Pandas DataFrame.

        Args:
        query (str): SQL query string.

        Returns:
        pd.DataFrame: Loaded data.
        """
        return pd.read_sql(query, con=self.engine)  #Load data from SQL into Pandas.       
class SpecificDataLoader(BaseDataLoader):
    def load_train_data(self):
        """ Load training data from the database. """
        return self.load_data('SELECT * FROM Train_data')

    def load_ideal_data(self):
        """ Load ideal data from the database. """
        return self.load_data('SELECT * FROM Ideal_data')

    def load_test_data(self):
        """ Load test data from the database. """
        return self.load_data('SELECT * FROM Test_data')
        
db_loader = SpecificDataLoader('sqlite:///python_database.db')
Train_data = db_loader.load_train_data()
Ideal_data = db_loader.load_ideal_data()
Test_data = db_loader.load_test_data()


print(Train_data.head())
print(Ideal_data.head())
print(Test_data.head())


def find_ideal_function(train_column, ideal_df):
    """
    Find the ideal function from an 'Ideal_data' file for one of the four functions in a 'Train_data' file.
    Create a new table 'New_data' with the found Ideal functions.
    """
    min_error = float('inf') 
    ideal_column = None
    for column in ideal_df.columns[1:]:   #Start  with the second column since the first one is 'X'
        #Find the best function using R-Squared 
        error = np.sum((train_column - ideal_df[column])**2) 
        try: #Standard exception handling
            if error < min_error:
               min_error = error
               ideal_column = column
        except TypeError:
            print("Error: non-comparable types encountered in error comparison.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return ideal_column

def create_new_data(Train_data, Ideal_data):
    """
    Create a new DataFrame 'New_data' using the best matching ideal functions for each column in 'Train_data'.
    """
    New_data = pd.DataFrame()
    New_data['X'] = Train_data['X']  # Copy 'X' column from Train_data
    for col in Train_data.columns[1:]:  # Assume the first column is 'X'
        ideal_func_column = find_ideal_function(Train_data[col], Ideal_data)
        New_data[col + '(Ideal Func)'] = Ideal_data[ideal_func_column]
    return New_data

New_data = create_new_data(Train_data, Ideal_data)

print(New_data)
#Save a 'New_data' file to csv for better analysis 
New_data.to_csv('New_data.csv', index=False) 


def match_test_with_ideal():
    """Find from ideal functions a function with the standard deviation less than sqrt(2). 
       Match the chosen fucntion with Y(test func). 
       Save the results in a new column called 'DeltaY' in Test_data.
       Save a number of the chosen ideal function in another new column called 'No. of ideal function' in Test_data.
       Update a SQL table 'Test_data' with new columns 'DeltaY'
    """

    
    New_data = pd.DataFrame({
        'X': np.linspace(0, 10, 100),
        'Y1(training func)(Ideal Func)': np.sin(np.linspace(0, 10, 100)),
        'Y2(training func)(Ideal Func)': np.cos(np.linspace(0, 10, 100)),
        'Y3(training func)(Ideal Func)': np.tan(np.linspace(0, 10, 100)),
        'Y4(training func)(Ideal Func)': np.log1p(np.linspace(0, 10, 100))
    })
    Test_data = pd.DataFrame({
        'X(test func)': np.linspace(0, 10, 100),
        'Y(test func)': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.1, 100)
    })
# Preparing the DataFrame to store the standard deviations and function names
    std_devs = pd.DataFrame(index=Test_data.index)
# Calculate the standard deviation of the differences for each function and select the best one   
    threshold = np.sqrt(2) 
    for i in range(1, 5):
        func_col = f'Y{i}(training func)(Ideal Func)'
        interpolated_values = np.interp(Test_data['X(test func)'], New_data['X'], New_data[func_col]) # Interpolate New_data Y values at Test_data X points 
        differences = Test_data['Y(test func)'] - interpolated_values # Calculate the differences
        std_dev = np.std(differences) # Calculate the standard deviation of the differences 
        
        if std_dev < threshold: # Standard deviation should be less than sqrt(2). Update std_devs DataFrame
            std_devs[func_col] = differences

    if not std_devs.empty:
        min_std_func = std_devs.idxmin(axis=1) # Select the column with the minimum standard deviation for each row. 
        Test_data['DeltaY(test func)'] = std_devs.min(axis=1)
        Test_data['No. of ideal func'] = min_std_func # Include the name of the chosen function
    else:
        Test_data['DeltaY(test func)'] = np.nan
        Test_data['No. of ideal func'] = "No valid function" 

    print(Test_data.head())
    Test_data.to_csv('updated.csv', index=False)

match_test_with_ideal()
