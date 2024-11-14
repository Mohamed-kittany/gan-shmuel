from python_on_whales import docker
import logging
import os
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_project_root():
    """Find the project root directory (where docker-compose.yml is located)"""
    current = Path.cwd()
    while current != current.parent:
        # Look for docker-compose.yml in the /app/scripts folder (since it's mounted there)
        if (current / 'docker-compose.yml').exists() or (current / 'scripts/docker-compose.yml').exists():
            return current
        current = current.parent
    raise FileNotFoundError("Could not find docker-compose.yml in any parent directory")

def execute_docker_compose(commands):
    """
    Executes docker-compose commands with proper build context
    """
    try:
        # Explicitly set the working directory to /app/scripts
        project_root = Path("/app/scripts")  # Directly use the path where docker-compose.yml is located
        os.chdir(project_root)

        logger.info(f"Project root directory: {project_root}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Directory contents: {os.listdir()}")

        # Verify required files exist
        required_files = ['docker-compose.yml', 'Dockerfile']
        for file in required_files:
            file_path = project_root / file
            if not file_path.exists():
                raise FileNotFoundError(f"Required file {file} not found at {file_path}")
            logger.info(f"Found {file} at {file_path}")

        # Use subprocess for better control and error handling
        cmd = ['docker', 'compose'] + commands
        logger.info(f"Executing command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(project_root)  
        )

        logger.info("Command stdout:")
        logger.info(result.stdout)

        if result.stderr:
            logger.warning("Command stderr:")
            logger.warning(result.stderr)

    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}")
        logger.error(f"Command stdout: {e.stdout}")
        logger.error(f"Command stderr: {e.stderr}")
        raise Exception(f"Docker compose command failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Error executing docker compose command: {e}")
        raise

def main():
    try:
        logger.info("Starting CI pipeline execution")

        # Execute docker compose commands
        execute_docker_compose(['up', '--build', '--detach'])

        logger.info("CI pipeline completed successfully")

    except Exception as e:
        logger.error(f"CI pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
