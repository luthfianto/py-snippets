def get_scikit_summary(X,y,predictions, params):
  from scipy import stats
  newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
  MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

  var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
  sd_b = np.sqrt(var_b)
  ts_b = params/ sd_b

  p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX[0])))) for i in ts_b]

  sd_b = np.round(sd_b,3)
  ts_b = np.round(ts_b,3)
  p_values = np.round(p_values,3)
  params = np.round(params,4)

  myDF3 = pd.DataFrame()
  myDF3["Coefficients"],myDF3["Standard Errors"],myDF3["t values"],myDF3["Probabilities"] = [params,sd_b,ts_b,p_values]
  print(myDF3)

get_scikit_summary(X_train,y_train,train_proba, lrtrain.coef_)
