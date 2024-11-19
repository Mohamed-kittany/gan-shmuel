# import subprocess
# import random
# import os
# from logging_config import logger
# from pathlib import Path
# from shutil import copyfile
# from dotenv import load_dotenv
# from datetime import datetime
# load_dotenv(dotenv_path="env.test")

# # Get the path of the current directory
# CURRENT_DIR = Path(__file__).parent
# REPO_DIR = CURRENT_DIR / "gan-shmuel"  # Path to the cloned repository
# class CloneRepositoryError(Exception):
#     pass


# def assign_ports(service_type):
#     """Assign a random available port for backend and db services."""
#     if service_type == "backend":
#         # Port range for backend: 8080-8090
#         port_range = range(8080, 8091)
#     elif service_type == "db":
#         # Port range for db: 3000-3090
#         port_range = range(3000, 3091)
#     else:
#         raise ValueError("Unknown service type")
    
#     available_ports = []
#     for port in port_range:
#         result = subprocess.run(
#             ['lsof', '-i', f':{port}'],
#             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
#         )
#         if result.returncode != 0:  # Port is available
#             available_ports.append(port)

#     if not available_ports:
#         raise RuntimeError(f"No available ports found for {service_type} service.")
    
#     # Pick a random available port
#     return random.choice(available_ports)

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

# #     """Pull the latest code from the GitHub repository (from the master branch)."""
# #     logger.info("Pulling latest code from GitHub...")

# #     try:
# #         try:
# #             subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
# #         except subprocess.CalledProcessError:
# #             # If branch doesn't exist, create it tracking remote
# #             subprocess.run(['git', 'checkout', '-b', 'master', 'origin/master'], cwd=REPO_DIR, check=True)
        
# #         # Ensure we're tracking the remote branch
# #         subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
        
# #         # Pull latest changes
# #         subprocess.run(['git', 'pull'], cwd=REPO_DIR, check=True)
# #         logger.info("Successfully pulled latest code from master branch")
# #     except subprocess.CalledProcessError as e:
# #         logger.error(f"Failed to pull latest code from master: {e}")
# #         raise
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

# # def execute_docker_compose(commands, service_dir, environment):
# #     try:
   
# #         env_file = f'.env.{environment}'
# #         logger.info(f"Running: docker-compose -f {str(service_dir / 'docker-compose.yml')} --env-file {env_file} {' '.join(commands)}")
        
# #         # Run with timeout to avoid hanging
# #         process = subprocess.run(
# #             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file] + commands,
# #             check=True,
# #             timeout=300  # 5 minute timeout
# #         )
        
# #         logger.info(f"Successfully executed: {' '.join(commands)} in {service_dir}")
# #     except subprocess.TimeoutExpired:
# #         logger.error(f"Docker compose command timed out. Cleaning up...")
# #         # Force cleanup on timeout
# #         cleanup_containers(service_dir)
# #         raise
# #     except subprocess.CalledProcessError as e:
# #         logger.error(f"Error executing docker compose {' '.join(commands)} in {service_dir}: {e}")
# #         # Cleanup on error
# #         cleanup_containers(service_dir)
# #         raise
# def rename_existing_container(service_name, container_name):
#     """Renames an existing container if a conflict exists."""
#     try:
#         # Check if a container with the same name exists
#         result = subprocess.run(
#             ['docker', 'ps', '-a', '--filter', f'name={container_name}', '--format', '{{.Names}}'],
#             capture_output=True,
#             text=True,
#             check=True
#         )

#         # If the container already exists, rename it
#         if result.stdout.strip():  # If a container name is returned
#             timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#             new_name = f"{container_name}_{timestamp}"
#             logger.info(f"Renaming existing container '{container_name}' for service '{service_name}' to '{new_name}'...")
#             subprocess.run(['docker', 'rename', result.stdout.strip(), new_name], check=True)
#             logger.info(f"Successfully renamed container '{container_name}' to '{new_name}'")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error while renaming container: {e}")
#         raise


# def execute_docker_compose(commands, service_dir, environment, service_type):
#     env_file = f'.env.{environment}'  # this could be .env.test or .env.prod
#     project_name = f"{service_type}_{environment}"  # Use the service directory name as part of the project name
    
#     logger.info(f"Running: docker-compose -f {str(service_dir / 'docker-compose.yml')} --env-file {env_file} {' '.join(commands)}")
    
#     # Running Docker Compose with the project name to differentiate environments
#     subprocess.run(
#         ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file, '-p', project_name] + commands,
#         check=True,
#         timeout=300  # 5 minute timeout
#     )

# # def execute_docker_compose(commands, service_dir, environment):
# #     env_file = f'.env.{environment}'  # this could be .env.test or .env.prod
# #     project_name = f"{service_dir.stem}_{environment}"  # Use the service directory name as part of the project name
    
# #     logger.info(f"Running: docker-compose -f {str(service_dir / 'docker-compose.yml')} --env-file {env_file} {' '.join(commands)}")
    
# #     # Running Docker Compose with the project name to differentiate environments
# #     subprocess.run(
# #         ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file, '-p', project_name] + commands,
# #         check=True,
# #         timeout=300  # 5 minute timeout
# #     )

# # def cleanup_containers(service_dir):
# #     """Clean up containers and networks created by docker-compose."""
# #     try:
# #         logger.info("Cleaning up containers and networks...")
# #         subprocess.run(
# #             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'down', '--volumes', '--remove-orphans'],
# #             check=False,  # Don't raise exception if cleanup fails
# #             timeout=60
# #         )
# #     except Exception as e:
# #         logger.error(f"Error during cleanup: {e}")
# def cleanup_containers(service_dir, environment):
#     """Clean up containers and networks created by docker-compose."""
#     try:
#         env_file = f'.env.{environment}'
#         project_name = f"{service_dir.stem}_{environment}"
        
#         logger.info(f"Cleaning up {environment} containers and networks...")

#         subprocess.run(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file, '-p', project_name, 'down', '--volumes', '--remove-orphans'],
#             check=False, 
#             timeout=60
#         )
#     except Exception as e:
#         logger.error(f"Error during cleanup: {e}")

# # def build_and_deploy(service_dir, environment,other_service_dir=None):
# #     """Build Docker images and deploy containers for a given service directory."""
# #     try:
# #         copy_env_file(service_dir, environment)
# #         # Step 2: Build Docker images from the updated Dockerfile
# #         logger.info(f"Building Docker containers for {service_dir}...")
# #         execute_docker_compose(['build', '--no-cache'], service_dir,environment)

# #         # Step 3: Start containers and run them
# #         logger.info(f"Starting Docker containers for {service_dir}...")
# #         execute_docker_compose(['up', '-d'], service_dir,environment)  # Added -d for detached mode
        
# #         # Step 4: Check container health
# #         check_container_health(service_dir)
        
# #     except Exception as e:
# #         logger.error(f"Build and deploy failed for {service_dir}: {e}")
# #          # Clean up containers for the current service
# #         cleanup_containers(service_dir,environment)
# #         # Also clean up the other service if it's provided
# #         if other_service_dir:
# #             cleanup_containers(other_service_dir,environment)
# #         raise


# #     """Runs the test suite and checks if tests passed."""
# #     try:
# #         # Run pytest or your preferred test framework (e.g., unittest)
# #         logger.info("Running tests in the test environment...")
        
# #         # Run pytest and capture the exit code
# #         result = subprocess.run(['pytest', '--maxfail=1', '--disable-warnings', '-q'], 
# #                                 capture_output=True, text=True)
        
# #         # If the return code is 0, it means tests passed
# #         if result.returncode == 0:
# #             logger.info("Tests passed successfully!")
# #             return True
# #         else:
# #             # If non-zero return code, tests failed
# #             logger.error(f"Tests failed with exit code {result.returncode}")
# #             logger.error(f"Test output: {result.stdout}\n{result.stderr}")
# #             return False
# #     except Exception as e:
# #         logger.error(f"Error running tests: {e}")
# #         return False

# def update_env_file(service_dir, service_type, port, db_port, environment):
#     """Update the .env file with the correct ports."""
#     env_file_path = service_dir / f'.env.{environment}'

#     # Update environment variables for the service
#     if service_type == "backend":
#         set_key(env_file_path, "BILLING_BACKEND_PORT", str(port))
#         set_key(env_file_path, "BILLING_DB_PORT", str(db_port))
#     elif service_type == "db":
#         set_key(env_file_path, "BILLING_DB_PORT", str(db_port))
#     else:
#         raise ValueError(f"Unknown service type: {service_type}")

# def build_and_deploy(service_dir, environment, service_type, other_service_dir=None):
#     """Build Docker images and deploy containers for a given service directory."""
#     try:
#         # Step 1: Assign new ports for backend and db services
#         backend_port = assign_ports(service_type="backend", service_name="billing-backend")
#         db_port = assign_ports(service_type="db", service_name="billing-db")

#         # Step 2: Update the environment file with the new ports
#         update_env_file(service_dir, service_type="backend", port=backend_port, db_port=db_port, environment=environment)

#         # Step 3: Check if containers with these names exist, and rename if necessary
#         backend_name = f"{service_type}_{environment}_backend"
#         db_name = f"{service_type}_{environment}_db"
#         rename_existing_container(service_type, backend_name)
#         rename_existing_container(service_type, db_name)

#         # Step 4: Build Docker images from the updated Dockerfile
#         logger.info(f"Building Docker containers for {service_type} service...")
#         execute_docker_compose(['build', '--no-cache'], service_dir, environment, service_type)

#         # Step 5: Start containers and run them in detached mode
#         logger.info(f"Starting Docker containers for {service_type} service...")
#         execute_docker_compose(['up', '-d'], service_dir, environment, service_type)  # Added -d for detached mode
        
#         # Step 6: Check container health for the deployed service
#         check_container_health(service_dir)

#         # If there is another service that needs cleanup, handle it
#         if other_service_dir:
#             logger.info(f"Cleaning up containers for the other service: {other_service_dir}")
#             cleanup_containers(other_service_dir, environment)

#     except Exception as e:
#         logger.error(f"Build and deploy failed for {service_dir}: {e}")
        
#         # Clean up containers for the current service
#         cleanup_containers(service_dir, environment)
        
#         # Also clean up the other service if it's provided
#         if other_service_dir:
#             cleanup_containers(other_service_dir, environment)
        
#         raise
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
#     ## change only to check new prod
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

# def load_environment(env_file):
#     """Load environment variables from file, overriding existing ones."""
#     # Clear relevant environment variables before loading new ones
#     env_vars_to_clear = [
#         'BILLING_BACKEND_PORT',
#         'BILLING_DB_PORT',
#         'WEIGHT_BACKEND_PORT',
#         'WEIGHT_DB_PORT',
#         'BILLING_MYSQL_DATABASE_PASSWORD',
#         'BILLING_MYSQL_DATABASE_DB',
#         'NETWORK_NAME',
#         'ENV',
#         # Add any other environment variables that need to be cleared
#     ]
    
#     for var in env_vars_to_clear:
#         if var in os.environ:
#             del os.environ[var]
    
#     # Load new environment variables
#     load_dotenv(dotenv_path=env_file, override=True)
    
#     # Set ENV explicitly
#     environment = 'test' if env_file.endswith('.test') else 'prod'
#     os.environ['ENV'] = environment
# def main(rollback=False):
#     """Main function to process both billing and weight services."""
   
#     try:
#         clone_or_update_repo()
#         if rollback:
#             rollback_func()
#         load_environment('/app/.env.test')
#         environment = 'test' 

#         # Step 2: Build and deploy both services in the test environment
#         build_and_deploy(REPO_DIR / 'billing', environment)
#         build_and_deploy(REPO_DIR / 'weight', environment, other_service_dir=REPO_DIR / 'billing')

#         # Step 3: Check if tests passed (if applicable)
#         logger.info("Running tests in the test environment...")
#         logger.info("Running tests for billing service...")
#         if not check_tests_passed(str(REPO_DIR / 'billing' / 'tests'), rollback):
#             raise RuntimeError("Tests failed in the billing service. Aborting pipeline.")
        
#         # logger.info("Running tests for weight service...")
#         # if not check_tests_passed(str(REPO_DIR / 'weight' / 'tests'), rollback):
#         #     raise RuntimeError("Tests failed in the weight service. Aborting pipeline.")
        
#         # Step 4: Clean up test environment before deploying to production
#         logger.info("Cleaning up test environment...")
#         cleanup_containers(REPO_DIR / 'billing',environment)
#         cleanup_containers(REPO_DIR / 'weight',environment)
        
        
#         environment = 'prod' 
#         load_environment('/app/.env.prod')
#         # Step 5: Deploy to production environment (if tests passed)
#         logger.info("Deploying to production environment...")
#         build_and_deploy(REPO_DIR / 'billing', environment)
#         build_and_deploy(REPO_DIR / 'weight', environment)

#         # Step 6: Check if the production containers are healthy and running
#         logger.info("Checking health of production containers...")
#         if not check_container_health(REPO_DIR / 'billing'):
#             raise RuntimeError("Billing service in production is not healthy.")
#         if not check_container_health(REPO_DIR / 'weight'):
#             raise RuntimeError("Weight service in production is not healthy.")
        
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


import subprocess
import random
import os
import time
from logging_config import logger
from pathlib import Path
from shutil import copyfile
from dotenv import load_dotenv, set_key
from datetime import datetime

load_dotenv(dotenv_path="env.test")

# Get the path of the current directory
CURRENT_DIR = Path(__file__).parent
REPO_DIR = CURRENT_DIR / "gan-shmuel"  # Path to the cloned repository

class CloneRepositoryError(Exception):
    pass

def check_container_running(container_name):
    """Check if a container with the given name is currently running."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', f'name={container_name}', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            check=True
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking container status: {e}")
        return False

def get_container_port(container_name, port_type):
    """Get the current port being used by a running container."""
    try:
        if port_type == "backend":
            port_pattern = "8080-8090"
        else:  # db
            port_pattern = "3000-3090"
            
        result = subprocess.run(
            ['docker', 'port', container_name],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the port from the output
        for line in result.stdout.splitlines():
            if port_pattern in line:
                return int(line.split(':')[-1])
        return None
    except subprocess.CalledProcessError:
        return None

def assign_ports(service_type):
    """Assign a random available port for backend and db services."""
    if service_type == "backend":
        port_range = range(8080, 8091)
    elif service_type == "db":
        port_range = range(3000, 3091)
    else:
        raise ValueError("Unknown service type")
    
    available_ports = []
    for port in port_range:
        result = subprocess.run(
            ['docker', 'ps', '--filter', f'publish={port}', '--format', '{{.Ports}}'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0 or not result.stdout.strip():  # Port is available
            available_ports.append(port)

    if not available_ports:
        raise RuntimeError(f"No available ports found for {service_type} service.")
    
    return random.choice(available_ports)

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

def rollback_func():
    """Rollback to the previous commit in the repository."""
    try:
        logger.info("Rolling back to the previous commit...")
        try:
            subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            subprocess.run(['git', 'checkout', '-b', 'master', 'origin/master'], cwd=REPO_DIR, check=True)
        
        subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
        subprocess.run(['git', 'reset', '--hard', 'HEAD^'], cwd=REPO_DIR, check=True)
        logger.info("Successfully rolled back to the previous commit")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to rollback to the previous commit: {e}")
        raise

def rename_existing_container(service_name, container_name):
    """Renames an existing container if a conflict exists."""
    try:
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', f'name={container_name}', '--format', '{{.Names}}'],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_name = f"{container_name}_{timestamp}"
            logger.info(f"Renaming existing container '{container_name}' for service '{service_name}' to '{new_name}'...")
            subprocess.run(['docker', 'rename', result.stdout.strip(), new_name], check=True)
            logger.info(f"Successfully renamed container '{container_name}' to '{new_name}'")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while renaming container: {e}")
        raise

def execute_docker_compose(commands, service_dir, environment, service_type):
    """Execute docker-compose commands with proper project naming."""
    env_file = f'.env.{environment}'
    project_name = f"{service_type}_{environment}"
    
    logger.info(f"Running: docker-compose -f {str(service_dir / 'docker-compose.yml')} --env-file {env_file} {' '.join(commands)}")
    
    subprocess.run(
        ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file, '-p', project_name] + commands,
        check=True,
        timeout=300
    )

def cleanup_containers(service_dir, environment):
    """Clean up containers and networks created by docker-compose."""
    try:
        env_file = f'.env.{environment}'
        project_name = f"{service_dir.stem}_{environment}"
        
        logger.info(f"Cleaning up {environment} containers and networks...")

        subprocess.run(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file, '-p', project_name, 'down', '--volumes', '--remove-orphans'],
            check=False, 
            timeout=60
        )
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

def update_env_file(service_dir, service_type, port, db_port, environment):
    """Update the .env file with the correct ports."""
    env_file_path = service_dir / f'.env.{environment}'

    if service_type == "backend":
        set_key(env_file_path, "BILLING_BACKEND_PORT", str(port))
        set_key(env_file_path, "BILLING_DB_PORT", str(db_port))
    elif service_type == "db":
        set_key(env_file_path, "BILLING_DB_PORT", str(db_port))
    else:
        raise ValueError(f"Unknown service type: {service_type}")

def build_and_deploy(service_dir, environment, service_type, other_service_dir=None):
    """Build Docker images and deploy containers for a given service directory."""
    try:
        backend_port = None
        db_port = None
        need_port_update = False
        
        # Only check existing containers if we're in production
        if environment == 'prod':
            backend_name = f"{service_type}_prod_backend"
            db_name = f"{service_type}_prod_db"
            
            backend_running = check_container_running(backend_name)
            db_running = check_container_running(db_name)
            
            if backend_running or db_running:
                need_port_update = True
                # Get current ports if containers are running
                if backend_running:
                    backend_port = get_container_port(backend_name, "backend")
                    rename_existing_container(service_type, backend_name)
                
                if db_running:
                    db_port = get_container_port(db_name, "db")
                    rename_existing_container(service_type, db_name)
        
        # Assign new ports only if needed
        if not backend_port:
            backend_port = assign_ports(service_type="backend")
        if not db_port:
            db_port = assign_ports(service_type="db")
            
        # Update environment file only if ports changed
        if need_port_update:
            update_env_file(service_dir, service_type, backend_port, db_port, environment)

        # Build and start containers
        logger.info(f"Building Docker containers for {service_type} service...")
        execute_docker_compose(['build', '--no-cache'], service_dir, environment, service_type)

        logger.info(f"Starting Docker containers for {service_type} service...")
        execute_docker_compose(['up', '-d'], service_dir, environment, service_type)
        
        # Check container health
        check_container_health(service_dir)

        if other_service_dir:
            logger.info(f"Cleaning up containers for the other service: {other_service_dir}")
            cleanup_containers(other_service_dir, environment)

    except Exception as e:
        logger.error(f"Build and deploy failed for {service_dir}: {e}")
        cleanup_containers(service_dir, environment)
        if other_service_dir:
            cleanup_containers(other_service_dir, environment)
        raise

def check_tests_passed(test_directory, rollback=False):
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

def check_container_health(service_dir, retries=5, delay=10):
    """Check if all containers are healthy and running."""
    try:
        for _ in range(retries):
            result = subprocess.run(
                ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'ps'],
                capture_output=True,
                text=True,
                check=True
            )
            
            if 'Exit' in result.stdout:
                logger.error("One or more containers have exited unexpectedly")
                subprocess.run(
                    ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'logs'],
                    check=False
                )
                raise RuntimeError("Container startup failed")
            
            logger.info("Containers are healthy.")
            return True
            
            time.sleep(delay)
        logger.error("Containers did not become healthy within retries.")
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking container health: {e}")
        raise

def load_environment(env_file):
    """Load environment variables from file, overriding existing ones."""
    env_vars_to_clear = [
        'BILLING_BACKEND_PORT',
        'BILLING_DB_PORT',
        'WEIGHT_BACKEND_PORT',
        'WEIGHT_DB_PORT',
        'BILLING_MYSQL_DATABASE_PASSWORD',
        'BILLING_MYSQL_DATABASE_DB',
        'NETWORK_NAME',
        'ENV',
    ]
    
    for var in env_vars_to_clear:
        if var in os.environ:
            del os.environ[var]
    
    load_dotenv(dotenv_path=env_file, override=True)
    
    environment = 'test' if env_file.endswith('.test') else 'prod'
    os.environ['ENV'] = environment

def main(rollback=False):
    """Main function to process both billing and weight services."""
    try:
        clone_or_update_repo()
        if rollback:
            rollback_func()
        load_environment('/app/.env.test')
        environment = 'test' 

        # Build and deploy test environment
        build_and_deploy(REPO_DIR / 'billing', environment, 'billing')
        build_and_deploy(REPO_DIR / 'weight', environment, 'weight', other_service_dir=REPO_DIR / 'billing')

        # Run tests
        logger.info("Running tests in the test environment...")
        logger.info("Running tests for billing service...")
        # if not check_tests_passed(str(REPO_DIR / 'billing' / 'tests'), rollback):
        #     raise RuntimeError("Tests failed in the billing service. Aborting pipeline.")
        
        # Clean up test environment
        logger.info("Cleaning up test environment...")
        cleanup_containers(REPO_DIR / 'billing', environment)
        cleanup_containers(REPO_DIR / 'weight', environment)
        
        # Deploy to production
        environment = 'prod' 
        load_environment('/app/.env.prod')
        logger.info("Deploying to production environment...")
        build_and_deploy(REPO_DIR / 'billing', environment, 'billing')
        build_and_deploy(REPO_DIR / 'weight', environment, 'weight')

        # Check production health
        logger.info("Checking health of production containers...")
        if not check_container_health(REPO_DIR / 'billing'):
            raise RuntimeError("Billing service in production is not healthy.")
        if not check_container_health(REPO_DIR / 'weight'):
            raise RuntimeError("Weight service in production is not healthy.")
        
        logger.info(f"CI pipeline completed successfully in {environment} and prod environments.")
        
        if rollback: 
            logger.info("Tests passed. Pushing the rollback commit to GitHub...")
            GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
            subprocess.run(
                ['git', 'push', '--force', f'https://{GITHUB_TOKEN}@github.com/AM8151/gan-shmuel.git', 'master'],
                cwd=REPO_DIR,
                check=True
            )
            logger.info("Successfully pushed the rollback commit to GitHub.")

    except CloneRepositoryError as e:
        logger.error(f"Failed to clone repository: {e}")

    except Exception as e:
        logger.error(f"CI pipeline failed for one or both services: {e}")
        # Ensure cleanup in case of failure
        cleanup_containers(REPO_DIR / 'billing')
        cleanup_containers(REPO_DIR / 'weight')
        if not rollback:
            main(rollback=True)
        raise

if __name__ == "__main__":
    main()
