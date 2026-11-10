# Hospital Appointment System (Django + MySQL)

A Django-based hospital appointment management project with a responsive Bootstrap frontend.

## Features
- Patient registration, login and logout
- Separate Django admin login at `/admin/`
- Patient and staff dashboards
- Doctor management (staff/admin)
- Appointment booking, listing, editing and cancellation
- Search and status filtering
- Server-side validation and error handling
- MySQL database connectivity
- Responsive Bootstrap 5 interface

## Requirements
- Python 3.10+
- MySQL Server 8.x (or compatible)
- pip

## 1. Create the MySQL database
Start MySQL Server (or start MySQL from XAMPP), then open MySQL Workbench or phpMyAdmin and run:

```sql
CREATE DATABASE hospital_appointment_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

The default configuration expects:
- Database: `hospital_appointment_db`
- Username: `root`
- Password: empty
- Host: `127.0.0.1`
- Port: `3306`

If your MySQL root account has a password, set the `DB_PASSWORD` environment variable before running Django.

## 2. Windows setup (PowerShell)
Open PowerShell in the extracted project folder:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `mysqlclient` installation fails on Windows, install the Microsoft C++ Build Tools and retry, or use a compatible prebuilt `mysqlclient` wheel for your Python version.

## 3. Configure MySQL credentials (if needed)
In the same PowerShell terminal, set your credentials:

```powershell
$env:DB_NAME="hospital_appointment_db"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

If your root password is blank, you can skip setting `DB_PASSWORD`.

## 4. Create tables and admin account
```powershell
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
```

Enter a username, email and password for your administrator account.

## 5. Start the application
```powershell
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Patient login: http://127.0.0.1:8000/accounts/login/
- Patient registration: http://127.0.0.1:8000/register/
- Admin login: http://127.0.0.1:8000/admin/

## Add doctors
1. Sign in at `/admin/` using the superuser credentials.
2. Open **Doctors → Doctors → Add doctor**.
3. Enter doctor name, specialty, email, phone, consultation fee and availability.
4. Save. The doctor appears in the public Doctors page and appointment form.

You can make another account a staff user in Django admin to grant access to staff dashboard and doctor management.

## Notes
- This is an academic/development project configuration. Before production use, configure secrets securely, HTTPS, database backups, access controls, audit logging, and privacy safeguards.
- Do not use real patient medical data in a demo environment.
