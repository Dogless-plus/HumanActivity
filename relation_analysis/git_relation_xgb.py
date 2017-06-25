# coding=utf-8

import pandas as pd
import numpy as np
from sklearn.cross_validation import KFold
from pickle import dump
from xgboost import XGBClassifier

df = pd.read_csv("df_active.csv", encoding="utf-8", header=0)
print(df.shape)
n_folds = 5
folds = list(KFold(df.shape[0], n_folds=n_folds, shuffle=True))

baseday = 1
history_window = 60
right_map = {}
count = 0
for baseday in range(1, 8):
    for i, (idx_train, idx_test) in enumerate(folds):
        count +=1
        print(count)
        X = df[df.columns[-(baseday + history_window):-baseday]].as_matrix()
        y = np.array(df[df.columns[-baseday]])
        model = XGBClassifier(n_estimators=100)
        model.fit(X[idx_train], y[idx_train])
        y_pred = model.predict(X[idx_test])
        right_tmp = list(zip(idx_test, [1 if item[0] == item[1] else 0 for item in zip(y_pred, y[idx_test])]))
        for ri, vi in right_tmp:
            if ri in right_map:
                right_map[ri].append(vi)
            else:
                right_map[ri] = [vi, ]
        print(right_map.__str__()[:100])
with open("xgb_relation_error.pkl", "wb") as f:
    dump(right_map, f)
print("project done!")
