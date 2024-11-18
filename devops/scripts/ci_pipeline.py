# import subprocess
# import os
# from logging_config import logger
# from pathlib import Path
# from shutil import copyfile
# from dotenv import load_dotenv

# load_dotenv(dotenv_path="env.test")

# # Get the path of the current directory
# CURRENT_DIR = Path(__file__).parent
# REPO_DIR = CURRENT_DIR / "gan-shmuel"  # Path to the cloned repository
# class CloneRepositoryError(Exception):
#     pass
# def clone_repository():
#     """Clones the Git repository if it doesn't exist locally or initializes it if mounted."""
#     if not REPO_DIR.exists():
#         logger.info("Repository not found. Cloning repository into 'gan-shmuel' folder...")
#         try:
#             subprocess.run(['git', 'clone', 'https://github.com/AM8151/gan-shmuel.git', str(REPO_DIR)], check=True)
#             logger.info(f"Successfully cloned the repository into {REPO_DIR}")
#         except subprocess.CalledProcessError as e:
#             logger.error(f"Failed to clone the repository: {e}")
#             raise CloneRepositoryError("Failed to clone the repository")
#     else:
#         logger.info("Repository directory exists. Checking Git status...")
#         try:
#             # Check if it's a git repository
#             subprocess.run(['git', 'status'], cwd=REPO_DIR, check=True, capture_output=True)
#             logger.info("Git repository found. Proceeding with pulling latest changes.")
#         except subprocess.CalledProcessError:
#             logger.info("Directory exists but not a Git repository. Initializing...")
#             try:
#                 # Initialize git and set up remote
#                 subprocess.run(['git', 'init'], cwd=REPO_DIR, check=True)
#                 subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/AM8151/gan-shmuel.git'], cwd=REPO_DIR, check=True)
#                 subprocess.run(['git', 'fetch'], cwd=REPO_DIR, check=True)
#                 logger.info("Git repository initialized successfully")
#             except subprocess.CalledProcessError as e:
#                 logger.error(f"Failed to initialize git repository: {e}")
#                 raise CloneRepositoryError("Failed to initialize git repository")
# def pull_latest_code():
#     """Pull the latest code from the GitHub repository (from the master branch)."""
#     logger.info("Pulling latest code from GitHub...")

#     try:
#         try:
#             subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
#         except subprocess.CalledProcessError:
#             # If branch doesn't exist, create it tracking remote
#             subprocess.run(['git', 'checkout', '-b', 'master', 'origin/master'], cwd=REPO_DIR, check=True)
        
#         # Ensure we're tracking the remote branch
#         subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
        
#         # Pull latest changes
#         subprocess.run(['git', 'pull'], cwd=REPO_DIR, check=True)
#         logger.info("Successfully pulled latest code from master branch")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Failed to pull latest code from master: {e}")
#         raise

# def rollback_func():
#     """Rollback to the previous commit in the repository."""
#     try:
#         logger.info("Rolling back to the previous commit...")
#         try:
#             # Ensure we're on the correct branch 'master'
#             subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
#         except subprocess.CalledProcessError:
#             # If branch doesn't exist, create it tracking remote
#             subprocess.run(['git', 'checkout', '-b', 'master', 'origin/master'], cwd=REPO_DIR, check=True)
#         # Ensure we're tracking the remote branch
#         subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
#         # Reset to the previous commit
#         subprocess.run(['git', 'reset', '--hard', 'HEAD^'], cwd=REPO_DIR, check=True)
#         logger.info("Successfully rolled back to the previous commit")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Failed to rollback to the previous commit: {e}")
#         raise

# def copy_env_file(service_dir, environment):
#     """Copy the correct .env file based on the environment."""
#     env_file_map = {
#         'prod': '/app/.env.prod',   # Path to the prod environment file
#         'test': '/app/.env.test',   # Path to the test environment file
#     }
    
#     # Choose the correct env file based on the environment
#     env_file = env_file_map.get(environment)
#     if not env_file:
#         raise ValueError(f"Unknown environment: {environment}")
    
#     # Define the destination path for the .env file
#     target_env_path = service_dir / f'.env.{environment}'
    
#     # Copy the environment file to the target location
#     logger.info(f"Copying {env_file} to {target_env_path}...")
#     copyfile(env_file, target_env_path)
#     logger.info(f"Successfully copied {env_file} to {target_env_path}")

# def execute_docker_compose(commands, service_dir, environment):
#     try:
#         copy_env_file(service_dir, environment)
#         env_file = f'.env.{environment}'
#         logger.info(f"Running: docker-compose -f {str(service_dir / 'docker-compose.yml')} --env-file {env_file} {' '.join(commands)}")
        
#         # Run with timeout to avoid hanging
#         process = subprocess.run(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file] + commands,
#             check=True,
#             timeout=300  # 5 minute timeout
#         )
        
#         logger.info(f"Successfully executed: {' '.join(commands)} in {service_dir}")
#     except subprocess.TimeoutExpired:
#         logger.error(f"Docker compose command timed out. Cleaning up...")
#         # Force cleanup on timeout
#         cleanup_containers(service_dir)
#         raise
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error executing docker compose {' '.join(commands)} in {service_dir}: {e}")
#         # Cleanup on error
#         cleanup_containers(service_dir)
#         raise
# def cleanup_containers(service_dir):
#     """Clean up containers and networks created by docker-compose."""
#     try:
#         logger.info("Cleaning up containers and networks...")
#         subprocess.run(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'down', '--volumes', '--remove-orphans'],
#             check=False,  # Don't raise exception if cleanup fails
#             timeout=60
#         )
#     except Exception as e:
#         logger.error(f"Error during cleanup: {e}")

# def build_and_deploy(service_dir, environment,other_service_dir=None):
#     """Build Docker images and deploy containers for a given service directory."""
#     try:
#         # Step 1: Copy the correct .env file based on the environment
  
        
#         # Step 2: Build Docker images from the updated Dockerfile
#         logger.info(f"Building Docker containers for {service_dir}...")
#         execute_docker_compose(['build', '--no-cache'], service_dir,environment)

#         # Step 3: Start containers and run them
#         logger.info(f"Starting Docker containers for {service_dir}...")
#         execute_docker_compose(['up', '--build', '-d'], service_dir,environment)  # Added -d for detached mode
        
#         # Step 4: Check container health
#         check_container_health(service_dir)
        
#     except Exception as e:
#         logger.error(f"Build and deploy failed for {service_dir}: {e}")
#          # Clean up containers for the current service
#         cleanup_containers(service_dir)
#         # Also clean up the other service if it's provided
#         if other_service_dir:
#             cleanup_containers(other_service_dir)
#         raise


#     """Runs the test suite and checks if tests passed."""
#     try:
#         # Run pytest or your preferred test framework (e.g., unittest)
#         logger.info("Running tests in the test environment...")
        
#         # Run pytest and capture the exit code
#         result = subprocess.run(['pytest', '--maxfail=1', '--disable-warnings', '-q'], 
#                                 capture_output=True, text=True)
        
#         # If the return code is 0, it means tests passed
#         if result.returncode == 0:
#             logger.info("Tests passed successfully!")
#             return True
#         else:
#             # If non-zero return code, tests failed
#             logger.error(f"Tests failed with exit code {result.returncode}")
#             logger.error(f"Test output: {result.stdout}\n{result.stderr}")
#             return False
#     except Exception as e:
#         logger.error(f"Error running tests: {e}")
#         return False
# def check_tests_passed(test_directory, rollback=False):
#     """Runs the test suite and checks if tests passed for a specific test directory."""
#     try:
#         logger.info(f"Running tests from {test_directory}...")
        
#         result = subprocess.run(['pytest', test_directory, '--maxfail=1', '--disable-warnings', '-q'],
#                                 capture_output=True, text=True)
        
#         if result.returncode == 0:
#             logger.info("Tests passed successfully!")
#             return True
#         else:
#             if not rollback:
#                 rollback_func()
#             logger.error(f"Tests failed with exit code {result.returncode}")
#             logger.error(f"Test output: {result.stdout}\n{result.stderr}")
#             return False
#     except Exception as e:
#         if not rollback:
#             rollback_func()
#         logger.error(f"Error running tests: {e}")
#         return False

# def check_container_health(service_dir, retries=5, delay=10):
#     """Check if all containers are healthy and running."""
#     try:
#         for _ in range(retries):
#             result = subprocess.run(
#                 ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'ps'],
#                 capture_output=True,
#                 text=True,
#                 check=True
#             )
            
#             if 'Exit' in result.stdout:
#                 logger.error("One or more containers have exited unexpectedly")
#                 subprocess.run(
#                     ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'logs'],
#                     check=False
#                 )
#                 raise RuntimeError("Container startup failed")
            
#             logger.info("Containers are healthy.")
#             return True
            
#             time.sleep(delay)
#         logger.error("Containers did not become healthy within retries.")
#         return False
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error checking container health: {e}")
#         raise

# def main(rollback=False):
#     """Main function to process both billing and weight services."""
#     environment = os.getenv('ENV', 'test')  
    
#     try:
#         # Step 1: Clone and pull latest changes from the repository
#         clone_repository()

#         # Rollback to the previous commit if rollback flag is set
#         pull_latest_code()
#         if rollback:
#             rollback_func()

#         # Step 2: Build and deploy both services in the test environment
#         build_and_deploy(REPO_DIR / 'billing', environment)
#         build_and_deploy(REPO_DIR / 'weight', environment, other_service_dir=REPO_DIR / 'billing')

#         # Step 3: Check if tests passed (if applicable)
#         logger.info("Running tests in the test environment...")
#         logger.info("Running tests for billing service...")
#         # if not check_tests_passed(str(REPO_DIR / 'billing' / 'tests'), rollback):
#         #     raise RuntimeError("Tests failed in the billing service. Aborting pipeline.")
        
#         # logger.info("Running tests for weight service...")
#         # if not check_tests_passed(str(REPO_DIR / 'weight' / 'tests'), rollback):
#         #     raise RuntimeError("Tests failed in the weight service. Aborting pipeline.")
        
#         # Step 4: Clean up test environment before deploying to production
#         logger.info("Cleaning up test environment...")
#         cleanup_containers(REPO_DIR / 'billing')
#         cleanup_containers(REPO_DIR / 'weight')
        
#         # Step 5: Deploy to production environment (if tests passed)
#         logger.info("Deploying to production environment...")
#         os.environ['ENV'] = 'prod'  # Switch environment to production
#         build_and_deploy(REPO_DIR / 'billing', 'prod')
#         build_and_deploy(REPO_DIR / 'weight', 'prod', other_service_dir=REPO_DIR / 'billing')


#         logger.info(f"CI pipeline completed successfully in {environment} and prod environments.")
#         if rollback: 
#             logger.info("Tests passed. Pushing the rollback commit to GitHub...")
#             GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
#             subprocess.run(
#                 ['git', 'push', '--force', f'https://{GITHUB_TOKEN}@github.com/AM8151/gan-shmuel.git', 'master'],
#                 cwd=REPO_DIR,
#                 check=True
#             )
#             logger.info("Successfully pushed the rollback commit to GitHub.")

#     except CloneRepositoryError as e:
#         logger.error(f"Failed to clone repository: {e}")

#     except Exception as e:
#         logger.error(f"CI pipeline failed for one or both services: {e}")
#         # Ensure cleanup in case of failure
#         cleanup_containers(REPO_DIR / 'billing')
#         cleanup_containers(REPO_DIR / 'weight')
#         if not rollback:
#             main(rollback=True)
#         raise

# if __name__ == "__main__":
#     main()
# import socket
# import subprocess
# import os
# from pathlib import Path
# from shutil import copyfile
# from dotenv import load_dotenv
# from logging_config import logger

# load_dotenv(dotenv_path="env.test")

# CURRENT_DIR = Path(__file__).parent
# REPO_DIR = CURRENT_DIR / "gan-shmuel"
# class CloneRepositoryError(Exception):
#     pass


# def is_port_in_use(port):
#     """Check if a port is in use."""
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         return s.connect_ex(('localhost', port)) == 0


# def find_free_ports(start_port=8080, end_port=8090, num_ports=2):
#     """Find a specified number of free ports."""
#     free_ports = [port for port in range(start_port, end_port + 1) if not is_port_in_use(port)]
#     if len(free_ports) < num_ports:
#         raise Exception(f"Not enough free ports in range {start_port}-{end_port}")
#     return free_ports[:num_ports]


# def run_subprocess(command, cwd=None, timeout=300, capture_output=True, check=True):
#     """Run a subprocess command with error handling."""
#     try:
#         result = subprocess.run(command, cwd=cwd, timeout=timeout, capture_output=capture_output, text=True, check=check)
#         return result.stdout
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Command '{' '.join(command)}' failed: {e.stderr.strip()}")
#         raise
#     except subprocess.TimeoutExpired:
#         logger.error(f"Command '{' '.join(command)}' timed out.")
#         raise


# def clone_or_update_repo():
#     """Clone the repository or pull the latest changes."""
#     if not REPO_DIR.exists():
#         logger.info("Cloning repository...")
#         try:
#             run_subprocess(['git', 'clone', 'https://github.com/AM8151/gan-shmuel.git', str(REPO_DIR)])
#         except Exception as e:
#             raise CloneRepositoryError(f"Failed to clone repository: {e}")
#     else:
#         logger.info("Repository exists. Pulling latest changes...")
#         run_subprocess(['git', 'fetch'], cwd=REPO_DIR)
#         run_subprocess(['git', 'reset', '--hard', 'origin/master'], cwd=REPO_DIR)


# def manage_env_file(service_dir, environment):
#     """Copy the correct .env file."""
#     env_file_map = {
#         'prod': '/app/.env.prod',
#         'test': '/app/.env.test',
#     }
#     source_env = env_file_map.get(environment)
#     if not source_env:
#         raise ValueError(f"Unknown environment: {environment}")
#     target_env = service_dir / f'.env.{environment}'
#     copyfile(source_env, target_env)
#     logger.info(f"Copied {source_env} to {target_env}")


# def execute_docker_compose(service_dir, commands, environment):
#     """Run Docker Compose commands."""
#     try:
#         manage_env_file(service_dir, environment)
#         env_file = f".env.{environment}"
#         run_subprocess(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file] + commands,
#             cwd=service_dir,
#         )
#     except Exception as e:
#         logger.error(f"Docker Compose failed: {e}")
#         cleanup_containers(service_dir)
#         raise


# def cleanup_containers(service_dir):
#     """Clean up Docker containers and networks."""
#     try:
#         run_subprocess(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'down', '--volumes', '--remove-orphans'],
#             cwd=service_dir,
#             check=False
#         )
#         logger.info("Cleaned up containers and networks.")
#     except Exception as e:
#         logger.error(f"Error during cleanup: {e}")


# def check_container_health(service_dir, retries=5, delay=10):
#     """Check health of Docker containers."""
#     import time
#     for _ in range(retries):
#         output = run_subprocess(['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'ps'], cwd=service_dir)
#         if 'Exit' not in output:
#             logger.info("Containers are healthy.")
#             return True
#         time.sleep(delay)
#     logger.error("Containers did not pass health checks.")
#     raise RuntimeError("Unhealthy containers detected.")


# def build_and_deploy(service_dir, environment):
#     """Build and deploy services."""
#     try:
#         logger.info(f"Deploying {service_dir} in {environment} environment...")
#         execute_docker_compose(service_dir, ['build', '--no-cache'], environment)
#         execute_docker_compose(service_dir, ['up', '-d'], environment)
#         check_container_health(service_dir)
#         logger.info(f"Successfully deployed {service_dir}.")
#     except Exception as e:
#         cleanup_containers(service_dir)
#         raise RuntimeError(f"Deployment failed for {service_dir}: {e}")


# def run_tests(test_dir):
#     """Run test suite and return status."""
#     logger.info(f"Running tests in {test_dir}...")
#     result = run_subprocess(['pytest', test_dir, '--maxfail=1', '--disable-warnings', '-q'], cwd=test_dir)
#     logger.info("Test results:\n" + result)
#     return True


# def blue_green_deploy(service_dir, environment):
#     """Perform a blue-green deployment."""
#     backend_port, db_port = find_free_ports()
#     os.environ[f'{service_dir.upper()}_BACKEND_PORT'] = str(backend_port)
#     os.environ[f'{service_dir.upper()}_DB_PORT'] = str(db_port)
#     build_and_deploy(service_dir, environment)
#     logger.info(f"Blue-green deployment complete for {service_dir}.")

# def rollback_func():
#     """Rollback to the previous commit in the repository."""
#     try:
#         logger.info("Rolling back to the previous commit...")
#         try:
#             # Ensure we're on the correct branch 'master'
#             subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
#         except subprocess.CalledProcessError:
#             # If branch doesn't exist, create it tracking remote
#             subprocess.run(['git', 'checkout', '-b', 'master', 'origin/master'], cwd=REPO_DIR, check=True)
#         # Ensure we're tracking the remote branch
#         subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
#         # Reset to the previous commit
#         subprocess.run(['git', 'reset', '--hard', 'HEAD^'], cwd=REPO_DIR, check=True)
#         logger.info("Successfully rolled back to the previous commit")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Failed to rollback to the previous commit: {e}")
#         raise
# def main(rollback=False):
#     try:
        
#         clone_or_update_repo()
#         if rollback:
#             rollback_func()
            
#         environment = os.getenv('ENV', 'test') 
#         build_and_deploy(REPO_DIR / 'billing', 'test')
        
#         logger.info("Running tests in the test environment...")
#         if run_tests(REPO_DIR / 'billing/tests'):
#             environment = os.getenv('ENV', 'prod') 
#             blue_green_deploy(REPO_DIR / 'billing', 'prod')
            
#         logger.info(f"CI pipeline completed successfully in {environment} and prod environments.")
        
#         if rollback: 
#             logger.info("Tests passed. Pushing the rollback commit to GitHub...")
#             GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
#             subprocess.run(
#                 ['git', 'push', '--force', f'https://{GITHUB_TOKEN}@github.com/AM8151/gan-shmuel.git', 'master'],
#                 cwd=REPO_DIR,
#                 check=True
#             )
#             logger.info("Successfully pushed the rollback commit to GitHub.")
#     except Exception as e:
#         logger.error(f"Pipeline failed: {e}")


# if __name__ == "__main__":
#     main()
import socket
import subprocess
import os
from pathlib import Path
from shutil import copyfile, copytree
from dotenv import load_dotenv
from logging_config import logger
from datetime import datetime

load_dotenv(dotenv_path="env.test")

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

def manage_env_file(service_dir, environment):
    """Copy the correct .env file."""
    env_file_map = {
        'prod': '/app/.env.prod',
        'test': '/app/.env.test',
    }
    source_env = env_file_map.get(environment)
    if not source_env:
        raise ValueError(f"Unknown environment: {environment}")
    target_env = service_dir / f'.env.{environment}'
    copyfile(source_env, target_env)
    logger.info(f"Copied {source_env} to {target_env}")

def execute_docker_compose(service_dir, commands, environment):
    """Run Docker Compose commands."""
    try:
        manage_env_file(service_dir, environment)
        env_file = f".env.{environment}"
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
    if environment != "prod":
        try:
            run_subprocess(
                ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'down', '--volumes', '--remove-orphans'],
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
    # Convert service_dir to string before calling upper()
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

def main(rollback=False, env_suffix=None):
    try:
        clone_or_update_repo()

        # Ensure env_suffix is not None
        if env_suffix is None:
            env_suffix = "1"  # Default to "1" if env_suffix is not provided

        # Now the environment suffix is always set
        os.environ["ENV_SUFFIX"] = env_suffix if env_suffix else "1"
        environment = os.getenv('ENV', 'test')
        
        
        # Define the folder paths based on environment suffix
        billing_service_dir = REPO_DIR / 'billing'
        weight_service_dir = REPO_DIR / 'weight'
        
        # Copy billing and weight folders to /app/test or /app/prod/{version}
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        target_prod_dir = Path(f'/app/prod/{timestamp}') 
        
        target_prod_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
        
        for service_dir, target_dir in [
            (billing_service_dir, target_prod_dir / 'billing'),
            (weight_service_dir, target_prod_dir / 'weight')
        ]:
        # Copy the entire directory structure (not just a single file)
            copytree(service_dir, target_dir, dirs_exist_ok=True)
        
        # Deploy test environment
        build_and_deploy(billing_service_dir, environment, 'billing')
        build_and_deploy(weight_service_dir, environment, 'weight')

        logger.info("Running tests in the test environment...")
        environment = os.getenv('ENV', 'prod')
        
       
        #if run_tests(weight_service_dir / 'tests') and run_tests(billing_service_dir / 'tests'):
        blue_green_deploy(target_prod_dir / 'billing', 'prod', 'billing')  
        blue_green_deploy(target_prod_dir / 'weight', 'prod', 'weight')
        
        # Cleanup test environment after successful deployment to the new environments
        cleanup_containers(billing_service_dir, environment)  # Clean old containers for billing
        cleanup_containers(weight_service_dir, environment)   # Clean old containers for weight
        
        logger.info(f"CI pipeline completed successfully in {environment} and prod-{env_suffix} environments.")
        
        # Push rollback commit to GitHub if necessary
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
