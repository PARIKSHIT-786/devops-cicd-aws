import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/")
def index():
    return jsonify(
        message="Hello from the CI/CD pipeline!",
        version=VERSION,
        host=socket.gethostname(),
        time=datetime.now(timezone.utc).isoformat(),
    )


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
