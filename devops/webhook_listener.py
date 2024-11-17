from flask import Flask, request, jsonify
import json
from ci_pipeline import main
from email_service import send_email
import os
from logging_config import logger

app = Flask(__name__)

@app.route('/rollback', methods=['POST'])
def rollback():
    try: 
        # trigger rollback pipeline
        main(rollback=True)
        logger.info("Rollback pipeline executed")
        # Send success email
        send_email(
                subject="Rollback Pipeline Success",
                body=f"Rollback pipeline executed successfully",
                to_addresses=["ayalm1357@gmail.com", "ayalm1357@gmail.com"]
            )
        return jsonify({"status": "success", "message": "Rollback pipeline executed successfully"}), 200
    except Exception as e:
        logger.error(f"Rollback pipeline failed: {e}")
        # Send failure email
        send_email(
            subject="Rollback Pipeline Failed",
            body=f"Rollback pipeline failed.\n\nError: {str(e)}",
            to_addresses=["ayalm1357@gmail.com", "ayalm1357@gmail.com"]
        )
        return jsonify({"status": "error", "message": str(e)}), 500    

@app.route('/health', methods=['POST'])
def health():
    logger.info("Health check endpoint accessed")
    return 'ok'

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    try:
        # Get the payload of the webhook request
        payload = request.json  # Direct access to the JSON payload
        branch_name = payload['ref'].split('/')[-1]  # Get the branch name from the 'ref' field
        author = payload['sender']['login']  # GitHub username of the author
        commit_info = payload['head_commit']  # Commit details
        commit_owner_email = commit_info['author']['email']  # Commit author's email
        time = commit_info['timestamp']  # Commit timestamp

        # Log payload details
        logger.info(f"Webhook received: Commit by {author} to branch {branch_name} at {time}")
        logger.info(f"Commit email: {commit_owner_email}")
        
        # Determine environment based on branch name
        if branch_name in ['master', 'billing', 'weight']:
            environment = 'test'
        else:
            logger.warning(f"Unknown branch: {branch_name}")
            return jsonify({"status": "error", "message": "Unknown branch"}), 400

        logger.info(f"Running CI pipeline for environment: {environment}")
        
        # Call the CI pipeline with the appropriate environment
        try:
            # Set environment variable to control which .env file to load
            os.environ['ENV'] = environment
            main()  # Trigger the pipeline for the test environment
            
            # Run tests after deploying to the test environment
            # if not check_tests_passed():
            #     raise Exception("Tests failed in the test environment")

            # Clean up the test environment after successful tests
            # cleanup_test_environment()
            
            # Now that tests passed, proceed to deploy to production
            os.environ['ENV'] = 'prod'  # Switch environment to production
            main()
            
            # Log success and send success email
            logger.info(f"CI pipeline executed successfully for commit by {author} to branch {branch_name}")
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
            logger.error(f"CI pipeline failed: {e}")
            
            # Send failure email
            send_email(
                subject="CI Pipeline Failed",
                body=f"CI pipeline failed on commit by {author}.\n\nError: {str(e)}",
                to_addresses=["ayalm1357@gmail.com", "ayalm1357@gmail.com"]
            )
            return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": "Invalid payload or processing error"}), 400

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host='0.0.0.0', port=5000)
