from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get("ask_input", "")
    print("Qbi 傳來的內容：", user_input)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
