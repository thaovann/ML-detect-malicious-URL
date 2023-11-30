from sklearn.ensemble import RandomForestClassifier
from data_preprocessing import X_train, X_test, y_train, y_test

# Create and train the Random Forest model
rf = RandomForestClassifier(n_estimators=100, max_features="sqrt")
rf.fit(X_train, y_train)



# Make predictions
y_pred_rf = rf.predict(X_test)
