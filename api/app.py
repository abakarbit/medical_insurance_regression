#!/usr/bin/env python3
"""API Flask — Prediksi Biaya Asuransi Kesehatan (Medical Insurance Cost).

Model: Linear Regression (sama dengan laporan praktikum).
Jalankan:  python app.py            -> http://127.0.0.1:5000

Endpoint:
  GET  /         info layanan
  GET  /health   status + metrik model
  POST /predict  prediksi charges dari JSON

Contoh curl:
  curl http://127.0.0.1:5000/health
  curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" \
       -d '{"age": 40, "sex": "male", "bmi": 30.5, "children": 2, "smoker": "no", "region": "southeast"}'
"""
import os, pickle
import pandas as pd
from flask import Flask, jsonify, request

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "model.pkl"), "rb") as f:
    BUNDLE = pickle.load(f)
MODEL = BUNDLE["model"]
FEATURES = BUNDLE["feature_columns"]
METRICS = BUNDLE["metrics"]
ALLOWED = METRICS["allowed_values"]  # {'sex': [...], 'smoker': [...], 'region': [...]}

RANGES = {"age": (0, 120), "bmi": (10.0, 70.0), "children": (0, 15)}
REQUIRED = ["age", "sex", "bmi", "children", "smoker", "region"]

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify({
        "service": "Prediksi Biaya Asuransi Kesehatan",
        "model": METRICS["model"],
        "endpoints": {
            "GET /health": "status dan metrik model",
            "POST /predict": "prediksi charges (USD) dari data nasabah",
        },
        "contoh_body_predict": {
            "age": 40, "sex": "male", "bmi": 30.5, "children": 2,
            "smoker": "no", "region": "southeast",
        },
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "model": METRICS["model"],
        "r2_test": METRICS["r2_test"],
        "mae_usd": METRICS["mae_usd"],
        "rmse_usd": METRICS["rmse_usd"],
        "train_size": METRICS["train_size"],
        "test_size": METRICS["test_size"],
    })


def validate(data):
    """Kembalikan (error_message, status) atau (None, 200) bila valid."""
    if not isinstance(data, dict):
        return "Body harus berupa JSON object.", 400
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        return f"Field wajib belum diisi: {', '.join(missing)}.", 400
    for field, (lo, hi) in RANGES.items():
        v = data[field]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return f"Field '{field}' harus berupa angka.", 400
        if not (lo <= float(v) <= hi):
            return f"Field '{field}' di luar rentang wajar ({lo}-{hi}).", 400
    for field in ("sex", "smoker", "region"):
        if data[field] not in ALLOWED[field]:
            return (f"Field '{field}' tidak valid. Pilihan: "
                    f"{', '.join(ALLOWED[field])}."), 400
    return None, 200


def to_features(data):
    row = {c: 0.0 for c in FEATURES}
    row["age"] = float(data["age"])
    row["bmi"] = float(data["bmi"])
    row["children"] = float(data["children"])
    for field in ("sex", "smoker", "region"):
        k = f"{field}_{data[field]}"
        if k in row:  # kategori baseline (drop_first) memang tidak punya kolom
            row[k] = 1.0
    return pd.DataFrame([row], columns=FEATURES)


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="Body tidak valid: kirim JSON dengan Content-Type: application/json."), 400
    err, status = validate(data)
    if err:
        return jsonify(error=err), status
    pred = float(MODEL.predict(to_features(data))[0])
    return jsonify({
        "prediction_usd": round(pred, 2),
        "input": {k: data[k] for k in REQUIRED},
        "model": METRICS["model"],
        "catatan": "Estimasi biaya asuransi tahunan (charges) dalam USD.",
    })


@app.errorhandler(404)
def not_found(_e):
    return jsonify(error="Endpoint tidak ditemukan. Lihat GET / untuk daftar endpoint."), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
