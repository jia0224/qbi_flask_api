from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get("ask_input", "")

    print("使用者輸入內容：", user_input)

    # === 這裡可以放你要查資料的邏輯 ===
    # 例如模擬查詢結果
    if "費用" in user_input:
        result = "查到一筆報銷資料，狀態：審核中。"
    elif "進度" in user_input:
        result = "目前進度為：會計審核中。"
    else:
        result = "目前沒有相關報銷資料。"

    # === 回傳給 Qbi 的內容 ===
    return jsonify({
        "isContinuum": 0,
        "messageType": "Text",
        "message": {
            "type": "Text",
            "text": [f"Qbi幫你查到：{result}"]
        },
        "getData": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
