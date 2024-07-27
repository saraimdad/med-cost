from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from pipeline.predict_pipeline import CustomData, PredictPipeline


application = Flask(__name__)

app = application

## Route for home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_data():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data = CustomData(
            age = request.form.get('age'), 
            sex = request.form.get('sex'),
            bmi = float(request.form.get('bmi')),
            children = request.form.get('children'),
            smoker = request.form.get('smoker'),
            region = request.form.get('region')
        )

        data_df = data.get_data_as_dataframe()
        print(data_df)

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(data_df)

        return render_template('home.html', results=result[0])

if __name__=='__main__':
    app.run(host='0.0.0.0')