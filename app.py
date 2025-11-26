from flask import Flask, request, jsonify
import os
import traceback
import json  # 引入 json 用於日誌列印

app = Flask(__name__)

@app.route("/", methods=["POST"])
@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    try:
        # 1. 接收資料
        data = request.get_json(silent=True) or {}
        ask_input = data.get("ask_input") or ""
        print(f"Qbi 傳來的內容: {ask_input}")

        # 2. 模擬資料邏輯
        expenses = [
            {"id": "EXP-250523-00001", "name": "財務部江昱壕人工購置費用", "status": "審核中", "applicant": "江昱壕", "amount": "900"},
            {"id": "EXP-250618-00003", "name": "202507-全速快遞費", "status": "已生效", "applicant": "江昱壕", "amount": "250"},
            {"id": "EXP-250811-00013", "name": "202507-AI專案-會議費", "status": "已生效", "applicant": "江昱壕", "amount": "3200"},
            {"id": "EXP-250818-00001", "name": "202507全速快遞費", "status": "已生效", "applicant": "江昱壕", "amount": "250"}
        ]

        # 3. 格式化表格
        header = "編號 | 名稱 | 狀態 | 申請人 | 金額"
        separator = "------------------------------------------------------------"
        
        formatted_rows = [header, separator]
        for e in expenses:
            row = f"{e['id']} | {e['name']} | {e['status']} | {e['applicant']} | {e['amount']}"
            formatted_rows.append(row)
        
        final_table_text = "\n".join(formatted_rows) 
        intro_text = "📌 以下是您的 ECP 報銷紀錄："

        # 4. 回傳成功 JSON (降級策略：改用最穩定的 Text 格式)
        # 根據文件 P.9，Text 類型的 text 欄位是一個字串陣列
        # 我們可以把「介紹語」和「表格」分開放在陣列中，顯示效果類似
        response_data = {
            "isContinuum": 0,
            "messageType": "Text",  # 改回基礎 Text 類型，避免 Multiple 結構被擋
            "message": {
                "type": "Text",
                "version": "v770",
                "text": [
                    intro_text,
                    final_table_text
                ]
            },
            "getData": True
        }

        # [除錯用] 在伺服器端印出我們要回傳的 JSON，確保結構正確
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
                "text": [f"系統發生內部錯誤，請聯繫管理員。\n錯誤原因: {str(e)}"]
            },
            "getData": True 
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)