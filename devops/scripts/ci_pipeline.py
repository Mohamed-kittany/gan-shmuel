
import socket
import subprocess
import os
from pathlib import Path
from shutil import copyfile, copytree, ignore_patterns
from dotenv import load_dotenv
from logging_config import logger
from datetime import datetime



CURRENT_DIR = Path(__file__).parent
REPO_DIR = CURRENT_DIR / "gan-shmuel"


class CloneRepositoryError(Exception):
    pass

def is_port_in_use(port):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_free_ports(service_type, start_port=8080, end_port=8090, num_ports=2):
    """Find a specified number of free ports for different services."""
    db_ports_map = {
        'weight': [3306, 3308],
        'billing': [3307, 3309]
    }
    
    if service_type not in db_ports_map:
        raise ValueError(f"Unknown service type: {service_type}")
    
    db_ports = db_ports_map[service_type]
    free_ports = [port for port in db_ports if not is_port_in_use(port)]
    
    if len(free_ports) < num_ports:
        raise Exception(f"Not enough free DB ports for {service_type}.")
    
    return free_ports[:num_ports]

def run_subprocess(command, cwd=None, timeout=300, capture_output=True, check=True):
    """Run a subprocess command with error handling."""
    try:
        result = subprocess.run(command, cwd=cwd, timeout=timeout, capture_output=capture_output, text=True, check=check)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(command)}' failed: {e.stderr.strip()}")
        raise
    except subprocess.TimeoutExpired:
        logger.error(f"Command '{' '.join(command)}' timed out.")
        raise

def clone_or_update_repo():
    """Clone the repository or pull the latest changes."""
    if not REPO_DIR.exists():
        logger.info("Cloning repository...")
        try:
            run_subprocess(['git', 'clone', 'https://github.com/AM8151/gan-shmuel.git', str(REPO_DIR)])
        except Exception as e:
            raise CloneRepositoryError(f"Failed to clone repository: {e}")
    else:
        logger.info("Repository exists. Pulling latest changes...")
        run_subprocess(['git', 'fetch'], cwd=REPO_DIR)
        run_subprocess(['git', 'reset', '--hard', 'origin/master'], cwd=REPO_DIR)


def execute_docker_compose(service_dir, commands, environment):
    """Run Docker Compose commands."""
    try:
        # manage_env_file(service_dir, environment)
        env_file = f".env.{environment}"
        logger.info(str(service_dir / 'docker-compose.yml'))
        run_subprocess(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file] + commands,
            cwd=service_dir,
        )
    except Exception as e:
        logger.error(f"Docker Compose failed: {e}")
        cleanup_containers(service_dir, environment)
        raise

def cleanup_containers(service_dir, environment):
    """Clean up Docker containers and networks only for the test environment."""
    try:
        run_subprocess(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'down'],
            cwd=service_dir,
            check=False
        )
        logger.info("Cleaned up containers and networks.")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

def check_container_health(service_dir, retries=5, delay=10):
    """Check health of Docker containers."""
    import time
    for _ in range(retries):
        output = run_subprocess(['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'ps'], cwd=service_dir)
        if 'Exit' not in output:
            logger.info("Containers are healthy.")
            return True
        time.sleep(delay)
    logger.error("Containers did not pass health checks.")
    raise RuntimeError("Unhealthy containers detected.")

def build_and_deploy(service_dir, environment, service_type):
    """Build and deploy services."""
    try:
        logger.info(f"Deploying {service_dir} in {environment} environment...")
        execute_docker_compose(service_dir, ['build', '--no-cache'], environment)
        execute_docker_compose(service_dir, ['up', '-d'], environment)
        check_container_health(service_dir)
        
        logger.info(f"Successfully deployed {service_dir}.")
    except Exception as e:
        cleanup_containers(service_dir, environment)
        raise RuntimeError(f"Deployment failed for {service_dir}: {e}")

def run_tests(test_directory, rollback=False):
    """Runs the test suite and checks if tests passed for a specific test directory."""
    try:
        logger.info(f"Running tests from {test_directory}...")
        
        result = subprocess.run(['pytest', test_directory, '--maxfail=1', '--disable-warnings', '-q'],
                                capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Tests passed successfully!")
            return True
        else:
            if not rollback:
                rollback_func()
            logger.error(f"Tests failed with exit code {result.returncode}")
            logger.error(f"Test output: {result.stdout}\n{result.stderr}")
            return False
    except Exception as e:
        if not rollback:
            rollback_func()
        logger.error(f"Error running tests: {e}")
        return False




def blue_green_deploy(service_dir, environment, service_type):
    """Perform a blue-green deployment."""
    backend_port, db_port = find_free_ports(service_type)
    os.environ[f'{str(service_dir).upper()}_BACKEND_PORT'] = str(backend_port)
    os.environ[f'{str(service_dir).upper()}_DB_PORT'] = str(db_port)
    build_and_deploy(service_dir, environment, service_type)
    logger.info(f"Blue-green deployment complete for {service_dir}.")


def rollback_func():
    """Rollback to the previous commit in the repository."""
    try:
        logger.info("Rolling back to the previous commit...")
        subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
        subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
        subprocess.run(['git', 'reset', '--hard', 'HEAD^'], cwd=REPO_DIR, check=True)
        logger.info("Successfully rolled back to the previous commit")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to rollback to the previous commit: {e}")
        raise
def log_environment_variables():
        logger.info("Current environment variables:")
        for key, value in os.environ.items():
            logger.info(f"{key}: {value}")
def load_environment(env_file):
    """Load environment variables from file, overriding existing ones."""
    # Clear relevant environment variables before loading new ones
    env_vars_to_clear = [
        'BILLING_BACKEND_PORT',
        'BILLING_DB_PORT',
        'WEIGHT_BACKEND_PORT',
        'WEIGHT_DB_PORT',
        'BILLING_MYSQL_DATABASE_PASSWORD',
        'BILLING_MYSQL_DATABASE_DB',
        'NETWORK_NAME',
        'ENV',
        # Add any other environment variables that need to be cleared
    ]
    
    for var in env_vars_to_clear:
        if var in os.environ:
            del os.environ[var]
    
    # Load new environment variables
    load_dotenv(dotenv_path=env_file, override=True)
    
    # Set ENV explicitly
    environment = 'test' if env_file.endswith('.test') else 'prod'
    os.environ['ENV'] = environment
    
    return environment

def main(rollback=False, env_suffix=None):
    try:
        logger.info("Starting CI pipeline...")
        clone_or_update_repo()

        # Ensure env_suffix is not None
        if env_suffix is None:
            env_suffix = "1"  # Default to "1" if env_suffix is not provided

        os.environ["ENV_SUFFIX"] = env_suffix

        # Load test environment
        environment = load_environment(".env.test")
        logger.info(f"Loaded test environment variables:")
        log_environment_variables()

        # Define the folder paths
        billing_service_dir = REPO_DIR / 'billing'
        weight_service_dir = REPO_DIR / 'weight'
        
        # Set up production directory
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        target_prod_dir = Path(f'/app/prod/{timestamp}')
        target_prod_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the directories
        for service_dir, target_dir in [
            (billing_service_dir, target_prod_dir / 'billing'),
            (weight_service_dir, target_prod_dir / 'weight')
        ]:
            logger.info(f"Starting to copy service from {service_dir} to {target_dir}")
            copytree(service_dir, target_dir, ignore=ignore_patterns(), dirs_exist_ok=True, copy_function=copyfile)

        # Deploy test environment
        build_and_deploy(billing_service_dir, environment, 'billing')
        build_and_deploy(weight_service_dir, environment, 'weight')

        logger.info("Running tests in the test environment...")
        
        # Clean up test containers
        cleanup_containers(billing_service_dir, environment)
        cleanup_containers(weight_service_dir, environment)
        
        # Load production environment
        environment = load_environment(".env.prod")
        logger.info(f"Loaded production environment variables:")
        log_environment_variables()
        
        logger.info(f"Deploying to production environment...")
        blue_green_deploy(target_prod_dir / 'billing', environment, 'billing')
        blue_green_deploy(target_prod_dir / 'weight', environment, 'weight')
        
        logger.info(f"CI pipeline completed successfully in {environment} environment.")
        
        # Handle rollback if necessary
        if rollback:
            logger.info("Tests passed. Pushing the rollback commit to GitHub...")
            GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
            subprocess.run(
                ['git', 'push', '--force', f'https://{GITHUB_TOKEN}@github.com/AM8151/gan-shmuel.git', 'master'],
                cwd=REPO_DIR,
                check=True
            )
            logger.info("Successfully pushed the rollback commit to GitHub.")
            
    except Exception as e:
        logger.error(f"Error: {e}")
        raise

if __name__ == '__main__':
    main()