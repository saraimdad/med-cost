import os
import sys
import dill
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mysql.connector
import pandas as pd
import numpy as np
import numpy
from sqlalchemy import create_engine
from exception import CustomException
from sklearn.model_selection import GridSearchCV

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
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]

            gs = GridSearchCV(model, para ,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    

def load_obj(file_path):
    try:
        with open(file_path, 'rb') as f:
            return dill.load(f)

    except Exception as e:
        raise CustomException(e, sys)