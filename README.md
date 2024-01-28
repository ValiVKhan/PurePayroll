# Pure Payroll
Pure Payroll is a simple web application for running payroll and processing payments. It is built using the Flask web framework and the Bootstrap CSS library.

### Getting started
To get started, you will need to install the required packages. You can do this by running the following command:

Download
Copy code
pip install -r requirements.txt
Next, you will need to create a config.py file with the following content:

Download
Copy code
class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///purepayroll.db'
Replace 'your_secret_key_here' with a secret key of your choice.

To run the application, use the following command:

Download
Copy code
flask run
The application will be available at http://localhost:5000.

### Using the application
To use the application, you will need to sign up for an account. Once you have signed up, you can log in and create a company. You can then add employees to the company and run payroll for them.

The application will calculate the gross pay, deductions, and net pay for each employee based on the pay period and pay rate that you specify. It will also process the payments using Dwolla.

### Contributing
If you would like to contribute to the development of Pure Payroll, please fork the repository and submit a pull request.

### Acknowledgments
Pure Payroll uses the following libraries and resources:

Flask: a lightweight web framework for building web applications in Python.
Bootstrap: a popular CSS library for building responsive and mobile-first web applications.
Dwolla: a payment platform for sending and receiving money.
SQLite: a self-contained, file-based SQL database.
Flask-SQLAlchemy: an extension for Flask that adds support for SQLAlchemy, a popular Object-Relational Mapping (ORM) library for Python.
