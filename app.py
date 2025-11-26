from flask import Flask, request, jsonify
import os
import traceback # 引入 traceback 以便印出錯誤日誌

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
        # 建議：明確使用換行符號 \n 來連接每一行，確保前端能正確顯示換行
        header = "編號 | 名稱 | 狀態 | 申請人 | 金額"
        separator = "------------------------------------------------------------"
        
        # 組合表格內容
        formatted_rows = [header, separator]
        for e in expenses:
            row = f"{e['id']} | {e['name']} | {e['status']} | {e['applicant']} | {e['amount']}"
            formatted_rows.append(row)
        
        # 將陣列轉為單一字串 (安全性較高，避免前端不吃 Array)
        final_table_text = "\n".join(formatted_rows) 
        intro_text = "📌 以下是您的 ECP 報銷紀錄："

        # 4. 回傳成功 JSON
        # 修正重點：根據文件 P.17，Multiple 格式的陣列欄位名稱應為 "ans"，而非 "items"
        return jsonify({
            "isContinuum": 0,
            "messageType": "Multiple",
            "message": {
                "type": "Multiple",
                "version": "v770", # 補上版本號
                "ans": [           # 修正：將 items 改為 ans
                    {
                        "type": "Text",
                        "text": [intro_text] 
                    },
                    {
                        "type": "Text",
                        "text": [final_table_text]
                    }
                ]
            },
            "getData": True
        })

    except Exception as e:
        # 5. 【關鍵】錯誤攔截
        # 如果程式崩潰，這裡會攔截到，並回傳一個「合法的 JSON 錯誤訊息」
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