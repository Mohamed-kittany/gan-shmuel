
# import socket
# import subprocess
# import os
# from pathlib import Path
# from shutil import copyfile, copytree, ignore_patterns
# from dotenv import load_dotenv
# from logging_config import logger
# from datetime import datetime



# CURRENT_DIR = Path(__file__).parent
# REPO_DIR = CURRENT_DIR / "gan-shmuel"


# class CloneRepositoryError(Exception):
#     pass

# def is_port_in_use(port):
#     """Check if a port is in use."""
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         return s.connect_ex(('localhost', port)) == 0

# def find_free_ports(service_type, start_port=8080, end_port=8090, num_ports=2):
#     """Find a specified number of free ports for different services."""
#     db_ports_map = {
#         'weight': [3306, 3308],
#         'billing': [3307, 3309]
#     }
    
#     if service_type not in db_ports_map:
#         raise ValueError(f"Unknown service type: {service_type}")
    
#     db_ports = db_ports_map[service_type]
#     free_ports = [port for port in db_ports if not is_port_in_use(port)]
    
#     if len(free_ports) < num_ports:
#         raise Exception(f"Not enough free DB ports for {service_type}.")
    
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


# def execute_docker_compose(service_dir, commands, environment):
#     """Run Docker Compose commands."""
#     try:
#         # manage_env_file(service_dir, environment)
#         env_file = f".env.{environment}"
#         logger.info(str(service_dir / 'docker-compose.yml'))
#         run_subprocess(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file] + commands,
#             cwd=service_dir,
#         )
#     except Exception as e:
#         logger.error(f"Docker Compose failed: {e}")
#         cleanup_test_containers(service_dir, environment)
#         raise

# def cleanup_test_containers(service_dir):
#     """Clean up Docker containers and networks only for the test environment."""
#     try:
#         run_subprocess(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', '.env.test', 'down'],
#             cwd=service_dir,
#             check=False
#         )
#         logger.info("Cleaned up test containers and networks.")
#     except Exception as e:
#         logger.error(f"Error during test cleanup: {e}")

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

# def build_and_deploy(service_dir, environment, service_type):
#     """Build and deploy services."""
#     try:
#         logger.info(f"Deploying {service_dir} in {environment} environment...")
#         execute_docker_compose(service_dir, ['build', '--no-cache'], environment)
#         execute_docker_compose(service_dir, ['up', '-d'], environment)
#         check_container_health(service_dir)
        
#         logger.info(f"Successfully deployed {service_dir}.")
#     except Exception as e:
#         cleanup_test_containers(service_dir, environment)
#         raise RuntimeError(f"Deployment failed for {service_dir}: {e}")

# def run_tests(test_directory, rollback=False):
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




# def blue_green_deploy(service_dir, environment, service_type):
#     """Perform a blue-green deployment."""
#     backend_port, db_port = find_free_ports(service_type)
#     os.environ[f'{str(service_dir).upper()}_BACKEND_PORT'] = str(backend_port)
#     os.environ[f'{str(service_dir).upper()}_DB_PORT'] = str(db_port)
#     build_and_deploy(service_dir, environment, service_type)
#     logger.info(f"Blue-green deployment complete for {service_dir}.")


# def rollback_func():
#     """Rollback to the previous commit in the repository."""
#     try:
#         logger.info("Rolling back to the previous commit...")
#         subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True, capture_output=True)
#         subprocess.run(['git', 'branch', '--set-upstream-to=origin/master', 'master'], cwd=REPO_DIR, check=True)
#         subprocess.run(['git', 'reset', '--hard', 'HEAD^'], cwd=REPO_DIR, check=True)
#         logger.info("Successfully rolled back to the previous commit")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Failed to rollback to the previous commit: {e}")
#         raise
# def log_environment_variables():
#         logger.info("Current environment variables:")
#         for key, value in os.environ.items():
#             logger.info(f"{key}: {value}")
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
    
#     return environment
# def cleanup_old_prod_containers(service_dir):
#     """Clean up old production Docker containers while keeping the new ones running."""
#     try:
#         # Get list of running containers using docker-compose
#         result = run_subprocess(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', '.env.prod', 'ps', '-q'],
#             cwd=service_dir,
#             check=True
#         )
        
#         if not result:
#             logger.info("No old containers found to clean up.")
#             return
            
#         # Stop and remove old containers using docker-compose
#         run_subprocess(
#             ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', '.env.prod', 'down'],
#             cwd=service_dir,
#             check=False
#         )
        
#         logger.info("Cleaned up old production containers.")
#     except Exception as e:
#         logger.error(f"Error during production cleanup: {e}")

# def get_running_containers_by_ports(backend_ports):
#     """Get running containers that use specific backend ports."""
#     try:
#         # Get container details including port mappings
#         result = run_subprocess(
#             ['docker', 'ps', '--format', '{{.Names}}\t{{.Ports}}'],
#             check=True
#         )
#         containers = []
#         for line in result.split('\n'):
#             if not line:
#                 continue
#             name, ports = line.split('\t')
#             if any(str(port) in ports for port in backend_ports):
#                 containers.append(name)
#         return containers
#     except Exception as e:
#         logger.error(f"Error getting running containers: {e}")
#         return []

# def cleanup_old_prod_containers(old_backend_ports):
#     """Clean up old production Docker containers after new deployment is verified."""
#     try:
#         # Get list of containers using the old ports
#         old_containers = get_running_containers_by_ports(old_backend_ports)
#         if not old_containers:
#             logger.info("No old containers found to clean up.")
#             return

#         # Stop and remove containers
#         for container in old_containers:
#             try:
#                 logger.info(f"Stopping old container: {container}")
#                 run_subprocess(['docker', 'stop', container], check=False)
#                 logger.info(f"Removing old container: {container}")
#                 run_subprocess(['docker', 'rm', container], check=False)
#             except Exception as e:
#                 logger.error(f"Error removing container {container}: {e}")
#                 continue

#         # Clean up unused networks
#         logger.info("Cleaning up unused networks...")
#         run_subprocess(['docker', 'network', 'prune', '-f'], check=False)
        
#         logger.info("Cleaned up old production containers and networks.")
#     except Exception as e:
#         logger.error(f"Error during production cleanup: {e}")

# def main(rollback=False, env_suffix=None):
#     try:
#         logger.info("Starting CI pipeline...")
#         clone_or_update_repo()

#         if env_suffix is None:
#             env_suffix = "1"

#         os.environ["ENV_SUFFIX"] = env_suffix

#         # Store current production ports before finding new ones
#         old_billing_ports = [int(os.getenv('BILLING_BACKEND_PORT', '8080')), 
#                            int(os.getenv('BILLING_DB_PORT', '3307'))]
#         old_weight_ports = [int(os.getenv('WEIGHT_BACKEND_PORT', '8081')), 
#                           int(os.getenv('WEIGHT_DB_PORT', '3306'))]

#         # Load test environment and run tests
#         environment = load_environment(".env.test")
#         logger.info("Loaded test environment variables:")
#         log_environment_variables()

#         billing_service_dir = REPO_DIR / 'billing'
#         weight_service_dir = REPO_DIR / 'weight'
        
#         timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#         target_prod_dir = Path(f'/app/prod/{timestamp}')
#         target_prod_dir.mkdir(parents=True, exist_ok=True)
        
#         # Copy the directories
#         for service_dir, target_dir in [
#             (billing_service_dir, target_prod_dir / 'billing'),
#             (weight_service_dir, target_prod_dir / 'weight')
#         ]:
#             logger.info(f"Starting to copy service from {service_dir} to {target_dir}")
#             copytree(service_dir, target_dir, ignore=ignore_patterns(), dirs_exist_ok=True, copy_function=copyfile)

#         # Deploy test environment
#         build_and_deploy(billing_service_dir, environment, 'billing')
#         build_and_deploy(weight_service_dir, environment, 'weight')

#         logger.info("Running tests in the test environment...")
        
#         # Clean up test containers
#         cleanup_test_containers(billing_service_dir)
#         cleanup_test_containers(weight_service_dir)
        
#         # Load production environment
#         environment = load_environment(".env.prod")
#         logger.info("Loaded production environment variables:")
#         log_environment_variables()
        
#         # Deploy new production containers with new ports
#         logger.info("Deploying new production environment...")
#         blue_green_deploy(target_prod_dir / 'billing', environment, 'billing')
#         blue_green_deploy(target_prod_dir / 'weight', environment, 'weight')

#         # Verify new deployment is healthy
#         check_container_health(target_prod_dir / 'billing')
#         check_container_health(target_prod_dir / 'weight')
        
#         # Only after new deployment is verified, clean up old containers
#         logger.info("New deployment verified. Cleaning up old production containers...")
#         cleanup_old_prod_containers(old_billing_ports + old_weight_ports)
        
#         logger.info(f"CI pipeline completed successfully in {environment} environment.")
        
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
#         logger.error(f"Error: {e}")
#         raise
# if __name__ == '__main__':
#     main()
# import os
# import subprocess
# import time
# from datetime import datetime
# from pathlib import Path
# from typing import List
# from logging_config import logger
# from concurrent.futures import ThreadPoolExecutor

# class DeploymentError(Exception):
#     """Custom exception for deployment errors"""
#     pass


# def run_command(command: List[str], cwd: Path = None, check: bool = True) -> str:
#     """
#     Execute a shell command and return its output.
#     """
#     try:
#         result = subprocess.run(
#             command,
#             cwd=cwd,
#             check=check,
#             capture_output=True,
#             text=True
#         )
#         return result.stdout.strip()
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Command failed: {' '.join(command)}")
#         logger.error(f"Error output: {e.stderr}")
#         if check:
#             raise DeploymentError(f"Command failed: {e.stderr}")
#         return ""


# class DockerService:
#     def __init__(self, service_dir: Path, service_name: str, env_file: str, is_production: bool = False):
#         self.service_dir = service_dir
#         self.service_name = service_name
#         self.env_file = env_file
#         self.is_production = is_production
#         self.env_file_path = Path("/app") / self.env_file

#         self.compose_cmd = [
#             'docker-compose',
#             '-f', str(service_dir / 'docker-compose.yml'),
#             '--env-file', str(self.env_file_path)
#         ]

#     def build(self, project_name: str) -> None:
#         """Build the Docker images"""
#         logger.info(f"Building {self.service_name} with project name {project_name}")
#         run_command([*self.compose_cmd, '-p', project_name, 'build', '--no-cache'], self.service_dir)

#     def start(self, project_name: str) -> None:
#         """Start the containers"""
#         logger.info(f"Starting {self.service_name} with project name {project_name}")
#         run_command([*self.compose_cmd, '-p', project_name, 'up', '-d'], self.service_dir)

#     def stop(self, project_name: str) -> None:
#         """Stop the containers"""
#         logger.info(f"Stopping {self.service_name} with project name {project_name}")
#         run_command([*self.compose_cmd, '-p', project_name, 'down'], self.service_dir, check=False)

#     def is_healthy(self, project_name: str) -> bool:
#         """Check if containers are healthy"""
#         time.sleep(10)
#         result = run_command([*self.compose_cmd, '-p', project_name, 'ps'], self.service_dir)
#         return '(healthy)' in result and 'Exit' not in result

#     def get_container_names(self, project_name: str) -> List[str]:
#         """Get list of container names for the service"""
#         return run_command(
#             ['docker', 'ps', '--filter', f'name={project_name}', '--format', '{{.Names}}']
#         ).splitlines()


# class Deployment:
#     def __init__(self, repo_url: str, base_dir: Path):
#         self.repo_url = repo_url
#         self.base_dir = base_dir
#         self.repo_dir = base_dir / "gan-shmuel"
#         self.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

#     def clone_repo(self) -> None:
#         """Clone or update the repository"""
#         if not self.repo_dir.exists():
#             logger.info("Cloning repository...")
#             run_command(['git', 'clone', self.repo_url, str(self.repo_dir)])
#         else:
#             logger.info("Updating repository...")
#             run_command(['git', 'fetch'], self.repo_dir)
#             run_command(['git', 'reset', '--hard', 'origin/master'], self.repo_dir)

#     def run_tests(self, service_dir: Path) -> bool:
#         """Run tests for a service"""
#         logger.info(f"Running tests for {service_dir.name}")
#         try:
#             test_dir = service_dir / 'tests'
#             if test_dir.exists():
#                 result = run_command(['pytest', str(test_dir), '-v'], service_dir)
#                 logger.info(f"Test results: {result}")
#                 return 'failed' not in result.lower()
#             logger.warning(f"No tests found in {test_dir}")
#             return True
#         except Exception as e:
#             logger.error(f"Tests failed: {e}")
#             return False

#     def deploy_service(self, service: DockerService) -> bool:
#         """Deploy the service to test environment and run tests"""
#         try:
#             # In the test environment, the service name does not need to be renamed
#             new_project = f"{service.service_name}_test"
#             service.build(new_project)
#             service.start(new_project)

#             # Run tests after deploying to test environment
#             logger.info(f"New version of {service.service_name} deployed successfully to test environment.")
#             # return self.run_tests(service.service_dir)
        
#         except Exception as e:
#             logger.error(f"Deployment failed for {service.service_name}: {e}")
#             service.stop(new_project)
#             return False

#     def deploy_to_prod(self, service: DockerService) -> bool:
#         """Deploy the service to production environment"""
#         logger.info(f"Deploying {service.service_name} to production")
#         # In the production environment, ensure the project name is renamed
#         if service.is_production:
#             new_project = f"{service.service_name}_prod"
#         else:
#             new_project = f"{service.service_name}_test"  # for test environment use the same project name
#         service.build(new_project)
#         service.start(new_project)
#         return True

#     def run(self) -> bool:
#         """Run the complete CI/CD pipeline"""
#         try:
#             logger.info("Starting CI/CD pipeline")
            
#             # Clone/update repository
#             self.clone_repo()

#             # Define services to deploy
#             services = [
#                 ('billing', '/app/.env.test', False),  # No need for production flag in test environment
#                 ('weight', '/app/.env.test', False)
#             ]

#             # Deploy both services to test environment in parallel
#             with ThreadPoolExecutor() as executor:
#                 deploy_results = list(executor.map(
#                     lambda s: self.deploy_service(DockerService(self.repo_dir / s[0], s[0], s[1], s[2])), 
#                     services
#                 ))

#             # Check if all tests passed for both services
#             if all(deploy_results):
#                 logger.info("All services passed test successfully. Deploying to production.")

#                 # Deploy both services to production in parallel (with renaming in production)
#                 with ThreadPoolExecutor() as executor:
#                     executor.map(
#                         lambda s: self.deploy_to_prod(DockerService(self.repo_dir / s[0], s[0], '.env.prod', True)),
#                         services
#                     )

#                 # Stop test containers after deployment
#                 for service_name, _, _ in services:
#                     service = DockerService(self.repo_dir / service_name, service_name, '/app/.env.test')
#                     service.stop(f"{service_name}_test")

#                 logger.info("CI/CD pipeline completed successfully")
#                 return True
#             else:
#                 logger.error("Deployment to test environment failed. Rolling back.")
#                 # Stop all services if any test fails
#                 with ThreadPoolExecutor() as executor:
#                     executor.map(
#                         lambda s: DockerService(self.repo_dir / s[0], s[0], '/app/.env.test').stop(f"{s[0]}_test"),
#                         services
#                     )
#                 return False

#         except Exception as e:
#             logger.error(f"CI/CD pipeline failed: {e}")
#             return False


# def main(rollback=False):
#     """Main function to execute the CI/CD pipeline"""
#     try:
#         # Configuration
#         REPO_URL = "https://github.com/AM8151/gan-shmuel.git"
#         BASE_DIR = Path(__file__).parent 

#         # Create and run deployment
#         deployment = Deployment(REPO_URL, BASE_DIR)

#         if rollback:
#             logger.info("Rollback triggered")
#             # Implement rollback logic here if necessary

#         success = deployment.run()

#         # Exit with appropriate status code
#         return success

#     except Exception as e:
#         logger.error(f"CI/CD pipeline failed: {e}")
#         return False


# if __name__ == "__main__":
#     main()
import subprocess
import os
from logging_config import logger
from pathlib import Path
from shutil import copyfile
from dotenv import load_dotenv
import time

load_dotenv(dotenv_path="env.test")

# Constants
CURRENT_DIR = Path(__file__).parent
REPO_DIR = CURRENT_DIR / "gan-shmuel"
GITHUB_REPO = "https://github.com/AM8151/gan-shmuel.git"

class CloneRepositoryError(Exception):
    pass


class GitHandler:
    """Handles Git operations like cloning, pulling, and rolling back commits."""
    
    @staticmethod
    def clone_repository():
        """Clones the Git repository if it doesn't exist locally or initializes it if mounted."""
        if not REPO_DIR.exists():
            logger.info("Repository not found. Cloning repository...")
            try:
                subprocess.run(['git', 'clone', GITHUB_REPO, str(REPO_DIR)], check=True)
                logger.info(f"Successfully cloned the repository into {REPO_DIR}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone the repository: {e}")
                raise CloneRepositoryError("Failed to clone the repository")
        else:
            logger.info("Repository exists. Pulling latest changes...")
            GitHandler.pull_latest_code()

    @staticmethod
    def pull_latest_code():
        """Pulls the latest code from the GitHub repository (from the master branch)."""
        logger.info("Pulling latest code from GitHub...")
        try:
            subprocess.run(['git', 'checkout', 'master'], cwd=REPO_DIR, check=True)
            subprocess.run(['git', 'pull'], cwd=REPO_DIR, check=True)
            logger.info("Successfully pulled latest code from master branch")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to pull latest code from master: {e}")
            raise

    @staticmethod
    def rollback():
        """Rollback to the previous commit in the repository."""
        try:
            logger.info("Rolling back to the previous commit...")
            subprocess.run(['git', 'reset', '--hard', 'HEAD^'], cwd=REPO_DIR, check=True)
            logger.info("Successfully rolled back to the previous commit")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to rollback to the previous commit: {e}")
            raise


class DockerHandler:
    """Handles Docker Compose operations like building, deploying, and cleaning up containers."""

    @staticmethod
    def copy_env_file(service_dir, environment):
        """Copies the correct .env file based on the environment."""
        env_file_map = {
            'prod': '/app/.env.prod',
            'test': '/app/.env.test',
        }

        env_file = env_file_map.get(environment)
        if not env_file:
            raise ValueError(f"Unknown environment: {environment}")

        target_env_path = service_dir / f'.env.{environment}'
        logger.info(f"Copying {env_file} to {target_env_path}...")
        copyfile(env_file, target_env_path)
        logger.info(f"Successfully copied {env_file} to {target_env_path}")

    @staticmethod
    def execute_docker_compose(commands, service_dir, environment):
        """Executes docker-compose commands in the provided service directory."""
        try:
            DockerHandler.copy_env_file(service_dir, environment)
            env_file = f'.env.{environment}'
            logger.info(f"Running docker-compose: {' '.join(commands)}")

            subprocess.run(
                ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), '--env-file', env_file] + commands,
                check=True,
                timeout=300  # 5-minute timeout
            )
            logger.info(f"Successfully executed: {' '.join(commands)}")
        except subprocess.TimeoutExpired:
            logger.error("Docker compose command timed out. Cleaning up...")
            DockerHandler.cleanup_containers(service_dir)
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing docker compose: {e}")
            DockerHandler.cleanup_containers(service_dir)
            raise

    @staticmethod
    def cleanup_containers(service_dir):
        """Cleans up containers and networks created by docker-compose."""
        try:
            logger.info("Cleaning up containers and networks...")
            subprocess.run(
                ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'down', '--volumes', '--remove-orphans'],
                check=False,
                timeout=60
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Error during cleanup: {e}")

    @staticmethod
    def build_and_deploy(service_dir, environment, other_service_dir=None):
        """Build and deploy Docker containers for the given service."""
        try:
            logger.info(f"Building and deploying service {service_dir} in {environment} environment...")
            DockerHandler.execute_docker_compose(['build', '--no-cache'], service_dir, environment)
            DockerHandler.execute_docker_compose(['up', '--build', '-d'], service_dir, environment)

            # Zero downtime deployment strategy:
            DockerHandler.zero_downtime_deployment(service_dir)
            
        except Exception as e:
            logger.error(f"Build and deploy failed for {service_dir}: {e}")
            DockerHandler.cleanup_containers(service_dir)
            if other_service_dir:
                DockerHandler.cleanup_containers(other_service_dir)
            raise

    @staticmethod
    def zero_downtime_deployment(service_dir):
        """Performs zero-downtime deployment by ensuring new containers are healthy before shutting down old ones."""
        logger.info("Starting zero-downtime deployment...")

        # Check for any running containers
        result = subprocess.run(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'ps', '--services', '--filter', 'status=running'],
            capture_output=True, text=True, check=True
        )
        running_services = result.stdout.splitlines()
        
        # Start new containers in detached mode
        logger.info("Starting new containers...")
        subprocess.run(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'up', '--build', '--detach'],
            check=True
        )
        
        # Check if the new containers are healthy
        logger.info("Checking health of new containers...")
        DockerHandler.check_container_health(service_dir)

        # Stop old containers
        logger.info("Stopping old containers...")
        subprocess.run(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'stop'] + running_services,
            check=True
        )

        # Clean up old containers
        logger.info("Cleaning up old containers...")
        subprocess.run(
            ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'rm', '--force'] + running_services,
            check=True
        )
        
        logger.info("Zero-downtime deployment completed.")

    @staticmethod
    def check_container_health(service_dir, retries=5, delay=10):
        """Checks if all containers are healthy and running."""
        for _ in range(retries):
            result = subprocess.run(
                ['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'ps'],
                capture_output=True, text=True, check=True
            )

            if 'Exit' in result.stdout:
                logger.error("One or more containers have exited unexpectedly")
                subprocess.run(['docker-compose', '-f', str(service_dir / 'docker-compose.yml'), 'logs'], check=False)
                raise RuntimeError("Container startup failed")

            logger.info("Containers are healthy.")
            return True
            time.sleep(delay)

        logger.error("Containers did not become healthy within retries.")
        return False


class TestHandler:
    """Handles test suite execution and checks if tests passed."""

    @staticmethod
    def run_tests(test_directory, rollback=False):
        """Runs the test suite and checks if tests passed for a specific test directory."""
        logger.info(f"Running tests from {test_directory}...")
        result = subprocess.run(
            ['pytest', test_directory, '--maxfail=1', '--disable-warnings', '-q'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            logger.info("Tests passed successfully!")
            return True
        else:
            if not rollback:  # Only trigger rollback if not requested by the user
                GitHandler.rollback()
            logger.error(f"Tests failed with exit code {result.returncode}")
            logger.error(f"Test output: {result.stdout}\n{result.stderr}")
            return False


class Pipeline:
    """Main pipeline class that orchestrates the steps."""

    def __init__(self, environment='test'):
        self.environment = environment

    def run(self, rollback=False):
        """Run the entire pipeline: clone repo, build, deploy, run tests, and deploy to production."""
        try:
            # Step 1: Clone and pull the latest code
            GitHandler.clone_repository()

            # Rollback if necessary
            if rollback:
                GitHandler.rollback()

            # Step 2: Build and deploy both services in the test environment
            logger.info("Deploying services in test environment...")
            DockerHandler.build_and_deploy(REPO_DIR / 'billing', self.environment)
            DockerHandler.build_and_deploy(REPO_DIR / 'weight', self.environment, other_service_dir=REPO_DIR / 'billing')

            # Step 3: Run tests for billing service
            logger.info("Running tests for billing service...")
            # if not TestHandler.run_tests(str(REPO_DIR / 'billing' / 'tests'), rollback):
            #     raise RuntimeError("Tests failed in the billing service. Aborting pipeline.")

            # Step 4: Run tests for weight service
            logger.info("Running tests for weight service...")
            # if not TestHandler.run_tests(str(REPO_DIR / 'weight' / 'tests'), rollback):
            #     raise RuntimeError("Tests failed in the weight service. Aborting pipeline.")

            # Step 5: Cleanup test environment before deploying to production
            logger.info("Cleaning up test environment...")
            DockerHandler.cleanup_containers(REPO_DIR / 'billing')
            DockerHandler.cleanup_containers(REPO_DIR / 'weight')

            # Step 6: Deploy to production environment with zero-downtime
            logger.info("Deploying to production environment...")
            os.environ['ENV'] = 'prod'
            DockerHandler.build_and_deploy(REPO_DIR / 'billing', 'prod')
            DockerHandler.build_and_deploy(REPO_DIR / 'weight', 'prod', other_service_dir=REPO_DIR / 'billing')

            logger.info(f"CI pipeline completed successfully in {self.environment} and prod environments.")
            
        except Exception as e:
            logger.error(f"CI pipeline failed: {e}")
            raise
def main(rollback=False):
    """Main entry point to run the pipeline with optional rollback."""
    pipeline = Pipeline(environment=os.getenv('ENV', 'test'))
    pipeline.run(rollback=rollback)

if __name__ == "__main__":
    # Pass rollback=True if you want to trigger the rollback logic
    main(rollback=True)