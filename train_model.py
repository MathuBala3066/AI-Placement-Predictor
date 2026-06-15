import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("placementdata.csv")

# Encode categorical columns
df["ExtracurricularActivities"] = df["ExtracurricularActivities"].str.strip().map({
    "Yes": 1,
    "No": 0
})

df["PlacementTraining"] = df["PlacementTraining"].str.strip().map({
    "Yes": 1,
    "No": 0
})

df["PlacementStatus"] = df["PlacementStatus"].str.strip().map({
    "Placed": 1,
    "NotPlaced": 0
})

# Drop StudentID (not useful for prediction)
df = df.drop(columns=["StudentID"])

# Features and target
X = df.drop(columns=["PlacementStatus"])
y = df["PlacementStatus"].astype(int)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model and feature column order
joblib.dump(model, "placement_model.pkl")
joblib.dump(list(X.columns), "model_columns.pkl")

print("Model saved as placement_model.pkl")