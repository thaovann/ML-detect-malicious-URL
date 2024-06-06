from sklearn.metrics import classification_report, accuracy_score
from data_preprocessing import X_train, X_test, y_train, y_test, X
from random_forest_model import y_pred_rf, rf
from xgboost_model import y_pred_x
from lgbm_model import y_pred_lgb
import matplotlib.pyplot as plt
import numpy as np

print("Random Forest:")
print(classification_report(y_test, y_pred_rf, target_names=['benign', 'defacement', 'phishing', 'malware']))
print("Accuracy:", accuracy_score(y_test, y_pred_rf))


print("XGBoost:")
print(classification_report(y_test, y_pred_x, target_names=['benign', 'defacement', 'phishing', 'malware']))
print("Accuracy:", accuracy_score(y_test, y_pred_x))

print("Light GBM:")
print(classification_report(y_test, y_pred_lgb, target_names=['benign', 'defacement', 'phishing', 'malware']))
print("Accuracy:", accuracy_score(y_test, y_pred_lgb))
