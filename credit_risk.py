# !pip install optbinning
# !pip install scorecardpy
# !pip install seaborn


from datetime import datetime
from matplotlib import pyplot
from optbinning import OptimalBinning, ContinuousOptimalBinning, Scorecard, BinningProcess
from optbinning.scorecard.plots import plot_ks, plot_auc_roc
from pylab import rcParams
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix,plot_confusion_matrix, precision_recall_fscore_support, ConfusionMatrixDisplay

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scorecardpy as sc
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf


def df_summarier(df) -> pd.DataFrame:
    a = df.isna().any(axis=0)
    notnan= df.count()
    b = df.dtypes
    c = df.nunique()
    d = pd.Series({col: df[col].unique() for col in df})
    print("df.shape", df.shape)
    # print("df.created_time.min()", df.created_time.min(), "df.created_time.max()", df.created_time.max(), )
    print("df summary")
    return pd.concat([a, notnan,b, c,d,df.describe().T], axis=1).rename(
        columns={0: "has nan?",1: "num of notnan", 2: "dtypes", 3: "num of unique values", 4: "list of unique values"}
    )


def create_binning_config(df_: pd.DataFrame, force_monotonic: bool =False) -> dict:
    bfp={}
    for col in df_.columns:
        if col=='TARGET':
            continue
        dtype="numerical"
        solver="cp"
        if df_[col].dtype==object:
            dtype="categorical"
            # solver="mip"
        name=col
        
        if force_monotonic:
            bfp[name]= {"dtype": dtype, "solver": solver, "monotonic_trend":'auto_asc_desc'}
        else:
            bfp[name]= {"dtype": dtype, "solver": solver}

            

    return bfp


def predictiveness(i: float) -> str:
    if i <0.02: return 'Not useful for prediction'
    if 0.02 < i <= 0.1: return 'Weak predictive Power'
    if 0.1  < i <= 0.3: return 'Medium predictive Power'
    if 0.3  < i <= 0.5: return 'Strong predictive Power'
    if i >0.5: return 'Suspicious Predictive Power'


def create_binning(df_: pd.DataFrame, binning_fit_params: dict, special_codes=[999999,365243], plot=True) -> BinningProcess:
    # 1) Define list of features and categorical ones
    list_features = df_.drop(columns=['TARGET']).columns.values
    list_categorical = df_.select_dtypes(include=['object', 'category']).columns.values
    # 2) Instantiate BinningProcess
    binning_process = BinningProcess(
        categorical_variables=list_categorical,
        variable_names=list_features, binning_fit_params=binning_fit_params,
        special_codes=special_codes
    )

    # 3) Fit and transform dataset
    binning_process.fit(df_.drop(columns=['TARGET']), df_.TARGET)


    for col in binning_process.variable_names:
        optb=binning_process.get_binned_variable(col)
        optb.binning_table.build()
        if plot:
            print(col)
            optb.binning_table.plot(metric="woe")
            display(optb.binning_table.build())
            display(optb.binning_table.build().Bin.values.tolist())

            print('==')


    return binning_process


def get_iv(binning_process: BinningProcess) -> pd.DataFrame:
    ll=[]

    for col in binning_process.variable_names:
        optb=binning_process.get_binned_variable(col)
        # optb.binning_table.plot(metric="woe")
        iv=optb.binning_table.build().IV.Totals
        ll.append({"column": col, "IV":iv})

    dfiv=pd.DataFrame(ll).sort_values('IV', ascending=False)
    dfiv['predictiveness']=dfiv.IV.apply(predictiveness)
    return dfiv

def get_class_weight(df_):
    cw0full=df_.groupby('TARGET').count().T.iloc[0]
    class_weightfull=(1-(cw0full/df.shape[0])).to_dict()
    return class_weightfull
