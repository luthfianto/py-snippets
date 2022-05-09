from datetime import timedelta

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import prophet.plot

from matplotlib import pyplot as plt
from matplotlib import rc, rc_context
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import add_changepoints_to_plot, plot_components_plotly, plot_cross_validation_metric, plot_plotly, plot_seasonality
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews



def acf_res(forecast: pd.DataFrame, train: pd.DataFrame):
    """
    Plots a autocorrelation plot of the residuals (y-true minus y-predicted) for training data.
    """
    date_range = train['ds']
    res = train.set_index('ds')['y'] - forecast.set_index('ds').loc[date_range, 'yhat']
    plot_acf(res)

def plot_residuals(df_ori: pd.DataFrame, df_backtest: pd.DataFrame, ylim=None):
    dfmantap = pd.merge(df_ori, df_backtest, on='ds')[['ds','y','yhat']]
    dfmantap['residuals'] =  dfmantap['yhat'] - dfmantap['y']
    fig, axes = plt.subplots(1,3, figsize=(20,4), dpi=100)

    # dfmantap['abs_residuals'] = dfmantap['residuals'].abs()
    # dfmantap['sign'] = (dfmantap['residuals'] / dfmantap['abs_residuals']).astype(int)
    # dfmantap['month'] = dfmantap.ds.dt.month
    dfmantap.plot(x='ds',y='residuals',ax=axes[0], ylim=ylim)
    dfmantap['residuals'].hist(ax=axes[1])
    dfmantap['residuals'].plot(kind='kde',ax=axes[2])
    
    return dfmantap
