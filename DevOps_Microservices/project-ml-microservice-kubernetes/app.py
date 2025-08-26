from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import os
import json
import joblib
import pandas as pd

# ----- App & Logging -----
app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

# ----- Model loading -----
MODEL_PATH = "./model_data/boston_housing_prediction.joblib"
REQUIRED_COLS = ["CHAS", "RM", "TAX", "PTRATIO", "B", "LSTAT"]

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found at {MODEL_PATH}. "
        "Make sure you've generated it and copied it into the image."
    )

try:
    clf = joblib.load(MODEL_PATH)
    LOG.info("Model loaded successfully from %s", MODEL_PATH)
except Exception as e:
    LOG.exception("Failed to load model: %s", e)
    raise

# ----- Routes -----
@app.route("/", methods=["GET"])
def home():
    """Health/info endpoint."""
    return "<h3>Sklearn Prediction Service is up</h3>", 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Perform a prediction.

    Expected JSON payload (keys must match REQUIRED_COLS):
    {
      "CHAS": {"0": 0},
      "RM": {"0": 6.575},
      "TAX": {"0": 296.0},
      "PTRATIO": {"0": 15.3},
      "B": {"0": 396.9},
      "LSTAT": {"0": 4.98}
    }

    Returns:
    { "prediction": [ <float>, ... ] }
    """
    try:
        json_payload = request.get_json(force=True, silent=False)
    except Exception:
        # Bad JSON format
        return jsonify(error="Invalid JSON body."), 400

    if not isinstance(json_payload, dict):
        return jsonify(error="JSON payload must be an object/dict."), 400

    LOG.info("JSON payload received:\n%s", json.dumps(json_payload, indent=2))

    payload_cols = set(json_payload.keys())
    missing = [c for c in REQUIRED_COLS if c not in payload_cols]
    extra = [c for c in payload_cols if c not in REQUIRED_COLS]
    if missing:
        return jsonify(error=f"Missing required keys: {missing}"), 400
    if extra:
        # Not fatal, but safer to enforce schema strictly for this project
        return jsonify(error=f"Unexpected keys present: {extra}"), 400

    try:
        df = pd.DataFrame({col: json_payload[col] for col in REQUIRED_COLS})
        df = df[REQUIRED_COLS].astype(float)
    except Exception as e:
        LOG.exception("Failed to construct/convert DataFrame: %s", e)
        return jsonify(error="Could not parse payload into numeric DataFrame."), 400

    LOG.info("Inference DataFrame:\n%s", df)

    try:
        y_pred = clf.predict(df)
    except Exception as e:
        LOG.exception("Model prediction failed: %s", e)
        return jsonify(error="Model prediction failed."), 500
    
    preds = [float(p) for p in y_pred]  # ensure JSON-serializable
    LOG.info("Model prediction: %s", preds)

    return jsonify({"prediction": preds}), 200


if __name__ == "__main__":
    # For local/dev use only; in Docker this will be invoked directly.
    # Flask default logger already configured above.
    app.run(host="0.0.0.0", port=80, debug=True)
