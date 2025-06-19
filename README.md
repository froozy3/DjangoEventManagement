# Event Management API


## Features
- User Authentication with JWT
- Event Creation and Management
- RESTful API Architecture
- Swagger/OpenAPI Documentation
- Docker Container Support
- Email Notifications

## Tech Stack
- Django REST Framework
- SQLite
- Docker
- Swagger/OpenAPI
- JWT Authentication

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/froozy3/DjangoEventManagement.git
   ```

2. Configure environment variables:
   Create a `.env` file in the root directory with the following:
   ```env
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```
   Note: For EMAIL_HOST_PASSWORD you need to request password from passwrod secutriy(GOOGLE)

3. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

4. Access the API:
   - API Documentation: http://127.0.0.1:8000/api/docs/
   - Default admin credentials:
     ```json
     {
       "username": "admin",
       "password": "admin"
     }
     ```

## API Authentication
1. Login using the credentials above
2. Copy the access token from the response
3. Click the "Authorize" button in Swagger UI
4. Enter the token in format: `Bearer <your_token>`

## API Documentation
Full API documentation is available at `/api/docs/` endpoint after running the server.
