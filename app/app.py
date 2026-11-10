
from flask import Flask, render_template
from prometheus_flask_exporter import PrometheusMetrics
import socket

app = Flask(__name__)

# Enable Prometheus monitoring
metrics = PrometheusMetrics(app)


@app.route("/")
def home():
    return render_template(
        "index.html",
        hostname=socket.gethostname()
    )


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/ready")
def ready():
    return {"status": "ready"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
