import os
import sys
import dill
import mysql.connector
import pandas as pd
import numpy
from sqlalchemy import create_engine
from exception import CustomException

def get_data():
    db_config = {
    'user': 'root',
    'password': 'qwerty123',
    'host': 'localhost',
    'database': 'med_cost'
}

    conn = mysql.connector.connect(**db_config)

    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(connection_string)

    query = "SELECT * FROM insurance"

    df = pd.read_sql(query, engine)
    return df

def save_obj(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as f:
            dill.dump(obj, f)

    except Exception as e:
        raise CustomException(e, sys)
    