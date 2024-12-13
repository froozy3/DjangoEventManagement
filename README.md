API realized bonus points: implement like filtering and send emails to users upon event registration.
### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/froozy3/DjangoEventManagement.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\Activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Setting Up Email Sending for Event Registration
   To enable the email-sending functionality upon event registration, you need to:
	1.	Create a .env file in the root directory of your project.
	2.	Add the following fields with your email configuration:
   ```bash
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_password
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
 
   Default values are provided in the project, but it is recommended to replace them with your own credentials for security and functionality.

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the app at [http://localhost:8000](http://localhost:8000).

### Docker (Optional)

If you prefer to use Docker:

1. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```

2. Access the app at [http://localhost:8000](http://localhost:8000).
