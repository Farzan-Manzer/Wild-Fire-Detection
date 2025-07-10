# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# import joblib

# # Load data
# data = pd.read_csv("data/dataset.csv")

# X = data[['temp', 'humidity', 'wind_speed', 'vegetation', 'recent_fires']]
# y = data['fire_detected']

# # Train model
# model = RandomForestClassifier()
# model.fit(X, y)

# # Save model
# joblib.dump(model, 'app/ml/model.pkl')
# print("✅ Model trained and saved to app/ml/model.pkl")


# import xgboost as xgb
# import pandas as pd
# import joblib

# # Load your dataset
# df = pd.read_csv("dataset.csv")

# # Define features and target
# X = df[["temperature", "humidity", "wind_speed", "vegetation", "recent_fires"]]
# y = df["fire_detected"]

# # Train new model
# model = xgb.XGBClassifier()
# model.fit(X, y)

# # Save the new model
# joblib.dump(model, "model.pkl")


# app/ml/train.py

# import pandas as pd
# import xgboost as xgb
# import joblib
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score

# # 1. Load dataset
# df = pd.read_csv("dataset.csv")

# # 2. Features and target
# feature_cols = ["temperature", "humidity", "wind_speed", "vegetation", "recent_fires"]
# target_col = "fire_detected"

# X = df[feature_cols]
# y = df[target_col]

# # 3. Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 4. Initialize and train XGBoost
# model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
# model.fit(X_train, y_train)

# # 5. Evaluate
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"✅ Model trained with accuracy: {accuracy:.2f}")

# # 6. Save model
# joblib.dump(model, "app/ml/model.pkl")
# print("📦 Model saved to app/ml/model.pkl")



# app/ml/train.py

import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load dataset
df = pd.read_csv("data/dataset.csv")

# 2. Define features and label
X = df[["temperature", "humidity", "wind_speed", "vegetation", "recent_fires"]]
y = df["fire_detected"]

# 3. Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Model trained — Accuracy: {acc:.2%}")

# 6. Save model
joblib.dump(model, "app/ml/model.pkl")
print("📦 Model saved as app/ml/model.pkl")