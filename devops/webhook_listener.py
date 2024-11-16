from flask import Flask, request, jsonify
import json
from ci_pipeline import main
from email_service import send_email
import os

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # Get the payload of the webhook request
    try:
        payload = request.json  # Direct access to the JSON payload
        branch_name = payload['ref'].split('/')[-1]  # Get the branch name from the 'ref' field
        author = payload['sender']['login']  # GitHub username of the author
        commit_info = payload['head_commit']  # Commit details
        commit_owner_email = commit_info['author']['email']  # Commit author's email
        time = commit_info['timestamp']  # Commit timestamp

        # Print for debugging
        print(f"Commit by {author} to branch {branch_name} at {time}")
        print(f"Commit email: {commit_owner_email}")
        
        # Determine environment based on branch name
        if branch_name == 'master':
            environment = 'prod'  # Use production environment for 'master'
        elif branch_name == 'billing' or branch_name == 'weight':
            environment = 'test'  # Use test environment for other branches

        print(f"Running CI pipeline for environment: {environment}")
        
        # Call the CI pipeline with the appropriate environment
        try:
            # Set environment variable to control which .env file to load
            os.environ['ENV'] = environment
            main()  # Trigger the pipeline with the chosen environment
            
            # Send success email
            send_email(
                subject="CI Pipeline Success",
                body=f"CI pipeline executed successfully on commit by {author}.\n\nCommit email: {commit_owner_email}",
                to_addresses=["ayalm1357@gmail.com", "ayalm1357@gmail.com"]
            )
            
            return jsonify({
                "status": "success",
                "branch": branch_name,
                "author": author,
                "commit_email": commit_owner_email,
                "time": time,
                "environment": environment
            }), 200
        except Exception as e:
            print(f"CI pipeline failed: {e}")
            # Send failure email
            send_email(
                subject="CI Pipeline Failed",
                body=f"CI pipeline failed on commit by {author}.\n\nError: {str(e)}",
                to_addresses=["ayalm1357@gmail.com", "ayalm1357@gmail.com"]
            )
            return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": "Invalid payload or processing error"}), 400

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)