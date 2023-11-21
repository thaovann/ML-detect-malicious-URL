from sklearn.metrics import classification_report, accuracy_score
from Main.data_preprocessing import X_train, X_test, y_train, y_test, X
from random_forest_model import y_pred_rf, rf
from xgboost_model import y_pred_x
from lgbm_model import y_pred_lgb
import matplotlib.pyplot as plt
import numpy as np
# Evaluate the models
print("Random Forest:")
print(classification_report(y_test, y_pred_rf, target_names=['benign', 'defacement', 'phishing', 'malware']))
print("Accuracy:", accuracy_score(y_test, y_pred_rf))

# Similar code for XGBoost and Light GBM
print("XGBoost:")
print(classification_report(y_test, y_pred_x, target_names=['benign', 'defacement', 'phishing', 'malware']))
print("Accuracy:", accuracy_score(y_test, y_pred_x))

print("Light GBM:")
print(classification_report(y_test, y_pred_lgb, target_names=['benign', 'defacement', 'phishing', 'malware']))
print("Accuracy:", accuracy_score(y_test, y_pred_lgb))
# Feature importance plots (you can copy the feature importance plot code here)
# plt.figure(figsize=(10, 6))
# feature_importance_rf = rf.feature_importances_
# sorted_idx = np.argsort(feature_importance_rf)[::-1]
# feature_names = X.columns
# pos = np.arange(sorted_idx.shape[0]) + .5
# plt.barh(pos, feature_importance_rf[sorted_idx], align='center')
# plt.yticks(pos, feature_names[sorted_idx])
# plt.xlabel('Feature Importance')
# plt.title('Random Forest Feature Importance')
# plt.show()