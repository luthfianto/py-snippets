from datetime import timedelta
from matplotlib import pyplot as plt, rc_context, rc
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot, plot_plotly, plot_components_plotly
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px


def acf_res(forecast: pd.DataFrame, train: pd.DataFrame):
    """
    Plots a autocorrelation plot of the residuals (y-true minus y-predicted) for training data.
    """
    date_range = train['ds']
    res = train.set_index('ds')['y'] - forecast.set_index('ds').loc[date_range, 'yhat']
    plot_acf(res)

def plot_residuals(df_ori: pd.DataFrame, df_backtest: pd.DataFrame):
    dfmantap = pd.merge(df_ori, df_backtest, on='ds')[['ds','y','yhat']]
    dfmantap['residuals'] = dfmantap['y'] - dfmantap['yhat']
    fig, axes = plt.subplots(1,3, figsize=(20,4), dpi=100)

    # dfmantap['abs_residuals'] = dfmantap['residuals'].abs()
    # dfmantap['sign'] = (dfmantap['residuals'] / dfmantap['abs_residuals']).astype(int)
    # dfmantap['month'] = dfmantap.ds.dt.month
    dfmantap.plot(x='ds',y='residuals',ax=axes[0])
    dfmantap['residuals'].hist(ax=axes[1])
    dfmantap['residuals'].plot(kind='kde',ax=axes[2])
    
    return dfmantap
