from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get("ask_input", "")

    print("使用者輸入內容：", user_input)

    # === 回傳給 Qbi 的內容 ===
    return jsonify({
    "isContinuum": 0,
    "messageType": "Text",
    "message": {
        "type": "Text",
        "text": [f"我已成功接到：{user_input}"]
    },
    "getData": True
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
