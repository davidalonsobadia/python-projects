# Flask OAuth and Auth Service with User Management

## Overview
This is a Flask-based web application project that utilizes a SQLite database for user management and authentication. The project also includes Google OAuth support and email functionalities for further interactions. The application is structured to facilitate user login, registration, and more via Flask-Login and SQLAlchemy, along with additional features that can be extended as needed.

## Features
### User Authentication:

Supports user login and registration.
Password storage and retrieval using Flask-Login.
Google OAuth integration for social login via Google accounts.

### SQLite Database:

Users are stored in an SQLite database (your_database.db), with fields for username, email, and password.
SQLAlchemy is used as the ORM to handle database transactions.

### Email Support:

Email functionality using Gmail SMTP for sending emails. The email server configuration can be customized in the config.py file.
The application supports sending emails via Gmail's SMTP server (it needs to be configured in Gmail).

### Environment Configuration:

Environment variables are stored in a .env file and managed via python-dotenv.
The .env file handles sensitive configurations like secret keys, Google OAuth credentials, and email credentials.

### Project Structure
```
.
├── app.py               # Main application entry point
├── config.py            # Configuration settings (secret keys, database URIs, etc.)
├── models.py            # SQLAlchemy models for database interaction
├── routes.py            # Routes and request handling logic
├── .env                 # Environment variables (not included in repository for security)
├── your_database.db     # SQLite database file (generated automatically)
├── README.md            # Project README
```

## Installation & Setup
### Prerequisites
- Python 3.x must be installed.
- Virtual environment (Optional): It is recommended to use a Python virtual environment.
- Dependencies
Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

- Create the .env File
The .env file should store sensitive environment variables. Create a .env file in the root of the project directory with the following content:

```makefile
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=your_google_redirect_uri
MAIL_USERNAME=your_gmail_username
MAIL_PASSWORD=your_gmail_password
```

### Database Setup
Once everything is installed, you can initialize the database by running the following commands inside the Python shell:

```python
from app import db
db.create_all()
```
This will create a your_database.db SQLite file in the project directory, which will store user data.

## Running the Application
To run the Flask application, use the following command:

```bash
python app.py
```

By default, Flask runs on localhost:5000, and you can access the application in your browser via http://127.0.0.1:5000.

## Configuration Options
The config.py file handles the application's configuration settings, such as:

- SECRET_KEY: Required for session management and security.
- SQLALCHEMY_DATABASE_URI: URI for the SQLite database connection.
- Google OAuth Credentials: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REDIRECT_URI.
- Email Configuration: The application uses Gmail’s SMTP server to send emails.

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
```

## OAuth Integration (Google Login)
To set up Google OAuth for social login, follow these steps:

- Go to the Google Developer Console.
- Create a new project and generate OAuth 2.0 credentials.
- Add the Client ID, Client Secret, and Redirect URI to your .env file.

## Email Functionality

Emails are sent using Gmail's SMTP server. Update the MAIL_USERNAME and MAIL_PASSWORD fields in the .env file with your Gmail credentials.
Make sure that you enable Less secure apps in your Gmail account settings to allow the application to send emails.
If you can't do that in your Email account, consider using another SMTP Server, like SendGrid, for this feature.

## Database Models
The application uses SQLAlchemy ORM for database interactions. Currently, the User model is defined in the models.py file as:

```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

You can extend this model or add new models to accommodate additional features.

## Contribution Guidelines
- Fork the repository.
- Create a new branch.
- Make your changes.
- Submit a pull request for review.

## Security Note
Make sure to never commit your .env file or sensitive credentials to your Git repository. The .env file should be listed in your .gitignore file to prevent accidental leaks of sensitive information.

## License
This project is open-source and available under the MIT License.

