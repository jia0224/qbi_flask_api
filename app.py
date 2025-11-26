from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
@app.route("/api/qbi/test", methods=["POST"])
def qbi_test():
    data = request.get_json(silent=True) or {}
    ask_input = data.get("ask_input") or ""
    print("Qbi 傳來的內容:", ask_input)

    # 模擬多筆資料（之後可串真實 ECP）
    expenses = [
        {"id": "EXP-250523-00001", "name": "財務部江昱壕人工購置費用", "status": "審核中", "applicant": "江昱壕", "amount": "900"},
        {"id": "EXP-250618-00003", "name": "202507-全速快遞費", "status": "已生效", "applicant": "江昱壕", "amount": "250"},
        {"id": "EXP-250811-00013", "name": "202507-AI專案-會議費", "status": "已生效", "applicant": "江昱壕", "amount": "3200"},
        {"id": "EXP-250818-00001", "name": "202507全速快遞費", "status": "已生效", "applicant": "江昱壕", "amount": "250"}
    ]

    table_rows = [
        "編號 | 名稱 | 狀態 | 申請人 | 金額",
        "------------------------------------------------------------"
    ]

    for e in expenses:
        row = f"{e['id']} | {e['name']} | {e['status']} | {e['applicant']} | {e['amount']}"
        table_rows.append(row)

    return jsonify({
        "isContinuum": 0,
        "messageType": "Multiple",
        "message": {
            "type": "Multiple",
            "items": [
                {
                    "type": "Text",
                    "text": ["📌 以下是您的 ECP 報銷紀錄："]
                },
                {
                    "type": "Text",
                    "text": table_rows
                }
            ]
        },
        "getData": True
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
