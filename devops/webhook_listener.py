from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # קבלת המטען של הבקשה מה-webhook
    data = request.json

    # תיעוד הבקשה לצורכי דיבוג
    print("Received webhook:", data)

    # בדיקה אם מדובר באירוע ל-main branch
    if data.get('ref') == 'refs/heads/main':
        # כאן אפשר להפעיל את צינור ה-CI
        print("CI pipeline triggered")

        # החזרת סטטוס 200 במידה שהכל תקין
        return jsonify({"status": "success"}), 200
    else:
        # החזרת סטטוס 400 במידה שהאירוע אינו מתאים
        return jsonify({"status": "ignored", "reason": "Not main branch"}), 400

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)


