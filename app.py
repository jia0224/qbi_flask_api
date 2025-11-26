from flask import Flask, request, jsonify
import os
import traceback
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/", methods=["POST"])
@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    try:
        data = request.get_json(silent=True) or {}
        ask_input = data.get("ask_input") or ""
        print(f"Qbi 傳來的內容: {ask_input}")

        expenses = [
            {"name": "財務部江昱壕人工購置費用", "status": "審核中", "amount": "900"},
            {"name": "全速快遞費", "status": "已生效", "amount": "250"},
            {"name": "AI專案-會議費", "status": "已生效", "amount": "3200"},
        ]
        
        response_text_list = []
        
        response_text_list.append("📌 您的 ECP 報銷紀錄如下：")

        for e in expenses:
            line = f" {e['name']} | {e['status']} | ${e['amount']}"
            response_text_list.append(line)

        response_data = {
            "isContinuum": 0,
            "messageType": "Text",
            "message": {
                "type": "Text",
                "text": response_text_list 
            },
            "getData": True
        }

        # 印出 Log 檢查
        print("Server Response:", json.dumps(response_data, ensure_ascii=False))

        return jsonify(response_data)

    except Exception as e:
        error_msg = traceback.format_exc()
        print("發生錯誤:", error_msg)
        return jsonify({
            "isContinuum": 0,
            "messageType": "Text",
            "message": {
                "type": "Text",
                "text": ["系統發生錯誤", str(e)]
            },
            "getData": True 
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)