import subprocess
from pathlib import Path

# Set up paths
# Bring Dockerfile into the same directory as docker-compose.yml
CURRENT_DIR = Path(__file__).parent
DOCKER_COMPOSE_FILE = CURRENT_DIR / 'docker-compose.yml'

def execute_docker_compose(commands):
    """Executes docker-compose commands using the specified compose file."""
    try:
        subprocess.run(['docker', 'compose', '-f', str(DOCKER_COMPOSE_FILE), *commands], check=True)
        print(f"Successfully executed: docker compose {' '.join(commands)}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing docker compose {' '.join(commands)}: {e}")
        raise

def main():
    # Step 1: Build Docker images
    execute_docker_compose(['build', '--no-cache'])

    # Step 2: Deploy the containers
    execute_docker_compose(['up', '-d'])

if __name__ == "__main__":
    main()
