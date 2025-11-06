# 🏨 Hotel Management System

A comprehensive hotel booking and management system built with **Streamlit** and **MySQL**. This system provides a simple yet powerful interface for managing hotels, bookings, staff, and customers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [User Roles](#-user-roles)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔐 Authentication & Security
- Secure password hashing with SHA-256
- Role-based access control (RBAC)
- Session management
- User registration and login

### 👨‍💼 Admin Dashboard
- **User Management**: Create and manage system users
- **Staff Management**: Add and manage hotel staff
- **Hotel Management**: Add, edit, and manage hotel properties
- **Booking Management**: View and manage all bookings
- **Analytics**: Revenue reports and booking statistics
- **System Overview**: Real-time dashboard with key metrics

### 👔 Staff Dashboard
- View today's bookings
- Quick check-in operations
- Guest search functionality
- Booking management tools

### 🛎️ Customer Dashboard
- Browse available hotels
- Search hotels by location
- Make room bookings
- View booking history
- Manage personal profile

### 📊 Advanced Features
- Real-time booking availability
- Automated booking confirmations
- Revenue tracking and reporting
- Responsive UI with custom styling
- Data validation and error handling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Interface (Streamlit)               │
├─────────────────────────────────────────────────────────────┤
│                     Application Layer (Python)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   app.py     │  │   auth.py    │  │ database.py  │     │
│  │ (Main App)   │  │ (Auth Logic) │  │ (DB Utils)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                     Database Layer (MySQL)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Users     │  │   Hotels     │  │  Bookings    │     │
│  │    Roles     │  │    Rooms     │  │   Payments   │     │
│  │ User_Roles   │  │    Login     │  │   Reviews    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Three-Role System

| Role | Icon | Description |
|------|------|-------------|
| **Admin** | 🔧 | Full system control, manage users, staff, hotels, and analytics |
| **Staff** | 👔 | Manage bookings, check-ins, and guest services |
| **Customer** | 🛎️ | Browse hotels, make bookings, view history |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
  - Download from [python.org](https://www.python.org/downloads/)
  
- **MySQL Server 5.7 or higher**
  - Download from [mysql.com](https://dev.mysql.com/downloads/)
  
- **pip** (Python package manager)
  - Usually comes with Python installation

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bugsNburgers/Hotel-Management-System.git
cd Hotel-Management-System
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `streamlit` - Web application framework
- `mysql-connector-python` - MySQL database connector
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualizations

---

## 🗄️ Database Setup

### 1. Start MySQL Server

Ensure your MySQL server is running:

```bash
# Windows (if MySQL is in PATH)
net start MySQL80

# Or start via MySQL Workbench or Services
```

### 2. Configure Database Connection

Edit `db_config.py` with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Your MySQL username
    'password': 'your_password',  # Your MySQL password
    'database': 'hotel_booking_system'
}
```

### 3. Create Database and Tables

Run the schema file to create the database structure:

```bash
mysql -u root -p < schema.sql
```

Or manually in MySQL:

```sql
mysql -u root -p
source schema.sql;
```

### 4. Create Staff User (Optional)

Run the setup script to create a default staff user:

```bash
python fix_staff_user.py
```

---

## 🎯 Running the Application

### Start the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Default Login Credentials

| Role | Username/Email | Password |
|------|---------------|----------|
| **Admin** | `admin` | `adminpass` |
| **Staff** | `staff@hotel.com` | `staffpass` |
| **Customer** | (Register via UI) | - |

⚠️ **Important**: Change default passwords after first login!

---

## 👥 User Roles

### 🔧 Admin
**Full system administrator with complete access**

**Capabilities:**
- Create and manage users (admin/staff/customer)
- Add and configure hotels
- Manage all bookings across the system
- View revenue reports and analytics
- Assign roles and permissions
- System configuration

**Use Cases:**
- System setup and configuration
- User account management
- Hotel property management
- Financial reporting
- System maintenance

---

### 👔 Staff
**Hotel staff managing day-to-day operations**

**Capabilities:**
- View today's bookings and check-ins
- Search for guest bookings
- Manage booking status
- Handle customer inquiries
- Basic operational tasks

**Use Cases:**
- Front desk operations
- Guest check-in/check-out
- Booking assistance
- Customer service

---

### 🛎️ Customer
**End users booking hotel rooms**

**Capabilities:**
- Browse available hotels
- Search hotels by location
- Make room bookings
- View booking history
- Manage personal profile
- Leave reviews (if enabled)

**Use Cases:**
- Hotel search and booking
- Trip planning
- Booking management
- Account management

---

## 📖 Usage Guide

### For Admins

1. **Login** with admin credentials
2. **Dashboard** - View system overview and statistics
3. **Manage Users** - Create new users in User Management tab
4. **Add Hotels** - Configure hotel properties in Hotels tab
5. **View Reports** - Check revenue and booking analytics

### For Staff

1. **Login** with staff credentials
2. **View Today's Bookings** - See current day's check-ins
3. **Search Guests** - Look up booking information
4. **Manage Bookings** - Update booking status

### For Customers

1. **Register** - Create a new customer account
2. **Browse Hotels** - Search available properties
3. **Make Booking** - Select hotel, dates, and room type
4. **View History** - Check past and upcoming bookings

---

## 📁 Project Structure

```
hotel-management-system/
│
├── app.py                  # Main Streamlit application
├── auth.py                 # Authentication logic
├── database.py             # Database utility functions
├── db_config.py            # Database configuration
├── schema.sql              # Database schema and sample data
├── fix_staff_user.py       # Staff user setup script
├── check_users.py          # User verification utility
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── CHANGES_SUMMARY.md      # Change log and system updates
│
└── __pycache__/            # Python cache files
```

### Key Files

- **`app.py`** (877 lines) - Main application with all UI components and business logic
- **`auth.py`** - User authentication and password hashing
- **`database.py`** - Database connection and query utilities
- **`schema.sql`** (305 lines) - Complete database schema with tables, procedures, and sample data
- **`db_config.py`** - MySQL connection configuration

---

## ⚙️ Configuration

### Database Configuration

Edit `db_config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',      # Database host
    'user': 'root',           # MySQL username
    'password': 'password',   # MySQL password
    'database': 'hotel_booking_system'
}
```

### Application Settings

In `app.py`, you can customize:

```python
# Page configuration
st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🏨",
    layout="wide"
)

# Role emojis
ROLE_EMOJIS = {
    'admin': '🔧',
    'staff': '👔',
    'customer': '🛎️'
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error

**Error:** `Can't connect to MySQL server`

**Solution:**
- Ensure MySQL server is running
- Check credentials in `db_config.py`
- Verify database exists: `SHOW DATABASES;`

#### 2. Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install -r requirements.txt
```

#### 3. Login Failed

**Error:** User cannot login

**Solution:**
- Verify user exists in database:
  ```sql
  SELECT * FROM Login;
  ```
- Reset password using admin account
- Check User_Roles table for role assignment

#### 4. Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:**
```bash
# Kill existing Streamlit process or use different port
streamlit run app.py --server.port 8502
```

#### 5. Database Schema Errors

**Error:** Table doesn't exist

**Solution:**
```bash
# Re-run schema file
mysql -u root -p < schema.sql
```

---

## 🛠️ Development

### Adding New Features

1. **New Table** - Add to `schema.sql`
2. **New Page** - Create function in `app.py`
3. **New Role** - Update Roles table and modify `ROLE_EMOJIS`
4. **New Query** - Add to `database.py`

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and modular

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For issues, questions, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/bugsNburgers/Hotel-Management-System/issues)
- **Email**: support@hotelmanagement.com
- **Documentation**: See `CHANGES_SUMMARY.md` for recent updates

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Database powered by [MySQL](https://www.mysql.com/)
- Icons from emoji library

---

## 📊 Database Schema Overview

### Core Tables

- **Users** - User information (name, email, phone)
- **Login** - Authentication credentials
- **Roles** - System roles (admin, staff, customer)
- **User_Roles** - Role assignments
- **Hotels** - Hotel properties
- **Rooms** - Room inventory
- **Bookings** - Reservation records
- **Payments** - Payment transactions
- **Reviews** - Customer feedback

### Key Features

- Foreign key constraints for data integrity
- Indexed columns for performance
- Stored procedures for complex operations
- Sample data for testing

---

## 🎨 Screenshots

### Login Page
Clean and simple login interface with role-based authentication.

### Admin Dashboard
Comprehensive overview with user management, hotel management, and analytics.

### Staff Dashboard
Streamlined interface for managing daily operations and bookings.

### Customer Dashboard
User-friendly booking interface with hotel search and reservation management.

---

**Version:** 2.0 (Simplified 3-Role System)  
**Last Updated:** November 6, 2025  
**Maintainer:** bugsNburgers

---

Made with ❤️ for efficient hotel management
