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

## Local Deployment Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git (optional, for cloning)

### Step 1: Get the Code
**Option A: Clone from GitHub**
```bash
git clone https://github.com/sandeep-yadav-108/travel-lykke-assignment.git
cd travel-lykke-assignment
```

**Option B: Download ZIP**
- Download ZIP from GitHub repository
- Extract to your desired location
- Navigate to the project folder

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv travel_env

# Activate virtual environment
# On Windows:
travel_env\Scripts\activate
# On macOS/Linux:
source travel_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
**Install MySQL** (if not already installed):
- Download Install and set up MySQL server

**Create Database:**
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE travellykke_db;

-- Create user (optional)
CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON travellykke_db.* TO 'travel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 5: Environment Configuration
Create `.env` file in the project root:
```bash

Edit `.env` with your MySQL credentials:
```env
DB_NAME=travellykke_db
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 6: Django Setup
```bash
# Run database migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Load sample travel data
python manage.py create_sample_data

# Collect static files (if needed)
python manage.py collectstatic
```

### Step 7: Run the Application
```bash
python manage.py runserver
```

🌐 **Access your application:**
- Main site: [http://localhost:8000](http://localhost:8000)
- Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Testing
```bash
python manage.py test
```


### Development Commands:
```bash
# Check for issues
python manage.py check

# Create new migrations
python manage.py makemigrations

# View SQL for migrations
python manage.py sqlmigrate booking 0001

# Django shell
python manage.py shell
```

## Project Structure
```
travel-lykke-assignment/
├── booking/                  # Main Django app
│   ├── models.py            # TravelOption, Booking models
│   ├── views.py             # Business logic and views
│   ├── templates/           # HTML templates
│   ├── forms.py             # Custom forms
│   ├── tests.py             # Unit tests
│   ├── management/          # Custom management commands
│   └── templatetags/        # Custom template filters
├── travellykke/             # Django project settings
│   ├── settings.py          # Configuration
│   └── urls.py              # URL routing
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```


