# Tutorial 4 (T4): Building Programs to Evaluate Performance Metrics — Detailed Guide

## What is This Tutorial About?

In Tutorial 1 (T1), we preprocessed our data. In Tutorial 2 (T2), we built Linear Regression models and learned regression metrics (MAE, MSE, RMSE, R²). In Tutorial 3 (T3), we used Cross-Validation to ensure our scores are reliable. Now in Tutorial 4 (T4), we answer:

**"How do we comprehensively evaluate and compare classification models?"**

A single accuracy number doesn't tell the whole story. What if your model gets 95% accuracy but completely misses one crop class? We need **Precision**, **Recall**, **F1-Score**, **Confusion Matrices**, and **ROC-AUC** to truly understand model performance.

---

## Key Concepts Explained

### 1. Accuracy
The simplest metric — percentage of correct predictions out of all predictions.

$$\text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Predictions}}$$

**Example:** If our model predicts 180 out of 200 test samples correctly → Accuracy = 90%.

**Limitation:** If 95% of our data is "rice", a model that always predicts "rice" gets 95% accuracy but is useless for other crops!

### 2. Precision (Positive Predictive Value)
Of all samples the model **predicted** as class X, how many were actually class X?

$$\text{Precision} = \frac{TP}{TP + FP}$$

- **TP** (True Positive): Correctly predicted as class X
- **FP** (False Positive): Incorrectly predicted as class X (it was actually something else)

**Example:** Model predicts 20 samples as "rice". 18 are actually rice, 2 are maize.
→ Precision for rice = 18/20 = 0.90

**High Precision = Few false alarms.** Important when false positives are costly.

### 3. Recall (Sensitivity / True Positive Rate)
Of all samples that **actually are** class X, how many did the model find?

$$\text{Recall} = \frac{TP}{TP + FN}$$

- **FN** (False Negative): Actually class X but model predicted something else

**Example:** There are 25 actual rice samples. Model correctly identified 18 of them.
→ Recall for rice = 18/25 = 0.72

**High Recall = Few missed cases.** Important when missing positives is costly.

### 4. F1-Score (Harmonic Mean)
Balances Precision and Recall into a single number.

$$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**Why harmonic mean instead of simple average?** Because it penalizes extreme imbalances. If Precision = 1.0 but Recall = 0.0, the simple average would be 0.5, but F1 = 0.0 (which correctly shows the model is useless for that class).

### 5. Weighted Average (for Multi-Class)
Since our datasets have multiple classes (10 crops, 7 fertilizers), we use **weighted averages** where each class's metric is weighted by how many test samples it has:

$$\text{Weighted Avg} = \frac{\sum_{i} \text{support}_i \times \text{metric}_i}{\sum_{i} \text{support}_i}$$

### 6. Confusion Matrix
A table showing the count of predictions for every (Actual Class, Predicted Class) pair. The diagonal shows correct predictions; off-diagonal shows errors.

```
                Predicted
              rice  maize  chickpea
Actual rice    18     1      1      → 20 actual rice samples
      maize     2    15      0      → 17 actual maize samples
      chickpea  0     1     12      → 13 actual chickpea samples
```

### 7. ROC-AUC (Receiver Operating Characteristic — Area Under Curve)
For each class, ROC plots True Positive Rate vs. False Positive Rate at various classification thresholds. AUC = 1.0 is perfect, AUC = 0.5 is random guessing.

For multi-class problems, we use **One-vs-Rest (OvR)**: treat each class as "positive" vs. all others as "negative".

---

## Models Used in This Tutorial

| Model | How It Works | Strengths | Weaknesses |
|-------|-------------|-----------|------------|
| **Random Forest** | Ensemble of many Decision Trees, each trained on random data subsets | High accuracy, handles non-linearity, gives feature importance | Slower to train, less interpretable |
| **Decision Tree** | Single tree of if-else rules based on feature thresholds | Fast, easy to visualize and explain | Prone to overfitting |
| **KNN (K=5)** | Classifies based on 5 nearest neighbors in feature space | Simple, no training phase | Slow on large data, sensitive to scaling |
| **SVM (RBF)** | Finds optimal hyperplane with RBF kernel for non-linear boundaries | Effective in high dimensions | Slow on large datasets, needs scaling |

---

## Step-by-Step What the Code Does

### Step 0: Setup
- Import all required libraries (sklearn metrics, classifiers, plotting)
- If running in Google Colab without the CSV files, auto-generate sample data

### Steps 1A–6A: Crop Recommendation Dataset
1. **Load & Preprocess** — Read CSV, define features (N, P, K, temperature, humidity, ph, rainfall), scale with StandardScaler, 80/20 stratified split
2. **Train 4 Models** — Random Forest, Decision Tree, KNN, SVM all trained on the same data
3. **Compute Metrics** — Accuracy, Precision, Recall, F1 (all weighted) in a comparison table
4. **Classification Report** — Per-class breakdown for each model
5. **Confusion Matrix Heatmaps** — 2×2 grid showing all 4 models
6. **Metrics Bar Chart** — Visual comparison of all metrics across models

### Steps 1B–6B: Fertilizer Prediction Dataset
Same pipeline applied to the fertilizer dataset (with categorical encoding for Soil Type and Crop Type)

### Steps 7–10: Combined Analysis
7. **Combined Summary Table** — Both datasets side-by-side with best model identified
8. **Combined Accuracy Chart** — Crop vs. Fertilizer accuracy for each model
9. **ROC-AUC Curves** — One-vs-Rest ROC for each crop class using Random Forest
10. **Feature Importance** — Which features matter most for each dataset

---

## How to Interpret the Results

### Reading the Metrics Table
```
Model           Accuracy   Precision   Recall   F1-Score
Random Forest   0.9500     0.9520      0.9500   0.9490
Decision Tree   0.8800     0.8850      0.8800   0.8790
KNN (K=5)       0.9200     0.9230      0.9200   0.9180
SVM (RBF)       0.9400     0.9410      0.9400   0.9390
```

- **Best overall**: Highest F1-Score (balances precision and recall)
- **If precision ≈ recall**: Model is balanced across classes
- **If precision >> recall**: Model is conservative (few false positives, but misses many)
- **If recall >> precision**: Model is aggressive (catches most, but many false alarms)

### Reading the Confusion Matrix
- **Dark diagonal** = Most predictions are correct
- **Off-diagonal values** = Specific misclassifications to investigate
- Example: If rice is often confused with maize, the (rice, maize) cell will be high

### Reading ROC-AUC
- **AUC close to 1.0** for a class → Model separates that class very well
- **AUC close to 0.5** for a class → Model struggles with that class (random guessing)

---

## Connecting to Previous Tutorials

| Tutorial | What We Learned | How T4 Uses It |
|----------|----------------|---------------|
| **T1** | Data cleaning, encoding, scaling, splitting | T4 applies the same preprocessing pipeline before training |
| **T2** | Regression metrics (MAE, MSE, R²) | T4 extends to **classification** metrics (Precision, Recall, F1) |
| **T3** | Cross-validation for reliable scores | T4 evaluates on a held-out test set; cross-validation could be added for even more robust metrics |

---

## Common Viva Questions & Answers

**Q: Why is accuracy not enough?**
A: In imbalanced datasets, a model can get high accuracy by always predicting the majority class. Precision and Recall reveal per-class performance.

**Q: When would you prefer Precision over Recall?**
A: When false positives are costly. Example: Recommending an expensive fertilizer incorrectly wastes money. High precision ensures recommendations are reliable.

**Q: When would you prefer Recall over Precision?**
A: When false negatives are costly. Example: Failing to detect a disease-prone crop condition means crop loss. High recall ensures we catch all risky cases.

**Q: What does F1-Score represent?**
A: The harmonic mean of Precision and Recall. It's the single best metric when you need to balance both. F1 = 1.0 is perfect, F1 = 0.0 means the model fails on either precision or recall.

**Q: Why use weighted average for multi-class?**
A: To account for class imbalance. Classes with more test samples contribute more to the overall score, giving a realistic picture of real-world performance.

**Q: What does the confusion matrix diagonal tell us?**
A: The diagonal shows correct predictions (True Positives for each class). A perfect model has all values on the diagonal and zeros everywhere else.

**Q: How does ROC-AUC work for multi-class?**
A: We use One-vs-Rest (OvR) — for each class, we treat it as "positive" and all others as "negative", then compute a separate ROC curve and AUC score.
