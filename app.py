from flask import Flask, request, jsonify
import os
import json
import traceback

app = Flask(__name__)

# 讓中文正常顯示
app.config["JSON_AS_ASCII"] = False


@app.route("/", methods=["POST"])
@app.route("/api/qbi/test", methods=["POST"])
@app.route("/getAnswer", methods=["POST"])
def qbi_test():
    try:
        # QBI 有時用 JSON、有時用網址參數傳資料，兩種都接
        data = request.get_json(silent=True) or {}

        user_input = (
            data.get("ask_input", "")
            or request.args.get("ask_input", "")
        )

        print(f"Qbi 傳來的內容: {user_input}")

        # 固定回覆文字
        response_data = {
            "isContinuum": 0,
            "messageType": "Text",
            "message": {
                "type": "Text",
                "version": "v770",
                "text": "我是外部知識的文字"
            },
            "getData": True
        }

        print(
            "Server Response:",
            json.dumps(response_data, ensure_ascii=False)
        )

        return jsonify(response_data)

    except Exception as e:
        print("發生錯誤:", traceback.format_exc())

        return jsonify({
            "isContinuum": 0,
            "messageType": "Text",
            "message": {
                "type": "Text",
                "version": "v770",
                "text": "程式發生錯誤"
            },
            "getData": True
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
