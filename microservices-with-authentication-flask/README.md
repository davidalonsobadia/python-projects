# Microservices with Authentication and NGINX

This project demonstrates a microservices architecture with Flask, JWT-based authentication, and NGINX as a reverse proxy. The system consists of three microservices (Authentication Service, User Service, and Address Service) and uses Docker for containerization.

## Project Overview

### Architecture
- **Authentication Service**: Handles user authentication and issues JWT tokens.
- **User Service**: Manages user data.
- **Address Service**: Manages address data.
- **NGINX**: Acts as a reverse proxy to route requests and handle path rewriting.

### Components
1. **Flask Services**:
   - **Authentication Service**: Manages login and token generation.
   - **User Service**: Provides endpoints for user management.
   - **Address Service**: Provides endpoints for address management.
2. **NGINX**: Handles path rewriting and proxies requests to the appropriate service.
3. **Docker**: Containerizes each service and NGINX, managed by Docker Compose.

## Installation

### Prerequisites
- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

### Clone the Repository
```bash
git clone https://github.com/yourusername/microservices-with-authentication-flask.git
cd microservices-with-authentication-flask
```

## Build and Run
1. Navigate to the project directory:
```bash
cd microservices-with-authentication-flask
```
2. Build and start the services using Docker Compose:
```bash
docker-compose up --build
```
This command builds the Docker images for each service and starts the containers.

## Configuration
### NGINX Configuration
NGINX is configured to forward requests based on the path. The nginx.conf file contains the routing rules:

- /auth/ routes to the Authentication Service.
- /user/ routes to the User Service.
- /address/ routes to the Address Service.

### Dockerfile for Each Service
Each service has its own Dockerfile for building the image:

 - **Authentication Service** (authentication_service/Dockerfile)
 - **User Service** (user_service/Dockerfile)
 - **Address Service** (address_service/Dockerfile)
 - **NGINX** (nginx/Dockerfile)

## Usage
### Authentication Service
 - Register User:
 ```bash
 curl --location 'http://localhost/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "userName",
    "password": "password",
    "email": "email@gmail.com",
    "full_name": "FullName"
}'
 ```
 - Login:
```bash
curl --location 'http://localhost/auth/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "userName",
    "password": "password"
}'
```
Returns a JWT token upon successful login.
### User Service
 - Get User Data:
```bash
curl --location 'http://localhost/user/profiles/<username>' \
--header 'Authorization: Bearer <YOUR_JWT_TOKEN>'
```
Replace <YOUR_JWT_TOKEN> with the token obtained from the authentication service.

### Address Service
 - Post new Address Data:
```bash
curl --location 'http://localhost/address/addresses' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <YOUR_JWT_TOKEN>' \
--data '{
    "street": "some street",
    "city": "some city",
    "postal_code": "1234"
}'
``` 
 - Get Address Data:
```bash
curl --location 'http://localhost/address/addresses' \
--header 'Authorization: Bearer <YOUR_JWT_TOKEN>'
```
Replace <YOUR_JWT_TOKEN> with the token obtained from the authentication service.

## Project Structure
```
project/
├── authentication_service/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── user_service/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── address_service/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
└── docker-compose.yml
```


### Notes
- **Security**: The SECRET_KEY used in the Flask services should be kept secure and not exposed in the codebase. In production, consider using environment variables or a secrets management system.
- **Scaling**: For production, you may want to use a more robust setup with multiple instances of each service and additional load balancing strategies.
### Troubleshooting
- **Service Not Reachable**: Ensure all services are running by checking Docker logs:
```bash
docker-compose logs
```
- **NGINX Configuration Issues**: Verify the NGINX configuration file for syntax errors and reload NGINX:
```bash
docker-compose restart nginx
```


### Key Points
- **Installation**: Instructions to clone the repository, build, and run the services.
- **Configuration**: Details about NGINX and Dockerfile setup.
- **Usage**: Examples of how to interact with the services.
- **Project Structure**: Overview of the folder structure and purpose of each component.
- **Notes**: Security considerations and scaling advice.
- **Troubleshooting**: Common issues and their solutions.

Feel free to adjust any details according to your specific needs or project updates.