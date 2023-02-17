import os
import requests

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

# checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# download data if it is unavailable
if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

# read data
data = pd.read_csv('../Data/data.csv')
X = data.select_dtypes('number').drop(columns=['salary', 'experience', 'age'])
y = data['salary']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
model = LinearRegression()
model.fit(x_train, y_train)
predictions = model.predict(x_test)


def adjust_negative_predictions(technique: str) -> list:
    if technique == 'zeroes':
        no_negatives = [0 if i < 0 else i for i in predictions]
    elif technique == 'median':
        no_negatives = [np.median(y_train) if i < 0 else i for i in predictions]
    return no_negatives


print(round(mape(y_test, adjust_negative_predictions('zeroes')), 5))
