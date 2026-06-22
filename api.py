"""
Sentiment Analyzer - Flask version (Railway compatible)
"""
from flask import Flask, request, jsonify, render_template
import os, sys, socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.sentiment_engine import SentimentAnalyzer

app = Flask(__name__, template_folder="templates")
analyzer = SentimentAnalyzer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/face")
def face():
    return render_template("face.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "2.0.0"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "Text tidak boleh kosong"}), 400
    result = analyzer.analyze(data["text"], data.get("language", "auto"))
    return jsonify(result)

@app.route("/analyze/bulk", methods=["POST"])
def analyze_bulk():
    data = request.get_json()
    if not data or not data.get("texts"):
        return jsonify({"error": "Texts tidak boleh kosong"}), 400
    if len(data["texts"]) > 50:
        return jsonify({"error": "Maksimal 50 teks"}), 400
    result = analyzer.analyze_bulk(data["texts"], data.get("language", "auto"))
    return jsonify(result)

@app.route("/stats")
def stats():
    return jsonify(analyzer.get_stats())

@app.route("/history")
def history():
    limit = min(int(request.args.get("limit", 10)), 100)
    return jsonify({"history": analyzer.history[-limit:], "total": len(analyzer.history)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    def get_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: return "localhost"
    print(f"\n{'='*50}")
    print(f"  Sentiment Analyzer v2.0")
    print(f"  Lokal  : http://localhost:{port}")
    print(f"  Jaringan: http://{get_ip()}:{port}")
    print(f"{'='*50}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
