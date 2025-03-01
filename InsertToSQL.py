import pandas as  #Loading the necessary libraries
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table

def CSV_insert_to_SQL():

    
    """Load csv files to SQLALchemy using Pandas."""

    # Create a database SQLite using create_engine function
    engine = db.create_engine('sqlite:///python_database.db', echo=True)
    
    #Load CSV data and write to SQL using Pandas

    #Loading a 'Train_data' file into SQL
    df_train = pd.read_csv('') #Insert your file path
    df_train.columns = ['X', 'Y1(training func)', 'Y2(training func)', 'Y3(training func)', 'Y4(training func)'] 
    df_train.to_sql(con=engine, name='Train_data', if_exists='replace', index=False) 

     #Loading an 'Ideal_data' file into SQL
    df_ideal = pd.read_csv('') #Insert your file path
    df_ideal.columns = ['X'] + [f'Y{i}(ideal func)' for i in range(1, 51)] 
    df_ideal.to_sql(con=engine, name='Ideal_data', if_exists='replace', index=False) 

    #Loading a 'Test_data' file into SQL
    df_test = pd.read_csv('/Users/marththe/Desktop/Python/test.csv') 
    df_test.columns = ['X(test func)', 'Y(test func)'] 
    df_test.to_sql(con=engine, name='Test_data', if_exists='replace', index=False) 
    
    #Connect to the engine 
    conn = engine.connect() 
    metadata = db.MetaData()
    
    #Reflecting tables
    train_data = Table('Train_data', metadata, autoload_with=engine)
    ideal_data = Table('Ideal_data', metadata, autoload_with=engine)
    test_data = Table('Test_data', metadata, autoload_with=engine)
    
    #Example query on Test_data
    query = test_data.select()
    result = conn.execute(query).fetchmany(5)
    for r in result:
        print(r)

CSV_insert_to_SQL()