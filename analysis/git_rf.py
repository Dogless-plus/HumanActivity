# coding=utf-8

import pandas as pd
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.ensemble import RandomForestClassifier
from pickle import dump

df = pd.read_csv("df_active.csv",encoding="utf-8",header=0)
print(df.shape)
n_folds = 5
folds =list(KFold(df.shape[0],n_folds=n_folds,shuffle=True))

model_map = {"rf": (RandomForestClassifier, {"n_estimators": 100,"n_jobs":4}), }
def calc_error(baseday, history_window, folds, model_type="rf", verbose=1):
    errors, n_folds = [], len(folds)
    for i, (idx_train, idx_test) in enumerate(folds):
        X = df[df.columns[-(baseday + history_window):-baseday]].as_matrix()
        y = np.array(df[df.columns[-baseday]])
        model = model_map[model_type][0](**model_map[model_type][1])
        model.fit(X[idx_train], y[idx_train])
        y_pred = model.predict(X[idx_test])
        error_rate = sum(map(lambda x: 0 if x[0] == x[1] else 1, zip(y_pred, y[idx_test]))) / len(idx_test)
        if verbose == 1: print(r"%s/%s" % (i + 1, n_folds), "error:", error_rate)
        errors.append(error_rate)
    mean_error = np.mean(errors)
    if verbose > 0: print("baseday:", baseday, "windows:", history_window,"error", mean_error,"\n", errors[:8])
    return mean_error,errors

def get_day(baseday,max_window=3,min_window=1,window_list = None):
    if not window_list: window_list = range(min_window,max_window+1)
    return tuple(zip(*[calc_error(baseday,window, folds,verbose= 2) for window in window_list]))

max_window,min_window = 300,1
d_632 = get_day(1,max_window=max_window,min_window=min_window)
with open("d_632_rf.pkl","wb") as f:
    dump(d_632,f)
d_631 = get_day(2,max_window=max_window,min_window=min_window)
with open("d_631_rf.pkl","wb") as f:
    dump(d_631,f)
d_630 = get_day(3,max_window=max_window,min_window=min_window)
with open("d_630_rf.pkl","wb") as f:
    dump(d_630,f)
d_629 = get_day(4,max_window=max_window,min_window=min_window)
with open("d_629_rf.pkl","wb") as f:
    dump(d_629,f)
d_628 = get_day(5,max_window=max_window,min_window=min_window)
with open("d_628_rf.pkl","wb") as f:
    dump(d_628,f)
d_627 = get_day(6,max_window=max_window,min_window=min_window)
with open("d_627_rf.pkl","wb") as f:
    dump(d_627,f)
d_626 = get_day(7,max_window=max_window,min_window=min_window)
with open("d_626_rf.pkl","wb") as f:
    dump(d_626,f)

print("project_done!")