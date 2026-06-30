from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import random

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # auto-exposes /metrics

USERS = {
    1: {"id": 1, "name": "Archana", "tier": "gold"},
    2: {"id": 2, "name": "Test User", "tier": "silver"},
}

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify(error="not found"), 404
    return jsonify(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)