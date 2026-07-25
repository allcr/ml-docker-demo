import json
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(8675309)

n = 500
X = rng.normal(size=(n, 4))
true_coef = np.array([2.5, -1.0, 0.3, 4.0])
y = X @ true_coef + 1.5 + rng.normal(scale=0.5, size=n)

model = LinearRegression()
model.fit(X, y)

artifact = {
    "coef": model.coef_.tolist(),
    "intercept": float(model.intercept_),
    "feature_names": ["x1", "x2", "x3", "x4"],
}

with open("model.json", "w") as f:
    json.dump(artifact, f, indent=2)

