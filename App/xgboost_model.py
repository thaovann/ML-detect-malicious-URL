import xgboost as xgb
from data_preprocessing import X_train, X_test, y_train

xgb_c = xgb.XGBClassifier(n_estimators=100)
xgb_c.fit(X_train, y_train)

y_pred_x = xgb_c.predict(X_test)
