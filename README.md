# 📢 Notice Board Management System

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A full-stack web application designed to manage and display college/school notices.  
It features secure authentication with separate dashboards for **Admins** (publish/manage notices) and **Students** (view notices).

---

## ✨ Features

### 🔐 Authentication System
- Secure user registration and login  
- Password hashing using **Werkzeug**  
- Session management for persistent login  

### 👥 Role-Based Access

| Role    | Permissions |
|---------|-------------|
| **Admin**   | Create, edit, delete notices, categorize notices, set expiry dates, view all notices |
| **Student** | View active notices, filter by category, read full notice details |

### 📋 Notice Management
- Auto-filtering of expired notices  
- Real-time updates on homepage  
- Category-wise organization  
- Search and filter functionality  
- Notice expiry tracking  

### 🎨 User Interface
- Responsive design with **Bootstrap**  
- Clean and intuitive dashboard  
- Custom error pages (**404**, **500**)  
- Mobile-friendly layout  

---

## 🛠️ Tech Stack

| Component        | Technology                         |
|------------------|-------------------------------------|
| Backend          | Python 3.x, Flask                   |
| Frontend         | HTML5, Jinja2, Bootstrap CSS        |
| Database         | MySQL                                |
| Security         | Werkzeug Password Hashing            |
| Version Control  | Git & GitHub                         |

---

## 📁 Project Structure


notice-board-system/
│
├── app.py                
├── config.py             
├── requirements.txt       
├── Procfile             
├── .gitignore           
│
├── static/               
│   └── css/
│       └── style.css
│
└── templates/          
    ├── base.html
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── admin_dashboard.html
    ├── student_dashboard.html
    ├── about.html
    ├── 404.html
    └── 500.html
📦 Local Setup & Installation
✅ Prerequisites
Python 3.x

MySQL Server

Git (optional)

# 1️⃣ Clone the Repository
git clone https://github.com/SonuJaiswal6828/Notice-Board-System.git
cd Notice-Board-System

# 2️⃣ Install Dependencies
pip install flask mysql-connector-python werkzeug
Or:

pip install -r requirements.txt


# 3️⃣ Database Setup
Login to MySQL:

mysql -u root -p
Create database & tables:

CREATE DATABASE notice_board;
USE notice_board;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
⚠️ Important: Don’t commit real passwords to GitHub.

# 4️⃣ Configuration

Create config.py in root:

class Config:
    SECRET_KEY = 'your_super_secret_key_here_change_in_production'

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'your_mysql_password'
    MYSQL_DB = 'notice_board'

    DEBUG = True
# 5️⃣ Run the Application

python app.py
Open 👉 http://localhost:5000

## 🚀 Deployment Guide (Render + Cloud MySQL)

# Step 1️⃣ requirements.txt
Flask==2.3.3
mysql-connector-python==8.1.0
Werkzeug==2.3.7
gunicorn==21.2.0
python-dotenv==1.0.0

# Step 2️⃣ .env (Local Testing)
SECRET_KEY=your_super_secret_key
MYSQL_HOST=your-cloud-mysql-host
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database

# Step 3️⃣ config.py (Production)
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'notice_board')

    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
# Step 4️⃣ Procfile
web: gunicorn app:app

# Step 5️⃣ Deploy to Render
Push code to GitHub

Login to https://render.com

New ➜ Web Service ➜ Connect GitHub repo

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Add environment variables

Click Create Web Service

## 🔒 Security Best Practices
✅ Do's
Use strong SECRET_KEY in production

Keep DB credentials in environment variables

Use HTTPS

Regular password updates

Backup database regularly

## ❌ Don'ts
Don’t commit config.py with real credentials

Don’t use default admin credentials

Don’t expose DB ports publicly

Don’t disable CSRF protection

### 🤝 Contributing
Fork the repository

Create a branch:

git checkout -b feature/AmazingFeature
Commit changes:

git commit -m "Add AmazingFeature"
Push:

git push origin feature/AmazingFeature
Open a Pull Request

📝 License
This project is licensed under the MIT License.

### 👨‍💻 Developed By
Sonu Jaiswal

GitHub: https://github.com/SonuJaiswal6828

LinkedIn: Sonu Jaiswal

Email: sonujaiswal6828@gmail.com



📧 Contact
For support or queries: sonujaiswal6828@gmail.com

⭐ Star this repository if you find it helpful!

