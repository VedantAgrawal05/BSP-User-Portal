# 🏭 SAIL Bhilai Steel Plant (BSP) — Remodeled User Portal

An enterprise employee attendance, shift tracking, and human resources portal designed for the **Steel Authority of India Limited (SAIL) — Bhilai Steel Plant (BSP)**. Developed as a Vocational Training Project under the **Computer & Information Technology (C&IT) Department**, Bhilai Steel Plant.

---

## 👥 Project Team
- **Animesh Banerjee**
- **Arnav Kaser**
- **Vedant Agrawal** ([@VedantAgrawal05](https://github.com/VedantAgrawal05))

---

## ✨ Features & Capabilities

### 1. ⏱️ Live Plant Shift & Real-Time Duty Tracker
- Real-time dynamic shift mapping matching SAIL operational timings:
  - **Shift A (Morning)**: `06:00 AM – 02:00 PM`
  - **General Shift (G)**: `09:00 AM – 05:00 PM`
  - **Shift B (Evening)**: `02:00 PM – 10:00 PM`
  - **Shift C (Night)**: `10:00 PM – 06:00 AM`
- Live ticking digital clock with auto-updating duty status pill badges (*On Duty*, *Shift Completed*, *Punch In Pending*).
- Immediate punch-in and punch-out logging with duplicate punch prevention.

### 2. 📊 Central HR & Department HR Analytics
- **Superuser / Central HR Dashboard**: Plant-wide visibility of employee strength, total check-ins today, attendance percentage, and department-by-department breakdowns.
- **Department HR Dashboard**: Departmental attendance metrics, frequent late arrivals alert, and monthly attendance charts.
- **Filtered Roster Views**: One-click drill-downs into *Present Today*, *Absent Today*, and *Late Arrivals*.

### 3. 📥 CSV Spreadsheet Export
- One-click roster export for Central HR and Department HR:
  - **Employee Directory CSV**: Full profile records, IDs, designations, contact information, and plant departments.
  - **Daily Attendance Roster CSV**: Timestamped record of today's attendance status across all plant departments.

### 4. 📄 Printable SAIL Payslip
- Branded, print-ready digital payslip with SAIL header, employee details, pay slab breakdown (Basic Salary, Allowances, Deductions, Net Salary), and formatted currency in Indian numbering system (`₹ XX,XX,XXX`).

### 5. 🔔 Modern Toast Notifications
- Instant visual feedback on all user actions (punch in, punch out, new employee registration, validation alerts) with auto-dismissing toast alerts.

### 6. 🌱 One-Command Automated Data Seeder
- Includes `python manage.py seed_data` to automatically provision 11 plant departments, 11 designations, 10 pay slabs, 6 demo accounts, and 30 days of realistic attendance history.

---

## 🛠️ Technology Stack
- **Backend Framework**: Python 3.13 / Django 5.2 (LTS)
- **Database**: MySQL 8.0 / MySQL Connector
- **Frontend**: Responsive HTML5, Modern CSS3 (Glassmorphism / Dark Theme), Vanilla JavaScript
- **Security & Config**: `python-dotenv` environment variable isolation

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/VedantAgrawal05/BSP-User-Portal.git
cd BSP-User-Portal
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
venv\Scripts\activate   # On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and set your MySQL credentials:
```ini
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=bsp_site_2
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 4. Initialize Database & Seed Demo Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Launch Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open **http://127.0.0.1:8000/** in your browser.

---

## 🔑 Pre-Configured Demo Accounts

| Username | Role / Department | Default Password | Access Level |
|---|---|---|---|
| `central_hr` | Central Human Resources | `Logitech1*` | Superuser / Central HR Admin |
| `hr_user` | Dept HR (Computer & IT) | `Logitech1*` | Department HR Dashboard |
| `user2` | Mechanical Engineering | `Logitech1*` | Standard Employee Portal |
| `archit` | Information Technology | `Logitech1*` | System Administrator |

---

## 📜 License
Developed for educational and training purposes for Bhilai Steel Plant (SAIL). All rights reserved.
