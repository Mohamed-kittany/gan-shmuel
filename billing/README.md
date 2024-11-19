
# Billing Microservice

## Overview
The **Billing Microservice** is a component of the Gan Shmuel Project, designed to manage payments to fruit providers based on truck weights and product rates. It integrates with other services, such as the Weight Microservice, to calculate net weights and generate provider bills.

## Features
- Register and manage providers.
- Upload and manage product rates.
- Register and manage trucks.
- Generate detailed billing reports for providers.
- Modular, RESTful API design for scalability.

## Architecture
The service uses a modular architecture built with Flask, making it easy to extend and maintain. Key components include:
- **Routing Layer**: Defines RESTful endpoints.
- **Service Layer**: Contains business logic.
- **Utilities and Extensions**: Handles logging, configuration, and other utilities.
- **Database Integration**: Uses `mysql-connector-python` for persistence.

## Prerequisites
- Docker and Docker Compose
- Python 3.9 or higher
- MySQL database

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd billing
   ```
2. Set up the environment:
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your database credentials.

3. Build and run the application:
   ```bash
   docker-compose up --build
   ```

## API Endpoints
### Provider Management
- `POST /provider` - Create a new provider.
- `PUT /provider/{id}` - Update provider details.

### Truck Management
- `POST /truck` - Register a truck.
- `PUT /truck/{id}` - Update truck information.

### Rate Management
- `POST /rates` - Upload product rates.
- `GET /rates` - Download product rates.

### Billing
- `GET /bill/{id}` - Retrieve billing details for a provider.

### Health Check
- `GET /health` - Check the service health.

## Testing
Run tests using `pytest`:
```bash
pytest
```

## Logging
Logs are stored in the `logs/` directory.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Commit changes and open a pull request.