# Travel Lykke - Travel Booking Application

A Django web application for booking flights, trains, and buses.

## Features

- User registration and authentication
- Browse and filter travel options (flights, trains, buses)
- Book travel with seat validation
- View and cancel bookings
- User profile management
- Admin interface for managing travel data

## Technology Stack

- Django 5.2.5
- MySQL Database
- Bootstrap 5.3.3
- Python 3.8+

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy update with your MySQL credentials:
```env
DB_NAME=travellykke_db
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 3. Database Setup
```sql
CREATE DATABASE travellykke_db;
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Load Sample Data
```bash
python manage.py create_sample_data
```

### 7. Run Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Testing
```bash
python manage.py test
```

## Admin Access
Visit `/admin/` with superuser credentials to manage travel options and bookings.

## Project Structure
```
booking/                  # Main application
├── models.py            # TravelOption, Booking models
├── views.py             # Business logic
├── templates/           # HTML templates
└── tests.py             # Unit tests
```


