from lightgbm import LGBMClassifier
from data_preprocessing import X_train, X_test, y_train

lgb = LGBMClassifier(objective='multiclass', boosting_type='gbdt', n_jobs=5, silent=True, random_state=5)
LGB_C = lgb.fit(X_train, y_train)

y_pred_lgb = LGB_C.predict(X_test)
