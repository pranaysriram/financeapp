# Finance Tracking System

## Project Overview

This project is a Python-based Finance Tracking System that allows users to manage and analyze their financial records.  
The application supports storing income and expense transactions, viewing financial summaries, and implementing role-based access control.

The system is designed to demonstrate backend development skills including API design, data handling, validation, and logical structuring of application components.

---

## Features

### User Authentication
- User registration
- User login and logout
- Session-based authentication

### Role Based Access Control
The system supports three types of users:

Admin:
- Can create transactions
- Can delete transactions
- Can view financial summary

Analyst:
- Can view transactions
- Can view summary reports

Viewer:
- Can only view transactions

---

### Financial Records Management

Users can manage financial records including:

- Amount
- Transaction type (Income or Expense)
- Category
- Date
- Notes

CRUD Operations:
- Create transaction
- View transactions
- Delete transaction

---

### Financial Summary

The system calculates:

- Total Income
- Total Expenses
- Current Balance

Balance formula:
Balance = Total Income - Total Expense

---

## Technologies Used

- Python
- Flask
- HTML
- CSS
- SQLite

---

## Project Structure

finance_project/

app.py → main backend application

database.db → SQLite database

templates/ → HTML pages

static/ → CSS styling

README.md → documentation

---

## Installation and Setup

Step 1: Install dependencies

pip install flask

Step 2: Run the application

python app.py

Step 3: Open browser

http://127.0.0.1:5000/

---

## Assumptions

- Simple authentication system implemented
- SQLite database used for simplicity
- Basic UI used to focus on backend logic
- Role-based permissions implemented

---

## Future Improvements

- Update transaction feature
- Filter transactions by category or date
- Export financial report to CSV
- Graphical charts for analytics
- Password encryption for better security

---

## Conclusion

This project demonstrates backend development skills such as Python programming, database integration, business logic implementation, and application structuring using Flask framework.
