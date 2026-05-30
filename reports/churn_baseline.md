# Churn Model — Baseline Report

## Logistic Regression (baseline)

- **model**: Logistic Regression
- **class_weight**: balanced
- **roc_auc_train**: 0.8998
- **roc_auc_val**: 0.9046
- **avg_precision_val**: 0.9366
- **f1_val**: 0.8015
- **accuracy_val**: 0.8018

## Classification Report (Validation)

```
              precision    recall  f1-score   support

    Retained       0.71      0.92      0.80       344
     Churned       0.92      0.71      0.80       448

    accuracy                           0.80       792
   macro avg       0.82      0.82      0.80       792
weighted avg       0.83      0.80      0.80       792
```
