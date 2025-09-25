# Banking Management System (Python + MySQL)
This is a **Banking Management System** built using **Python** and **MySQL**.  
It allows users to register, log in, manage accounts, perform transactions, and view statements.  
Admins can monitor all accounts and transactions.

---

## Features

### User
- Register a new account (Savings, Current, Salary, Fixed Deposit)
- Login with account number & PIN
- View account details
- Check balance
- Change PIN with OTP verification
- Deposit / Withdraw money
- Get transaction statements (daily, between dates, full history)
- Transfer funds between accounts

### Admin 
- Login with Admin ID & Password
- View all users or a single user
- View transactions of a particular user
- View all transactions on a particular day
- View transactions between date ranges
- Monitor full banking system

---

## Tech Stack
- **Language**: Python 3.10
- **Database**: MySQL
- **Libraries Used**:
  - `mysql-connector-python` - Connect Python with MySQL
  - `tabulate` - Display tables in a neat format
  - `colorama` - Colored terminal outputs
  - `datetime`, `random`, `time` - Built-in Python libraries

---

## Setup Instructions

### 1. Clone Repository 
```
https://github.com/Madhavasai21/Banking-Management-system.git
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Setup Database
- Open MySQL and create database
  ```
  CREATE DATABASE Bank;
  USE Bank;
  ```
- Create required tables
  ```
  CREATE TABLE users (
      User_Name VARCHAR(30),
      Account_Number BIGINT PRIMARY KEY,
      Account_Type ENUM('Savings', 'Current'),
      phone_no VARCHAR(12) UNIQUE,
      Pin CHAR(4),
      Amount BIGINT,
      Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  
  CREATE TABLE transactions (
      Transaction_id VARCHAR(30) PRIMARY KEY,
      Account_number BIGINT,
      Transaction_type VARCHAR(10), -- 'Credit' or 'Debit'
      Transaction_amount INT,
      Transaction_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      Available_Amount INT,
      FOREIGN KEY (Account_number) REFERENCES users(Account_Number)
  );
  
  CREATE TABLE admin (
      admin_id BIGINT PRIMARY KEY,
      Admin_Name VARCHAR(20),
      Password CHAR(6),
      Email_id VARCHAR(25),
      Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  ```
---

### 4. Run the project 
```
python main.py
```
### Sample Workflow
1. User registers - gets a 14-digit account number.
2. User logs in → deposits, withdraws, transfers, or checks balance.
3. Admin logs in → views all users & transactions.
4. All actions stored in transactions table for records.

### Features Demo
- User Registration
- User Actions
- Admin Login & Actions

### Note
- Minimum deposit to Open account - 500rs
- PIN - 4 digits only
- Account Number - 14 digits (auto-generated)


  
