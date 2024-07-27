import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from exception import CustomException
from logger import logging
from utils import save_obj


@dataclass
class DataTransformationConfig:
    preprocessor_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transfromation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        try:
            numerical_columns = ['age', 'bmi', 'children']
            categorical_columns = ['sex', 'smoker', 'region']

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )


            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )

            logging.info('Numerical columns transformed.')
            logging.info('Categorical columns transfromed.')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Train and test data obtained.')

            preprocessing_obj = self.get_data_transformer_obj()

            target_column = 'charges'
            numerical_columns = ['age', 'bmi', 'children']
            categorical_columns = ['sex', 'smoker', 'region']

            target_feature_train_df = train_df[target_column]
            input_feature_train_df = train_df.drop(columns=[target_column], axis=1)

            target_feature_test_df = test_df[target_column]
            input_feature_test_df = test_df.drop(columns=[target_column], axis=1)

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info('Saved preprocessing object.')

            save_obj(
                file_path = self.data_transfromation_config.preprocessor_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transfromation_config.preprocessor_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        
