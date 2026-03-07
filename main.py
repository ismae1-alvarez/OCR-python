"""
main.py - ERP Backend minimal para diagnóstico
"""
import os
import io
import re

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "python": "running"})

@app.route("/test-imports")
def test_imports():
    results = {}
    try:
        import fitz
        results["pymupdf"] = fitz.__version__
    except Exception as e:
        results["pymupdf"] = f"ERROR: {e}"
    try:
        import openpyxl
        results["openpyxl"] = openpyxl.__version__
    except Exception as e:
        results["openpyxl"] = f"ERROR: {e}"
    return jsonify(results)

@app.route("/generar-erp", methods=["POST"])
def generar_erp():
    return jsonify({"error": "En mantenimiento - revisando imports"}), 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)