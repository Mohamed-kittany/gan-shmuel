from flask import Flask, request, jsonify
import json
import ci_pipeline  # ייבוא קובץ ה-CI

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # קבלת המטען של הבקשה מה-webhook
    try:
        payload = request.json  # גישה ישירה למטען JSON
        branch_name = payload['ref'].split('/')[-1]  # הוצאת שם הסניף מתוך ה-ref
        author = payload['sender']['login']  # שם המשתמש של השולח
        commit_info = payload['head_commit']  # מידע אודות ה-commit
        commit_owner_email = commit_info['author']['email']  # כתובת אימייל של מחבר ה-commit
        time = commit_info['timestamp']  # זמן ה-commit

        # הדפסת מידע לצורכי דיבוג
        print(f"Commit by {author} to branch {branch_name} at {time}")
        print(f"Commit email: {commit_owner_email}")
        
        # אם מדובר בסניף 'main'
        if branch_name == 'main':
            print("CI pipeline triggered")
            try:
                ci_pipeline.main()  # הפעלת צינור ה-CI
                # החזרת סטטוס 200 במידה שהכל תקין
                return jsonify({
                    "status": "success",
                    "branch": branch_name,
                    "author": author,
                    "commit_email": commit_owner_email,
                    "time": time
                }), 200
            except Exception as e:
                print(f"CI pipeline failed: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        else:
            # אם הסניף לא main, תחזיר תשובה מתאימה
            return jsonify({
                "status": "ignored",
                "reason": "Not a main branch commit"
            }), 400

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": "Invalid payload or processing error"}), 400

if __name__ == '__main__':

     app.run(host='0.0.0.0', port=5000)

