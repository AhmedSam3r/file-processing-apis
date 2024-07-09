# File Management Service

## Project Structure

```
task/
│
├── project/
│   ├── app.py
│   ├── cli.py
│   ├── __init__.py
│   ├── files/
│   │   ├── models.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── ....
│   ├── migrations/
│   ├── static/
│   │   ├── files/
│   ├── templates/
│   ├── routes.py
│
├── run.py
├── venv/
├── requirements.txt
```

## Overview

This project provides a web service for file management, including functionalities like file upload, retrieving random lines from a file, getting the longest lines from a file, and maintaining metadata of uploaded files in a database.

## Setup Instructions

### Prerequisites

- Python 3.10+
- Virtual Environment (recommended)
- PostgreSQL 14 & up (or any SQL database supported by SQLAlchemy) 
- Flask 3.0
- Flask-Migrate
- Redis
- Celery 5.0

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/file-processing-apis.git
   cd file-processing-apis
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   Create a `.env` file in the root directory with the following content (update with your database credentials):

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost:5432/yourdatabase
   ```

5. **Initialize the database:**

   ```sh
   flask db init --directory project/migrations  # Only if migrations directory is not initialized
   flask db migrate -m "Initial migration" --directory project/migrations
   flask db upgrade --directory project/migrations
   ```
   #### To create empty migration file
   `flask db revision --directory project/migrations --empty -m "create_empty_migration"`

6. **Code quality check**
   #### After installing the flake8, you can run in the main directory the following
   ```flake8 --ignore E501`` 

7. **Celery**

   After Installing celery, open a new terminal and run it through `celery -A project.celery worker --loglevel=info` in the main directory


### Running the Application

1. **Start the Flask application:**

   ```sh
   flask --app run run --debug
   ```

2. **Navigate to the application:**

   Open your web browser and go to `http://localhost:5000`

## API Endpoints

### File Upload

- **URL:** `/file/upload`
- **Method:** `POST`
- **Description:** Upload a new file to the server.

### Get a Random Line from a File

- **URL:** `/file/random-line`
- **Method:** `GET`
- **Description:** Retrieve a random line from the specified file.

### Get 20 Longest Lines from a File

- **URL:** `/file/longest-lines`
- **Method:** `GET`
- **Description:** Retrieve the 20 longest lines from the specified file.

### Get Longest 100 Lines Across All Files

- **URL:** `/file/longest-lines-global`
- **Method:** `GET`
- **Description:** Retrieve the 100 longest lines across all files.


# Summary

This README provides a comprehensive overview of your project, setup instructions, API endpoints, and an example model. Adjust paths, URLs, and any other project-specific details as necessary.