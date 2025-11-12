# 這是一個最簡單的 Python 程式，可以接收 Qbi 傳來的文字
from flask import Flask, request, jsonify

# 建立一個小網站伺服器
app = Flask(__name__)

# 當 Qbi 傳資料到這個網址時，我們要接住它
@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    # 從 Qbi 收到的資料（是一個 JSON）
    data = request.get_json(force=True)

    # 把使用者說的話拿出來（Qbi 會放在 ask_input）
    user_input = data.get("ask_input", "(沒有收到資料)")

    print("Qbi 傳來的內容：", user_input)

    # 回傳一個簡單的回覆給 Qbi
    return jsonify({
        "isContinuum": 0,
        "messageType": "Text",
        "message": {
            "type": "Text",
            "text": [f"我收到你的話了：{user_input}"]
        },
        "getData": True
    })

# 讓程式跑起來
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
