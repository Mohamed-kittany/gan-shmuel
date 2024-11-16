import subprocess
import os
import logging
from pathlib import Path
from shutil import copyfile

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the path of the current directory
CURRENT_DIR = Path(__file__).parent
REPO_DIR = CURRENT_DIR / "gan-shmuel"  # Path to the cloned repository
def clone_repository():
    """Clones the Git repository if it doesn't exist locally or initializes it if mounted."""
    if not REPO_DIR.exists():
        logger.info("Repository not found. Cloning repository into 'gan-shmuel' folder...")
        try:
            subprocess.run(['git', 'clone', 'https://github.com/AM8151/gan-shmuel.git', str(REPO_DIR)], check=True)
            logger.info(f"Successfully cloned the repository into {REPO_DIR}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone the repository: {e}")
            raise
    else:
        logger.info("Repository directory exists. Checking Git status...")
        try:
            # Check if it's a git repository
            subprocess.run(['git', 'status'], cwd=REPO_DIR, check=True, capture_output=True)
            logger.info("Git repository found. Proceeding with pulling latest changes.")
        except subprocess.CalledProcessError:
            logger.info("Directory exists but not a Git repository. Initializing...")
            try:
                # Initialize git and set up remote
                subprocess.run(['git', 'init'], cwd=REPO_DIR, check=True)
                subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/AM8151/gan-shmuel.git'], cwd=REPO_DIR, check=True)
                subprocess.run(['git', 'fetch'], cwd=REPO_DIR, check=True)
                logger.info("Git repository initialized successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to initialize git repository: {e}")
                raise

def pull_latest_code():
    """Pull the latest code from the GitHub repository."""
    logger.info("Pulling latest code from GitHub...")
    try:
        try:
            subprocess.run(['git', 'checkout', 'ayala'], cwd=REPO_DIR, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # If branch doesn't exist, create it tracking remote
            subprocess.run(['git', 'checkout', '-b', 'ayala', 'origin/ayala'], cwd=REPO_DIR, check=True)
        
        # Ensure we're tracking the remote branch
        subprocess.run(['git', 'branch', '--set-upstream-to=origin/ayala', 'ayala'], cwd=REPO_DIR, check=True)
        
        # Pull latest changes
        subprocess.run(['git', 'pull'], cwd=REPO_DIR, check=True)
        logger.info("Successfully pulled latest code")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to pull latest code: {e}")
        raise
def copy_env_file(environment):
    """Copy the correct .env file based on the environment."""
    env_file_map = {
        'prod': '/app/.env.prod',   # Path to the prod environment file
        'test': '/app/.env.test',   # Path to the test environment file
    }
    
    # Choose the correct env file based on the environment
    env_file = env_file_map.get(environment)
    if not env_file:
        raise ValueError(f"Unknown environment: {environment}")
    
    # Define the destination path for the .env file
    target_env_path = REPO_DIR / 'billing' / '.env'
    
    # Copy the environment file to the target location
    logger.info(f"Copying {env_file} to {target_env_path}...")
    copyfile(env_file, target_env_path)
    logger.info(f"Successfully copied {env_file} to {target_env_path}")

def execute_docker_compose(commands, service_dir):
    """Executes docker-compose commands using the specified compose file in a given directory."""
    try:
        logger.info(f"Running: docker-compose -f {str(service_dir / 'docker-compose.yml')} {' '.join(commands)}")
        subprocess.run(['docker-compose', '-f', str(service_dir / 'docker-compose.yml')] + commands, check=True)
        logger.info(f"Successfully executed: {' '.join(commands)} in {service_dir}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing docker compose {' '.join(commands)} in {service_dir}: {e}")
        raise

def build_and_deploy(service_dir, environment):
    """Build Docker images and deploy containers for a given service directory."""
    # Step 1: Copy the correct .env file based on the environment
    copy_env_file(environment)
    
    # Step 2: Build Docker images from the updated Dockerfile
    logger.info(f"Building Docker containers for {service_dir}...")
    execute_docker_compose(['build', '--no-cache'], service_dir)

    # Step 3: Start containers and run them
    logger.info(f"Starting Docker containers for {service_dir}...")
    execute_docker_compose(['up', '--build'], service_dir)

def main():
    """Main function to process both billing and weight services."""
    environment = os.getenv('ENV', 'test')  # Default to 'test' if not set
    
    try:
        clone_repository()
        pull_latest_code() 

        # Process both billing and weight services with the correct environment
        build_and_deploy(REPO_DIR / 'billing', environment)
        build_and_deploy(REPO_DIR / 'weight', environment)

        logger.info(f"CI pipeline for both services completed successfully in {environment} environment.")
    
    except Exception as e:
        logger.error(f"CI pipeline failed for one or both services: {e}")
        raise

if __name__ == "__main__":
    main()