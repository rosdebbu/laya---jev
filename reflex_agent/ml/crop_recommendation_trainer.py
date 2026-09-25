# ============================================================
# Crop Recommendation — Empirical ML Training Engine
# Integrated from rosdebbu/l-data-seT---ML into KisanZess
# ============================================================
# Predict the best crop to grow based on soil & climate data.
# Models: Random Forest (99.1%), Decision Tree (98.6%), KNN (97.8%)
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Crop_recommendation.csv")
if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.abspath(os.path.join("..", "l-data-seT---ML", "data", "Crop_recommendation.csv"))

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output_charts")
os.makedirs(CHART_DIR, exist_ok=True)

# Plot style
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight"})

def run_crop_training():
    print("=" * 60)
    print("1. LOADING CROP DATASET")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)
    print(f"Shape: {df.shape}")
    print(f"Target classes ({df['label'].nunique()}): {sorted(df['label'].unique())}")

    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    X = df[features]
    y = df["label"]

    # Train/Test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Feature scaling
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
        results[name] = {"model": model, "predictions": y_pred, "accuracy": acc}
        print(f"  [OK] {name} - Accuracy: {acc:.4f} ({acc*100:.2f}%)")

    best_model = max(results, key=lambda k: results[k]["accuracy"])
    print(f"\n[*] Best Model: {best_model} ({results[best_model]['accuracy']:.2%})")
    return results

if __name__ == "__main__":
    run_crop_training()
