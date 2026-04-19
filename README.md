# SaaS Scheduling Dashboard 

A modern, premium internal operations dashboard built with a **Flask API backend** and a pristine, dependency-free **HTML/CSS frontend**. 

This system is designed as an all-in-one portal for teams to manage shift schedules, coordinate daily tasks, and calculate real-time attendance tracking via a digital clock-in system.

## 🚀 Features

- **SaaS-Grade UI**: A completely custom, visually stunning interface using CSS variables, flexbox grids, and the Inter font—designed to mirror apps like Stripe and Linear.
- **Role-Based Access Control**: Secure routing for both `Employee` and `Manager` accounts.
- **Task Management**: Create, assign, and track tasks (Pending, In Progress, Completed).
- **Shift Scheduling**: Assign employees precise time windows to work, viewable on their personal dashboard.
- **Time Clock**: Real-time punch card tracking timestamps for accurate session management.

## 🛠️ Tech Stack 

- **Backend Framework**: Python / Flask
- **Database Architecture**: Flask-SQLAlchemy + SQLite (local-mode) / MySQL (production)
- **Frontend Architecture**: Pure HTML5 and CSS3 (Jinja2 Templating). Zero Javascript frameworks (No React/Vue).
- **Authentication**: Native Flask Sessions & Werkzeug Password Hashing.

## ⚙️ How to Run Locally

### 1. Requirements
Ensure you have **Python 3.8+** installed. Optional: virtualenv.

### 2. Setup
Clone the repository and jump into the directory:
```bash
# Create and activate your environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `\.venv\Scripts\activate`

# Install dependencies (ensure you have Flask, SQLAlchemy, etc.)
pip install -r requirements.txt
```

### 3. Running the Server 
```bash
python3 main.py
```
Open `http://127.0.0.1:5000` in your web browser.

## 👑 Manager Access

By default, any new account created on the registration page is immediately registered as a standard **Employee**.

**To register as a Manager for administrative testing:**
When creating your account on the `/register` page, locate the optional `Manager Code` input field. Type the exact word `manager` into this box. The application will instantly flag your new user profile as a Manager, granting you access to the Admin portal!

---
*Created for CPSC 449 Back End Engineering*
*Team: Oscar Villela, Xiaohui Gao, Shaikh Amin*
