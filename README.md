### API Documentation


## 1. API Endpoints

- **Create Event**: `api/events/create/` (POST)
  **Request Body**: 
    ```json
    {
      "title":"Conference Python Devoloper",
      "description":"A conference for Python developers to share knowledge and network.",
      "location":"Online, Zoom",
      "date": "2024-12-25T12:00:00Z"
    }
- **Update Event**: `api/events/update/{id}` (PATCH)
-  **Request Body**: 
    ```json
    {
      "title":"Conference Java Devoloper",
      "description":"A conference for Java developers to share knowledge and network.",
      "location":"Kyiv, UA",
      "date": "2024-12-25T12:00:00Z"
    }
- **Delete Event**: `api/events/delete/{id}` (DELETE)
- **List Events**: `api/events/` (GET)
- **Single Event**: `api/events/{id}` (GET)
- **Registration**: `auth/register/` (POST)
   **Request Body**: 
    ```json
   {
    "username":"test_user",
    "email": "test@gmail.com",
    "password": "test_user"
   }
  
- **Login**: `auth/token/` (POST)
- -  **Request Body**: 
    ```json
   {
    "username":"test_user",
    "password": "test_user"
   }
- **Logout**: `auth/logout/` (POST)

   **Request Body**: 
    ```json
    {
      "title":"Conference Python Devoloper",
      "description":"A conference for Python developers to share knowledge and network.",
      "location":"Online, Zoom",
      "date": "2024-12-25T12:00:00Z"
    }

- **Response**:
   ```json
   {
      
    "id": 1,
    "title": "Conference Python Devoloper",
    "description": "A conference for Python developers to share knowledge and network.",
    "date": "2024-12-25T12:00:00Z",
    "location": "Online, Zoom",
    "organizer": 1,
    "registered_users": []

   }

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/froozy3/DjangoEventManagement.git
   ```
2. Create docker image:
   ```bash
   docker build -t django-event-management .
   ```

2. Run the docker container
   ```bash
   docker run -p 8000:8000 django-event-management
   ```
# Bonus Points: Features
   * **Filtering**: Add functionality to filter events (`api/events/?title=python&location=online`).
   * **Email Notifications**: Send email notifications to users upon event registration. Create and insert your own settings in the .env file.
