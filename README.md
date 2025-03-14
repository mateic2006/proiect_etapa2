# Driving School Project

This project is a web application for a driving school, built using Flask and a SQL Server database. The application allows users to sign up, log in, and manage their accounts. It also provides functionalities for instructors and students to interact with the system.

## Features

- User authentication (sign up, log in, log out)
- Role-based access control (instructors and students)
- Dashboard for viewing and managing lessons
- Email verification and password reset
- Simple and complex queries for retrieving data from the database

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:
    ```bash
    cd Driving_school
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    - Create a `.env` file in the project root directory.
    - Add the following environment variable:
        ```
        SECRET_KEY=your_secret_key
        ```

5. Update the database connection string in `server-app.py` to match your SQL Server configuration.

## Usage

1. Run the Flask application:
    ```bash
    python server-app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Routes

- `/` - Home page
- `/login` - User login
- `/signup` - User sign up
- `/dashboard` - User dashboard
- `/verify-email` - Email verification
- `/reset` - Password reset
- `/logout` - User logout
- `/toggle-menu` - Toggle menu (for UI purposes)
- `/delete` - Delete user account
- `/simple-query/<int:query_number>` - Execute simple queries
- `/complex-query/<int:query_number>` - Execute complex queries
- `/interogari` - Query page

## Database Schema

The application uses the following tables:

- `Utilizatori` - Stores user information (username, password, role)
- `Elevi` - Stores student information (CNP, name, birth date, phone, email, user ID)
- `Instructori` - Stores instructor information (CNP, name, phone, email, experience years, user ID)
- `Lectii` - Stores lesson information (lesson ID, student CNP, instructor CNP, date, vehicle series)
- `Vehicule` - Stores vehicle information (series, brand, model)
- `Plati` - Stores payment information (payment ID, student CNP, amount, date)
- `Recenzii` - Stores reviews (rating, student CNP, instructor CNP)

## License

This project is licensed under the MIT License.

## Acknowledgements

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- pyodbc: [https://github.com/mkleehammer/pyodbc](https://github.com/mkleehammer/pyodbc)

