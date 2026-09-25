# 📘 Master Guide: Tutorial 4 (T4) & Tutorial 5 (T5) in Python

> **Simple, Complete & Proper Reference for Lab Notebooks, Obsidian Notes & Viva**  
> Covers library imports, step-by-step implementation, formulas, and interpretations.

---

## 📊 Quick Overview: T4 vs T5 at a Glance

| Aspect | Tutorial 4 (T4) | Tutorial 5 (T5) |
| :--- | :--- | :--- |
| **Topic** | **Performance Metrics for Classification** | **Multiple Linear Regression** |
| **Problem Type** | Classification (Predicting categories) | Regression (Predicting continuous numbers) |
| **Target Variable ($y$)** | Discrete Label: Crop (`rice`, `maize`, `lentil`) | Continuous Value: `rainfall` (e.g., 202.5 mm) |
| **Input Features ($X$)** | Soil & climate features (N, P, K, temp, etc.) | Multiple features: N, P, K, temp, humidity, pH |
| **Model Algorithm** | `RandomForestClassifier` (or DecisionTree, KNN) | `LinearRegression` (Ordinary Least Squares) |
| **Core Metrics** | **Accuracy, Precision, Recall, F1-Score, Confusion Matrix** | **MAE, MSE, RMSE, $R^2$ Score** |
| **Output Plots** | Confusion Matrix Heatmap, Metrics Bar Chart | Actual vs Predicted Scatter Plot, Feature Coefficients |

---

# 📊 PART 1: TUTORIAL 4 (T4) — CLASSIFICATION PERFORMANCE METRICS

---

### 1. How to Import the Libraries (Explained Line-by-Line)

Here is the exact code block to import everything you need for T4:

```python
# 1. General data handling and math
import numpy as np          # Fast numerical arrays & math operations
import pandas as pd         # DataFrames to load, inspect, and filter CSV data

# 2. Visualization & plotting
import matplotlib.pyplot as plt   # Standard plotting library (figures, bars)
import seaborn as sns             # Beautiful statistical plots (confusion matrix heatmap)

# 3. Data preprocessing
from sklearn.model_selection import train_test_split  # Splits data into 80% Train, 20% Test
from sklearn.preprocessing import StandardScaler      # Rescales features to Mean=0, Std=1

# 4. Classification Machine Learning Model
from sklearn.ensemble import RandomForestClassifier   # Ensemble of Decision Trees

# 5. Performance Metrics for Evaluation
from sklearn.metrics import (
    accuracy_score,        # Fraction of all correct predictions: (TP + TN) / Total
    precision_score,       # Quality of positive guesses: TP / (TP + FP)
    recall_score,          # Coverage of actual positives: TP / (TP + FN)
    f1_score,              # Harmonic mean of Precision & Recall
    classification_report, # Formatted table showing Precision, Recall, F1 per class
    confusion_matrix       # 2D table of Actual vs. Predicted counts
)
```

#### Why do we need each library?
* **`pandas` & `numpy`**: Read the CSV file into a table (`df`) and handle feature matrices.
* **`StandardScaler`**: Puts variables like Nitrogen (0–140) and pH (3–9) on the same mathematical scale.
* **`RandomForestClassifier`**: The classifier that learns the rules from the training data.
* **`sklearn.metrics`**: Measures how well our model performs so we don't rely only on simple accuracy.

---

### 2. Step-by-Step Implementation (How to Do T4)

```python
# ==========================================================
# TUTORIAL 4: COMPLETE STEP-BY-STEP IMPLEMENTATION
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

# ----------------------------------------------------------
# STEP 1: Load Dataset & Define Features (X) and Target (y)
# ----------------------------------------------------------
df = pd.read_csv("data/Crop_recommendation.csv")

# Separate independent features (X) and dependent class label (y)
feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X = df[feature_cols]
y = df['label']  # Categories: rice, maize, chickpea, etc.

print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")

# ----------------------------------------------------------
# STEP 2: Train-Test Split (80% Train, 20% Test)
# ----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# ----------------------------------------------------------
# STEP 3: Feature Scaling (StandardScaler)
# ----------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------------------------------------------------
# STEP 4: Train Classifier (Random Forest)
# ----------------------------------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# ----------------------------------------------------------
# STEP 5: Make Predictions on Unseen Test Data
# ----------------------------------------------------------
y_pred = model.predict(X_test_scaled)

# ----------------------------------------------------------
# STEP 6: Compute the 4 Performance Metrics
# ----------------------------------------------------------
acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0)

print("\n" + "=" * 45)
print("       T4 CLASSIFICATION METRICS")
print("=" * 45)
print(f"  Accuracy:  {acc:.4f}  ({acc * 100:.2f}%)")
print(f"  Precision: {prec:.4f}")
print(f"  Recall:    {rec:.4f}")
print(f"  F1-Score:  {f1:.4f}")
print("=" * 45)

# ----------------------------------------------------------
# STEP 7: Classification Report (Per-Class Breakdown)
# ----------------------------------------------------------
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# ----------------------------------------------------------
# STEP 8: Confusion Matrix Heatmap
# ----------------------------------------------------------
labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels)
plt.title('T4: Confusion Matrix (Random Forest)', fontsize=14, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('Actual Label', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

---

### 3. Core Concepts Explained Simply

#### 1. Accuracy
$$\text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Predictions}}$$
* **What it means**: Percentage of total test samples correctly predicted.
* **Limitation**: If 90% of crops are rice and 10% are maize, a dummy model that always guesses "rice" gets 90% accuracy, but it completely fails on maize!

#### 2. Precision
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
* **Question it answers**: *"Out of all samples the model called Rice, how many are actually Rice?"*
* **Focus**: Minimizing **False Positives (False Alarms)**.

#### 3. Recall (Sensitivity)
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
* **Question it answers**: *"Out of all actual Rice samples in the field, how many did the model find?"*
* **Focus**: Minimizing **False Negatives (Missed Cases)**.

#### 4. F1-Score
$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
* **What it means**: The **harmonic mean** of Precision and Recall.
* **Why harmonic mean?** If Precision = $1.0$ and Recall = $0.0$, simple average = $0.5$ (misleading!), but F1 = $0.0$ (correctly flags failure).

#### 5. Confusion Matrix
* **Diagonal cells**: Correct predictions (True Positives). The darker the diagonal, the better.
* **Off-diagonal cells**: Errors / confusion between classes (e.g., maize mistaken for rice).

---
---

# 📈 PART 2: TUTORIAL 5 (T5) — MULTIPLE LINEAR REGRESSION

---

### 1. How to Import the Libraries (Explained Line-by-Line)

Here is the exact code block to import everything you need for T5:

```python
# 1. General data handling and math
import numpy as np          # Array operations & square root (np.sqrt for RMSE)
import pandas as pd         # Data loading and feature slicing

# 2. Visualization & plotting
import matplotlib.pyplot as plt   # Scatter plots and bar charts
import seaborn as sns             # Styled background themes

# 3. Data preprocessing
from sklearn.model_selection import train_test_split  # 80/20 train-test splitting
from sklearn.preprocessing import StandardScaler      # Feature normalization

# 4. Multiple Linear Regression Model
from sklearn.linear_model import LinearRegression     # Fits OLS hyperplane: y = b0 + b1*X1 + ...

# 5. Regression Performance Metrics
from sklearn.metrics import (
    mean_absolute_error,   # MAE: Average absolute distance in real units
    mean_squared_error,    # MSE: Average squared error (punishes outliers)
    r2_score               # R-Squared: Proportion of variance explained (0.0 to 1.0)
)
```

#### Why do we need each library?
* **`LinearRegression`**: Finds the best-fitting straight line / hyperplane by minimizing the sum of squared residuals (**Ordinary Least Squares**).
* **`mean_absolute_error`**: Gives the physical error in the original units (e.g., $\pm 12$ mm of rainfall).
* **`mean_squared_error`**: Used to compute **RMSE** via `np.sqrt(mse)`.
* **`r2_score`**: The standard goodness-of-fit score for regression models.

---

### 2. Step-by-Step Implementation (How to Do T5)

```python
# ==========================================================
# TUTORIAL 5: COMPLETE STEP-BY-STEP IMPLEMENTATION
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ----------------------------------------------------------
# STEP 1: Load Dataset & Define Multiple Features (X) and Target (y)
# ----------------------------------------------------------
df = pd.read_csv("data/Crop_recommendation.csv")

# MULTIPLE input features (X)
feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph']
X = df[feature_cols]

# CONTINUOUS target variable (y)
target_col = 'rainfall'
y = df[target_col]

print(f"Features (X): {feature_cols}")
print(f"Target (y):   {target_col}")
print(f"Shape: {X.shape[0]} samples with {X.shape[1]} features")

# ----------------------------------------------------------
# STEP 2: Train-Test Split (80% Train, 20% Test)
# ----------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# ----------------------------------------------------------
# STEP 3: Feature Scaling (StandardScaler)
# ----------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------------------------------------------------
# STEP 4: Fit Multiple Linear Regression Model
# ----------------------------------------------------------
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Inspect the mathematical equation learned by model:
print("\n" + "=" * 45)
print("     LINEAR REGRESSION MODEL WEIGHTS")
print("=" * 45)
print(f"Intercept (b0): {model.intercept_:.4f}")
print("Feature Coefficients:")
for feat, coef in zip(feature_cols, model.coef_):
    print(f"  {feat:>12}: {coef:>8.4f}")
print("=" * 45)

# ----------------------------------------------------------
# STEP 5: Predict on Test Set & Calculate Regression Metrics
# ----------------------------------------------------------
y_pred = model.predict(X_test_scaled)

mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print("\n" + "=" * 45)
print("       T5 REGRESSION PERFORMANCE METRICS")
print("=" * 45)
print(f"  MAE  (Mean Absolute Error):     {mae:.4f}")
print(f"  MSE  (Mean Squared Error):      {mse:.4f}")
print(f"  RMSE (Root Mean Squared Error): {rmse:.4f}")
print(f"  R2   (R-Squared Score):         {r2:.4f}")
print("=" * 45)

# ----------------------------------------------------------
# STEP 6: Plot 1 — Actual vs. Predicted Scatter Plot
# ----------------------------------------------------------
plt.figure(figsize=(7, 6))
plt.scatter(y_test, y_pred, color='#1f77b4', alpha=0.6, edgecolors='k', label='Predictions')

# Draw ideal 45-degree reference line (y = x)
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', linewidth=2, label='Ideal Fit (y = x)')

plt.title('T5: Actual vs Predicted Rainfall', fontsize=14, fontweight='bold')
plt.xlabel('Actual Rainfall (mm)', fontsize=12)
plt.ylabel('Predicted Rainfall (mm)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# STEP 7: Plot 2 — Feature Coefficients Bar Chart
# ----------------------------------------------------------
plt.figure(figsize=(8, 4))
colors = ['#2ca02c' if c >= 0 else '#d62728' for c in model.coef_]
plt.barh(feature_cols, model.coef_, color=colors)
plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
plt.title('T5: Feature Coefficients (Impact on Rainfall)', fontsize=14, fontweight='bold')
plt.xlabel('Coefficient Weight', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.tight_layout()
plt.show()
```

---

### 3. Core Concepts & Regression Formulas Explained

#### 1. The Mathematical Model Equation
$$y = b_0 + b_1 X_1 + b_2 X_2 + b_3 X_3 + \dots + b_n X_n$$
* $b_0$ is the **Intercept** (`model.intercept_`): The baseline target value when all inputs are 0.
* $b_1, b_2, \dots$ are the **Coefficients / Weights** (`model.coef_`): How much $y$ changes when feature $X_i$ increases by 1 unit.

#### 2. Mean Absolute Error (MAE)
$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
* Average error magnitude expressed in the **exact same units** as target variable (e.g., rainfall in mm).

#### 3. Root Mean Squared Error (RMSE)
$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$
* Heavily penalizes large outlier errors because errors are squared before averaging.

#### 4. $R^2$ Score (Coefficient of Determination)
$$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
* Tells what proportion of variance in target $y$ is explained by the input features.

---
---

# 🗣️ Quick Viva Speech Scripts & Q&A

### What to Say in Viva for T4 (Classification Metrics):
> *"Good morning Mam. In **Tutorial 4 (T4)**, I evaluated classification model performance beyond simple accuracy.*
> 1. *I trained a Random Forest classifier on our crop dataset and computed **Precision**, **Recall**, and **F1-Score** using weighted averages.*
> 2. *I generated a **Confusion Matrix Heatmap** to visualize true positives along the diagonal and identify any misclassified crops.*
> 3. *This ensures that even if class distribution is imbalanced, we can verify individual crop prediction reliability."*

### What to Say in Viva for T5 (Multiple Linear Regression):
> *"In **Tutorial 5 (T5)**, I built a Multiple Linear Regression model using several environmental features (N, P, K, temperature, humidity, pH) to predict continuous rainfall.*
> 1. *I extracted the model's intercept and feature coefficient weights to understand which variables have the strongest positive or negative influence on rainfall.*
> 2. *I evaluated prediction quality using **MAE**, **RMSE**, and the **$R^2$ score**.*
> 3. *Finally, I plotted Actual vs. Predicted values against the ideal $y = x$ line to visually inspect prediction errors."*

### Top 4 Viva Questions & Answers:

| Question | Short & Exact Viva Answer |
| :--- | :--- |
| **Q1: Why is Accuracy alone not reliable?** | In imbalanced datasets, predicting only the majority class gives high accuracy while failing on minority classes. Precision and Recall give true per-class insight. |
| **Q2: Why use `average='weighted'` in T4?** | Because Crop Recommendation is a multi-class dataset. Weighted average weights each class's score by its number of test samples (support). |
| **Q3: What is the difference between Simple and Multiple Linear Regression?** | Simple linear regression uses only **1 feature** ($y = b_0 + b_1X$). Multiple linear regression uses **2 or more features** ($y = b_0 + b_1X_1 + b_2X_2 + \dots$). |
| **Q4: Why do we use RMSE instead of MSE?** | MSE has squared units (e.g. $\text{mm}^2$), which is hard to interpret. Taking the square root gives **RMSE**, returning the error back to the original units ($\text{mm}$). |
