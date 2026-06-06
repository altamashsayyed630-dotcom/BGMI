# 🎮 BGMI Tournament Management System

A full-stack web application for managing BGMI (Battlegrounds Mobile India) tournaments — featuring user authentication, team registration, live highlights, points table, and Razorpay payment integration.

## 🌐 Live Demo
🔗 https://bgmi-jp1u.onrender.com

## 📁 GitHub Repository
🔗 https://github.com/altamashsayyed630-dotcom/BGMI

---

## ✨ Features

- 🔐 **User Authentication** — Signup & Login with MySQL database
- 🏆 **Tournament Groups** — Group A, B, C team listings
- 📊 **Points Table** — Live standings via CSV data
- 🎥 **Highlights** — Video highlights hosted on AWS S3
- 📝 **Team Registration** — Full player & team info form
- 💳 **Razorpay Payment** — ₹500 registration fee integration
- 📬 **Contact Form** — Messages stored in database
- 📱 **Responsive Design** — Mobile-friendly UI

---

## 🛠️ Tech Stack

| Technology | Usage |
|-----------|-------|
| Python + Flask | Backend web framework |
| MySQL (Aiven Cloud) | Cloud database |
| HTML5 + CSS3 | Frontend templates (Jinja2) |
| Razorpay API | Payment gateway |
| AWS S3 | Video highlights hosting |
| Render.com | Backend deployment |
| GitHub | Version control & CI/CD |

---

## 🗄️ Database Schema

### Tables Used:

**sign** — User authentication
```sql
CREATE TABLE sign (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email_id VARCHAR(100),
  password VARCHAR(100),
  confirm_password VARCHAR(100)
);
```

**contact_us** — Contact form submissions
```sql
CREATE TABLE contact_us (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email_id VARCHAR(100),
  subject VARCHAR(200),
  Message TEXT
);
```

**service_request** — Team registration data
```sql
CREATE TABLE service_request (
  id INT AUTO_INCREMENT PRIMARY KEY,
  Full_Name VARCHAR(100),
  In_game_Name VARCHAR(100),
  BGMI_UID VARCHAR(100),
  phone_number VARCHAR(20),
  email VARCHAR(100),
  Age_DOB VARCHAR(50),
  City VARCHAR(100),
  Team_Name VARCHAR(100),
  Role_in_team VARCHAR(50),
  Device_Name VARCHAR(100)
);
```

---

## 🚀 Setup Instructions (Local)

### 1. Clone the Repository
```bash
git clone https://github.com/altamashsayyed630-dotcom/BGMI.git
cd BGMI
```

### 2. Install Dependencies
```bash
pip install flask mysql-connector-python razorpay
```

### 3. Setup XAMPP (Local Database)
- Start Apache & MySQL in XAMPP
- Open phpMyAdmin → Create database: `dbproject`
- Run the SQL queries above to create tables

### 4. Update Database Credentials in `app.py`
```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dbproject"
    )
```

### 5. Add CSV Files
- Place `point.csv` and `data.csv` in `static/` folder

### 6. Run the App
```bash
python app.py
```
Open: http://localhost:5000

---

## ☁️ Deployment Guide (How We Made It Live)

### Step 1: Cloud Database Setup (Aiven MySQL)
1. Created free account at **https://aiven.io**
2. Created MySQL 8.4 service (Free tier)
3. Got connection credentials (host, port, user, password)
4. Created tables using Python script from local terminal:
```bash
python -c "
import mysql.connector
conn = mysql.connector.connect(
    host='YOUR_AIVEN_HOST',
    port=13868,
    user='avnadmin',
    password='YOUR_PASSWORD',
    database='defaultdb',
    ssl_disabled=False
)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS sign (...)')
conn.commit()
conn.close()
"
```

### Step 2: GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/BGMI.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render.com
1. Created account at **https://render.com**
2. New → Web Service → Connected GitHub repo
3. Settings:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
4. Added Environment Variables in Render Dashboard
5. Clicked **Deploy** → Live in 2 minutes! ✅

---

## 📂 Project Structure

```
BGMI/
├── app.py                  # Main Flask application
├── db.py                   # Database connection helper
├── requirements.txt        # Python dependencies
├── static/
│   ├── point.csv           # Points table data
│   ├── data.csv            # Additional data
│   └── pichure/            # Background images
└── templates/
    ├── login.html          # Login page
    ├── sign.html           # Signup page
    ├── home.html           # Home/Dashboard
    ├── table.html          # Points table
    ├── Highlight.html      # Video highlights
    ├── serviceRequest.html # Team registration
    ├── payment.html        # Razorpay payment
    └── contact.html        # Contact form
```

---

## 🔌 API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET/POST | `/login` | User login |
| GET/POST | `/sign` | User signup |
| GET | `/home` | Dashboard |
| GET | `/table` | Points table |
| GET | `/Highlight` | Video highlights |
| GET/POST | `/serviceRequest` | Team registration |
| GET | `/payment` | Payment page |
| POST | `/create_order` | Razorpay order creation |
| GET/POST | `/contact` | Contact form |

---

## 👨‍💻 Developer

**Altamash Sayyed**
Built as part of personal project — 2026
