import json
from fastapi import FastAPI
from pydantic import BaseModel

with open("model.json") as f:
    artifact = json.load(f)

coef = artifact["coef"]
intercept = artifact["intercept"]

app = FastAPI(title="linreg-demo")


class PredictRequest(BaseModel):
    x1: float
    x2: float
    x3: float
    x4: float



class PredictResponse(BaseModel):
    prediction: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    x = [req.x1, req.x2, req.x3, req.x4]
    y = sum(c * xi for c, xi in zip(coef, x)) + intercept
    return {"prediction": y}