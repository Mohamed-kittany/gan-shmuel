# webhook_listener.py
from flask import Flask, request, jsonify
import ci_pipeline  # ייבוא קובץ ה-CI

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # קבלת המטען של הבקשה מה-webhook
    data = request.json

    # תיעוד הבקשה לצורכי דיבוג
    print("Received webhook:", data)

    # בדיקה אם מדובר באירוע לסניף main
    if data and data.get('ref') == 'refs/heads/main':
        # הפעלת צינור ה-CI
        print("CI pipeline triggered")
        try:
            ci_pipeline.main()
            # החזרת סטטוס 200 במידה שהכל תקין
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"CI pipeline failed: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        # החזרת סטטוס 400 אם האירוע אינו מתאים
        return jsonify({"status": "ignored", "reason": "Not main branch or missing data"}), 400

if __name__ == '__main__':
    app.run(port=5000)

