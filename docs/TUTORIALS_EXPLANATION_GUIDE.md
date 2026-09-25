# 📘 Machine Learning Tutorials (T1, T2, T3) — Master Study & Viva Guide

> [!NOTE]
> **Complete Reference Guide** covering Python Code Architecture, Core Machine Learning Concepts, Viva Speech Scripts, and Lab Notebook Writeups for **Tutorial 1 (T1)**, **Tutorial 2 (T2)**, and **Tutorial 3 (T3)** based on Precision Agriculture Datasets.

---

## 📊 Quick Overview: Tutorials at a Glance

| Tutorial | Focus Area | Key Algorithms / Methods | Primary Deliverable |
| :--- | :--- | :--- | :--- |
| **Tutorial 1 (T1)** | **Data Preprocessing** | `LabelEncoder`, `StandardScaler`, `MinMaxScaler`, `train_test_split` | Clean Numerical Matrix (80% Train, 20% Test) |
| **Tutorial 2 (T2)** | **Linear Regression** | Ordinary Least Squares (OLS), Ridge ($L_2$), Lasso ($L_1$) | Continuous Target Prediction & Regularization Weights |
| **Tutorial 3 (T3)** | **Cross-Validation** | Stratified $K$-Fold ($5$-Fold & $10$-Fold), `learning_curve` | Model Stability Scores & Overfitting/Underfitting Plot |

---

# 🛠️ TUTORIAL 1 (T1): DATA PREPROCESSING

### 📌 1. Objective
To prepare raw, unformatted agricultural datasets (`Crop_recommendation.csv` and `Fertilizer_Prediction.csv`) into clean, scaled, numerical matrices ready for machine learning model training without data leakage.

---

### 💻 2. Step-by-Step Code Execution Map

```
    RAW DATASET (Text strings + Imbalanced Numbers)
                       │
                       ▼
       [ Step 1: Inspection & Cleaning ]
       - Check dataset shape (rows x cols)
       - Run df.isnull().sum() (Verify 0 missing values)
                       │
                       ▼
       [ Step 2: Categorical Encoding ]
       - Apply LabelEncoder on text columns
       - Map: "Clayey" -> 0, "Loamy" -> 1, "Sandy" -> 2
                       │
                       ▼
       [ Step 3: Feature Scaling ]
       - Apply StandardScaler: z = (x - μ) / σ
       - Rescale Nitrogen (0-140) and pH (3-9) to Mean=0, Std=1
                       │
                       ▼
       [ Step 4: Train-Test Data Splitting ]
       - Split 80% Training Data & 20% Testing Data
       - Use stratify=y to maintain equal class proportions
```

---

### 🧠 3. Core Concepts Explained Simply

> [!TIP]
> **Why do we need categorical encoding?**  
> Machine learning models perform linear algebra matrix operations ($X \cdot W$). They cannot calculate distances on string words like `"Clayey"`. Encoding maps words into unique integers ($0, 1, 2...$).

> [!TIP]
> **Why do we need feature scaling?**  
> Soil Nitrogen ranges up to $140$, while pH ranges from $3.5$ to $9.0$. Distance-based models (like KNN) will treat Nitrogen as $20\times$ more important than pH simply because its values are larger. `StandardScaler` normalizes all features onto a zero-mean scale.

---

### 🗣️ 4. What to Say to Mam (Viva Presentation Script)

> *"Good morning Mam. In **Tutorial 1 (T1)**, I built a data preprocessing pipeline for our agricultural datasets.*
>
> 1. *First, I checked for missing values and verified dataset dimensions.*
> 2. *Second, I used `LabelEncoder` to convert string columns like Soil Type and Crop Type into numerical indices so ML algorithms can process them.*
> 3. *Third, I applied `StandardScaler` to normalize features like Nitrogen and pH so high-magnitude values don't dominate smaller features.*
> 4. *Finally, I created an 80/20 stratified train-test split to evaluate our models on unseen data."*

---

### ❓ 5. Quick Viva Questions & Answers for T1

* **Q: Why fit the scaler only on training data and not testing data?**  
  * **A:** To prevent **data leakage**. Fitting on test data leaks test statistics into training, causing fake/overly optimistic accuracy.
* **Q: What does `stratify=y` do in `train_test_split`?**  
  * **A:** It ensures that every crop class (Rice, Maize, Chickpea) is represented in the exact same percentage in both training and testing sets.

---

# 📈 TUTORIAL 2 (T2): LINEAR REGRESSION & REGULARIZATION

### 📌 1. Objective
To build and evaluate Linear Regression models in Python to predict continuous agricultural targets (**Rainfall / Soil Moisture**) and explore **Ridge ($L_2$)** and **Lasso ($L_1$) Regularization** to control the Bias-Variance tradeoff.

---

### 💻 2. Step-by-Step Code Execution Map

```
    FEATURES (N, P, K, Temp, Humidity, pH)  ──>  TARGET (Continuous Rainfall in mm)
                                  │
                                  ▼
           [ Step 1: Feature Matrix & Target Setup ]
           - X = Numeric Soil & Weather Features
           - y = Continuous Rainfall values
                                  │
                                  ▼
           [ Step 2: Train-Test Split & Scaling ]
           - Split 80/20 & scale X using StandardScaler
                                  │
                                  ▼
           [ Step 3: Model Fitting & Evaluation ]
           - Model 1: Ordinary Least Squares (OLS) Linear Regression
           - Model 2: Ridge Regression (L2 Penalty = λ Σ w²)
           - Model 3: Lasso Regression (L1 Penalty = λ Σ |w|)
           - Calculate MAE, MSE, RMSE, and R² Score
                                  │
                                  ▼
           [ Step 4: Performance Visualization ]
           - Plot Actual vs Predicted Rainfall Scatter Plot
           - Plot Feature Coefficients Bar Chart
```

---

### 🧠 3. Core Concepts & Regression Metrics

| Metric / Term | Formula / Definition | What it Tells Us |
| :--- | :--- | :--- |
| **Linear Equation** | $y = b_0 + b_1 X_1 + ... + b_n X_n$ | Finds the optimal straight hyperplane fitting input features to target |
| **MAE** | $\frac{1}{n} \sum \|y - \hat{y}\|$ | Average error distance in original units (mm of rainfall) |
| **RMSE** | $\sqrt{\frac{1}{n} \sum (y - \hat{y})^2}$ | Error in original units, heavily penalizing large outliers |
| **$R^2$ Score** | $1 - \frac{\text{SS}_{res}}{\text{SS}_{tot}}$ | Percentage of variance explained ($0.0 \text{ to } 1.0$; higher is better) |
| **Ridge ($L_2$)** | Penalty $= \lambda \sum w_i^2$ | Shrinks feature weights smoothly to reduce variance without dropping features |
| **Lasso ($L_1$)** | Penalty $= \lambda \sum \|w_i\|$ | Shrinks uninformative feature weights to **exactly 0** (Feature Selection) |

---

### 🗣️ 4. What to Say to Mam (Viva Presentation Script)

> *"In **Tutorial 2 (T2)**, I built a linear regression pipeline to predict continuous rainfall requirements from soil and climate data.*
>
> 1. *I evaluated Ordinary Least Squares (OLS) Linear Regression using MAE, RMSE, and $R^2$ score.*
> 2. *To control the **Bias-Variance tradeoff** and prevent overfitting, I compared **Ridge ($L_2$)** and **Lasso ($L_1$) Regularization**.*
> 3. *The feature coefficient plot demonstrates how Lasso ($L_1$) shrinks uninformative feature weights down to zero, performing automatic feature selection."*

---

### ❓ 5. Quick Viva Questions & Answers for T2

* **Q: What is the difference between Classification and Regression?**  
  * **A:** Classification predicts discrete categories (e.g. Crop Name: Rice vs Maize). Regression predicts continuous numeric values (e.g. Rainfall: 202.5 mm).
* **Q: How does Lasso ($L_1$) perform feature selection?**  
  * **A:** Lasso adds an absolute weight penalty ($\lambda \sum |w|$). As $\lambda$ increases, weights of non-important features are driven to **exactly 0**, effectively removing them.

---

# 🔄 TUTORIAL 3 (T3): CROSS-VALIDATION & LEARNING CURVES

### 📌 1. Objective
To implement **$5$-Fold and $10$-Fold Stratified Cross-Validation** to eliminate single split evaluation bias, measure model stability (Standard Deviation), and plot **Learning Curves** to visually diagnose **Overfitting (High Variance)** vs **Underfitting (High Bias)**.

---

### 💻 2. Step-by-Step Code Execution Map

```
                     FULL DATASET (200 Soil Samples)
                                  │
        ┌─────────────────────────┴─────────────────────────┐
        ▼                                                   ▼
[ 5-Fold Stratified CV ]                        [ Learning Curve Generation ]
- Split data into 5 equal folds                 - Compute scores across 10 sample sizes
- Train on 4 folds, test on 1 fold              - Plot Training Accuracy (Blue)
- Repeat 5 times & average score                - Plot Validation Accuracy (Green)
- Calculate Standard Deviation (Stability)      - Diagnose Overfitting vs Underfitting
```

---

### 🧠 3. Core Concepts & Learning Curve Interpretation

> [!IMPORTANT]
> **Why is single Train-Test Split insufficient?**  
> A single 80/20 split tests the model on only 20% of data. If that 20% happens to be particularly easy or hard by random chance, the accuracy is misleading. $K$-Fold cross-validation ensures **every data point gets tested**.

#### How to Read the Learning Curve Plot:

```
Score
 1.0 ──  ═════════════════════════  <-- Training Score (Stays High)
     │   \
 0.8 ──   \   ────────────────────  <-- Validation Score (Converges)
     │     \ /
 0.0 └───┴───┴───┴───┴───┴───┴───┴
     10% 20% 30% 40% 50% 70% 100% (Training Sample Size)
```

1. **Overfitting (High Variance):** Large gap between high Training Score (~100%) and lower Validation Score.
2. **Underfitting (High Bias):** Both Training Score and Validation Score remain low.
3. **Good Fit:** Both lines converge closely at a high accuracy score.

---

### 🗣️ 4. What to Say to Mam (Viva Presentation Script)

> *"In **Tutorial 3 (T3)**, I implemented **5-Fold and 10-Fold Stratified Cross-Validation** to eliminate evaluation bias from single train-test splits.*
>
> 1. *I computed the mean accuracy and standard deviation across folds to measure model stability.*
> 2. *Finally, I generated **Learning Curves** plotting Training Score versus Validation Score over sample sizes to visually diagnose Overfitting and Underfitting."*

---

### ❓ 5. Quick Viva Questions & Answers for T3

* **Q: What does the Standard Deviation across folds tell us?**  
  * **A:** It measures model **variance/stability**. A low standard deviation means the model performs consistently regardless of how data is split.
* **Q: How do you fix Overfitting if seen on a Learning Curve?**  
  * **A:** Add more training samples, reduce model complexity (limit tree depth), or apply Regularization ($L_1$/$L_2$ penalties).

---

# 📝 LAB NOTEBOOK MASTER COPY ("WHAT I HAVE LEARNED")

> *Copy these exact points into your physical lab record notebook under "Learning Outcomes":*

### **Tutorial 1 (T1: Data Preprocessing)**
1. Raw agricultural soil data cannot be directly fed into machine learning algorithms without cleaning and encoding.
2. Algorithms like KNN are distance-sensitive; without **StandardScaler**, high-magnitude features (Nitrogen) dominate low-magnitude features (pH).
3. Categorical variables (`Soil Type`, `Crop Type`) must be numericalized via **Label Encoding** so algorithms can perform matrix computations.
4. Stratified train-test splitting ($80/20$) prevents data leakage and ensures balanced class representation.

### **Tutorial 2 (T2: Linear Regression)**
1. **Linear Regression** predicts continuous numeric outputs by fitting an optimal linear hyperplane.
2. **$R^2$ score** measures how well independent soil features explain variance in the target variable.
3. **Ridge ($L_2$) and Lasso ($L_1$) Regularization** control model complexity by shrinking feature weights, preventing overfitting and balancing the Bias-Variance tradeoff.

### **Tutorial 3 (T3: Cross-Validation)**
1. A single train-test split can give biased accuracy results depending on random data partitioning.
2. **K-Fold Cross-Validation** provides a robust, unbiased estimate of model generalization across multiple folds.
3. **Learning Curves** visually diagnose model health by plotting training error vs validation error across sample sizes.
