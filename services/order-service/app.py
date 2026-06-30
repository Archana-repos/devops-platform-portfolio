from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:5000")

ORDERS = {
    101: {"id": 101, "user_id": 1, "item": "Laptop", "amount": 75000},
    102: {"id": 102, "user_id": 2, "item": "Mouse", "amount": 800},
}

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/orders/<int:order_id>")
def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify(error="not found"), 404
    try:
        user_resp = requests.get(f"{USER_SERVICE_URL}/users/{order['user_id']}", timeout=2)
        order_with_user = {**order, "user": user_resp.json()}
        return jsonify(order_with_user)
    except requests.RequestException:
        return jsonify({**order, "user": None, "warning": "user-service unreachable"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)