

#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Create the .env file
echo "Creating .env file..."
cat <<EOL > .env
SECRET_KEY=your_secret_key
MYSQL_DATABASE_HOST=localhost
MYSQL_DATABASE_USER=root
MYSQL_DATABASE_PASSWORD=root
MYSQL_DATABASE_DB=billdb
EOL
echo ".env file created successfully."

# Step 4: Create a Python virtual environment
echo "Setting up Python virtual environment..."
cd billing

if [ ! -d "venv" ]; then
    python3 -m venv ./venv
    echo "Virtual environment created in 'billing/venv'."
else
    echo "Virtual environment already exists in 'billing/venv'."
fi

# Step 5: Activate the virtual environment and install requirements
echo "Activating virtual environment and installing dependencies..."
source ./venv/bin/activate
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies. Please check the logs for details."
    exit 1
fi

# Step 2: Run the Docker container
echo "Starting MySQL Docker container..."
docker run --rm --name mysql-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=billdb -v $(pwd)/database/billingdb.sql:/docker-entrypoint-initdb.d/billingdb.sql mysql:9.0.1

if [ $? -eq 0 ]; then
    echo "MySQL Docker container started successfully."
else
    echo "Failed to start the MySQL Docker container. Please check the logs for details."
    exit 1
fi

# Step 3: Wait for 10 seconds and check if the container is running
echo "Waiting 10 seconds to verify if the container is running..."
sleep 10

if docker ps --filter "name=mysql-db" --filter "status=running" | grep -q mysql-db; then
    echo "MySQL Docker container is running successfully."
else
    echo "MySQL Docker container is not running. Please check the logs for issues."
    exit 1
fi



# Return to the original directory
cd ..
