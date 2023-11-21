import xgboost as xgb
from Main.data_preprocessing import X_train, X_test, y_train
# Create and train the XGBoost model
xgb_c = xgb.XGBClassifier(n_estimators=100)
xgb_c.fit(X_train, y_train)

# Make predictions
y_pred_x = xgb_c.predict(X_test)
