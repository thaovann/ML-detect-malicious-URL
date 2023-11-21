from lightgbm import LGBMClassifier
from Main.data_preprocessing import X_train, X_test, y_train
# Create and train the Light GBM model
lgb = LGBMClassifier(objective='multiclass', boosting_type='gbdt', n_jobs=5, silent=True, random_state=5)
LGB_C = lgb.fit(X_train, y_train)

# Make predictions
y_pred_lgb = LGB_C.predict(X_test)
