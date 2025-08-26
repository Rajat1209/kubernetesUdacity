import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# We generate synthetic-but-plausible data matching your API keys.
# Columns: CHAS (0/1), RM (~rooms), TAX, PTRATIO, B, LSTAT
rng = np.random.default_rng(42)
n = 5000

CHAS = rng.integers(0, 2, size=n).astype(float)             # 0 or 1
RM = rng.normal(6.2, 0.8, size=n).clip(3.0, 9.0)            # rooms
TAX = rng.normal(350, 120, size=n).clip(100, 750)           # tax rate
PTRATIO = rng.normal(18.0, 2.5, size=n).clip(12, 25)        # pupil-teacher ratio
B = rng.normal(380, 40, size=n).clip(200, 400)              # "B" stat
LSTAT = rng.normal(12, 7, size=n).clip(1, 40)               # % lower status

X = pd.DataFrame({
    "CHAS": CHAS,
    "RM": RM,
    "TAX": TAX,
    "PTRATIO": PTRATIO,
    "B": B,
    "LSTAT": LSTAT
})

# Create a synthetic target with reasonable relationships
# (More rooms/CHAS/B increases price; higher TAX/PTRATIO/LSTAT decreases)
y = (
    10_000 * CHAS +
    20_000 * (RM - 5) -
    30 * TAX -
    1_000 * (PTRATIO - 15) +
    50 * (B - 350) -
    2_000 * (LSTAT - 10) +
    rng.normal(0, 10_000, size=n)  # noise
)

# Model: Standardize then Gradient Boosting
model = Pipeline([
    ("scaler", StandardScaler(with_mean=True, with_std=True)),
    ("gbr", GradientBoostingRegressor(random_state=42))
])

model.fit(X, y)
pred = model.predict(X)
print(f"Training R^2 on synthetic data: {r2_score(y, pred):.3f}")

# Save to model_data/boston_housing_prediction.joblib
os.makedirs("model_data", exist_ok=True)
out_path = "model_data/boston_housing_prediction.joblib"
joblib.dump(model, out_path)
print(f"Saved model to {out_path}")
