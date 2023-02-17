import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class CustomLinearRegression:
    def __init__(self, *, fit_intercept=True):

        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = None

    def fit(self, x, y):
        X = np.array(x)
        ones = np.array(np.ones(len(X)))
        if self.fit_intercept:
            X = np.column_stack((ones, X))
        y = np.matrix(y)
        self.coefficient = np.array(np.linalg.inv(X.T @ X) @ X.T @ y)
        if self.fit_intercept:
            self.intercept = float(self.coefficient[0])

    def predict(self, x):
        x_pred = np.array(x)
        ones = np.array(np.ones(len(x_pred)))
        if self.fit_intercept:
            x_pred = np.column_stack((ones, x_pred))
        return x_pred @ self.coefficient

    @staticmethod
    def calculate_r2_score(y, y_hat):
        y_bar = float(y.mean())
        ssreg = np.sum((y_hat - y_bar)**2)
        sstot = np.sum((y - y_bar) ** 2)
        return float(ssreg / sstot)

    @staticmethod
    def calculate_rmse(y, y_hat):
        return float(np.sqrt(((y - y_hat)**2).sum() / len(y)))


data = pd.read_csv('./data.csv')

Cust_reg = CustomLinearRegression(fit_intercept=True)
Cust_reg.fit(data[['f1', 'f2', 'f3']], data[['y']])
y_pred = Cust_reg.predict(data[['f1', 'f2', 'f3']])
my_r2 = Cust_reg.calculate_r2_score(data[['y']], y_pred)
my_rmse = Cust_reg.calculate_rmse(data[['y']], y_pred)

sci_reg = LinearRegression(fit_intercept=True)
sci_reg.fit(data[['f1', 'f2', 'f3']], data[['y']])
sci_pred = sci_reg.predict(data[['f1', 'f2', 'f3']])
r2_score = r2_score(data[['y']], sci_pred)
rmse = np.sqrt(mean_squared_error(data[['y']], sci_pred))

print({'Intercept': np.subtract(Cust_reg.intercept, sci_reg.intercept_),
       'Coefficient': np.subtract(Cust_reg.coefficient[1:].T, sci_reg.coef_),
       'R2': r2_score - my_r2, 'RMSE': rmse - my_rmse})
