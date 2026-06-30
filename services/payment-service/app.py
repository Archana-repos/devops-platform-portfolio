from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import requests
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:5000")

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/pay/<int:order_id>")
def pay(order_id):
    try:
        order_resp = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", timeout=2)
        if order_resp.status_code != 200:
            return jsonify(error="order not found"), 404
        order = order_resp.json()
        return jsonify(order_id=order_id, amount=order["amount"], status="payment_success")
    except requests.RequestException:
        return jsonify(error="order-service unreachable"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)