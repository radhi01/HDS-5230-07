import pandas as pd
import xgboost as xgb
from sklearn.model_selection import cross_val_score, KFold
import time, numpy as np

# Config
file = "generated_pima_data_100M.csv"
sizes = [100, 1000, 10000, 100000, 1000000, 10000000]
cols_x = ['pregnant', 'glucose', 'pressure', 'triceps', 'insulin', 'mass', 'pedigree', 'age']
col_y = 'outcome'
folds = 5
res = []

print(f"Running XGBoost on {file}\n" + "-"*40)

def run_cv(X, y):
    model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False)
    cv = KFold(n_splits=folds, shuffle=True, random_state=42)
    t0 = time.time()
    acc = cross_val_score(model, X, y, cv=cv, scoring='accuracy', n_jobs=-1)
    return np.mean(acc), time.time() - t0

for sz in sizes:
    print(f"\nSize: {sz}")
    try:
        t0 = time.time()
        df = pd.read_csv(file, nrows=sz)
        print(f"Loaded in {time.time() - t0:.2f}s")

        if not all(c in df.columns for c in cols_x + [col_y]):
            raise ValueError("Missing columns")

        X, y = df[cols_x], df[col_y].astype(int)
        print("Running CV...")
        acc, t_cv = run_cv(X, y)
        print(f"CV: {t_cv:.2f}s | Acc: {acc:.4f}")

        res.append({"Method": "XGBoost (CV)", "Size": sz, "Accuracy": acc, "CV Time (s)": t_cv})

    except Exception as e:
        print(f"Error: {e}")
        res.append({"Method": "XGBoost (CV)", "Size": sz, "Accuracy": "Error", "CV Time (s)": "Error"})

# Report
print("\n" + "="*40)
print("           Summary")
print("="*40)
df_res = pd.DataFrame(res)
print(df_res.to_string(index=False))
df_res.to_csv("xgb_results.csv", index=False)
print("\nSaved to xgb_results.csv")
