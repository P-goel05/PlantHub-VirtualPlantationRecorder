import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
data = pd.read_csv("tree_growth_data.csv")

# Encode tree type
encoder = LabelEncoder()
data["tree_type_encoded"] = encoder.fit_transform(data["tree_type"])

X = data[["tree_type_encoded", "avg_temp", "water_freq"]]
y = data["height_6_months"]

# Train model
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X, y)

# model = LinearRegression()
# model.fit(X, y)

model = DecisionTreeRegressor(random_state=42)
model.fit(X, y)

# Save model and encoder
with open("tree_growth_model.pkl", "wb") as f:
    pickle.dump((model, encoder), f)

# print("✅ Model trained and saved")
# print("✅ Linear Regression model saved")
print("✅ Decision Tree model saved")