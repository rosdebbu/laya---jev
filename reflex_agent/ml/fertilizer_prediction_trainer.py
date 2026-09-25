# ============================================================
# Fertilizer Prediction — ML Training & Evaluation Engine
# ============================================================
# Predicts optimal fertilizer formulation based on soil, crop & climate.
# Models: Random Forest, Decision Tree, KNN
# ============================================================

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def train_fertilizer_pipeline(data_path: str = None):
    if data_path is None:
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../l-data-seT---ML/data/Fertilizer_Prediction.csv"))
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Fertilizer dataset not found at {data_path}")

    df = pd.read_csv(data_path)
    target_col = "Fertilizer Name"

    # Label-encode categorical columns
    le_soil = LabelEncoder()
    le_crop = LabelEncoder()

    df["Soil_Type_encoded"] = le_soil.fit_transform(df["Soil Type"])
    df["Crop_Type_encoded"] = le_crop.fit_transform(df["Crop Type"])

    feature_cols = [
        "Temperature", "Humidity", "Moisture",
        "Soil_Type_encoded", "Crop_Type_encoded",
        "Nitrogen", "Phosphorous", "Potassium"
    ]
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        acc = accuracy_score(y_test, y_pred)
        results[name] = {"model": model, "accuracy": float(acc)}

    return {
        "models": {n: r["model"] for n, r in results.items()},
        "accuracies": {n: r["accuracy"] for n, r in results.items()},
        "scaler": scaler,
        "le_soil": le_soil,
        "le_crop": le_crop,
        "feature_cols": feature_cols,
        "classes": sorted(y.unique().tolist()),
    }


if __name__ == "__main__":
    res = train_fertilizer_pipeline()
    print("Fertilizer Models Trained Successfully:")
    for k, v in res["accuracies"].items():
        print(f"  {k}: {v*100:.2f}%")
