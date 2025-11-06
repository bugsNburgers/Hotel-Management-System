# Hotel Management System - Simplified 3-Role System

## Summary of Changes

Successfully simplified the hotel management system to have only **3 roles**: `admin`, `staff`, and `customer`.

---

## ✅ Changes Made

### 1. **app.py** - Main Application
- ✅ Removed all staff subrole logic (receptionist, housekeeping, maintenance, chef, security, concierge, etc.)
- ✅ Removed manager role completely
- ✅ Simplified `ROLE_EMOJIS` to only include admin (🔧), staff (👔), and customer (🛎️)
- ✅ Updated staff login to accept users with 'staff' role from User_Roles table
- ✅ Removed `staff_roles` session variable (previously used for subroles)
- ✅ Simplified sidebar to show only main role
- ✅ Updated Admin panel:
  - User creation now offers only: admin, staff, customer
  - Staff Management tab simplified (no subroles)
  - Hotels tab no longer references "Manager ID"
- ✅ Replaced complex staff dashboard (with subrole-specific views) with simple generic staff dashboard
- ✅ Staff can now view bookings and perform basic operations

### 2. **schema.sql** - Database Schema
- ✅ Removed `Staff_Role` table (was used for subroles like receptionist, housekeeping, etc.)
- ✅ Removed `Staff_Role_Audit` table
- ✅ Removed `Staff_Performance` table
- ✅ Removed `Staff_Schedule` table
- ✅ Removed indexes related to Staff_Role tables
- ✅ Removed views: `vw_active_staff`, `vw_staff_role_summary`
- ✅ Removed stored procedures: `sp_assign_staff_role`, `sp_remove_staff_role`, `sp_staff_performance_report`
- ✅ Removed functions: `fn_count_staff_by_role`
- ✅ Removed triggers related to Staff_Role
- ✅ Updated sample data:
  - Roles now only: 'admin', 'staff', 'customer' (removed 'manager')
  - Staff user is assigned 'staff' role via User_Roles table
  - Removed Staff_Role table inserts for subroles

### 3. **fix_staff_user.py** - Staff User Setup Script
- ✅ Changed from assigning 'manager' role to 'staff' role
- ✅ Updated email from staff@gmail.com to staff@hotel.com (matching schema)

### 4. **auth.py** - No Changes Needed
- Already supports the 3-role system through User_Roles table

---

## 🎯 System Architecture

### Role Structure (Simplified)
```
┌─────────────────────────────────────┐
│         User Table                  │
│  - user_id                          │
│  - user_name                        │
│  - user_email                       │
└─────────────┬───────────────────────┘
              │
              ├──────────┐
              │          │
    ┌─────────▼────┐  ┌─▼───────────────────┐
    │ Login Table  │  │ User_Roles Table    │
    │ - username   │  │ - user_id           │
    │ - password   │  │ - role_id           │
    └──────────────┘  └─┬───────────────────┘
                        │
                  ┌─────▼──────────────────┐
                  │ Roles Table            │
                  │ - role_id              │
                  │ - role_name:           │
                  │   • admin              │
                  │   • staff              │
                  │   • customer           │
                  └────────────────────────┘
```

### Login Credentials (Default)

| Role     | Username/Email       | Password    |
|----------|---------------------|-------------|
| Admin    | admin               | adminpass   |
| Staff    | staff@hotel.com     | staffpass   |
| Customer | (register via UI)   | (your pass) |

---

## 🚀 How to Use

### 1. Reset Database (if needed)
```bash
mysql -u root -p < schema.sql
```

### 2. Run the Application
```bash
streamlit run app.py
```

### 3. Access Different Dashboards

**Admin Dashboard:**
- Full system control
- Manage users, staff, hotels, bookings
- View analytics and reports

**Staff Dashboard:**
- View recent bookings
- Quick actions for check-ins
- Simple operations interface

**Customer Dashboard:**
- Browse hotels
- Make bookings
- View booking history

---

## 📝 Key Features by Role

### Admin
- Create/manage system users
- Assign roles (admin/staff/customer)
- Manage staff members
- Add/edit hotels
- View all bookings
- Access revenue reports

### Staff
- View today's bookings
- Search guests
- Mark check-ins
- Basic booking operations

### Customer
- Browse available hotels
- Book rooms
- View booking history
- Manage profile

---

## ⚠️ Important Notes

1. **Manager role has been removed** - All hotel management is now done by admin
2. **No more staff subroles** - Staff have a generic role for managing bookings
3. **Simplified database** - Removed 4 tables related to staff subrole management
4. **Clean architecture** - Only 3 roles managed through standard User_Roles table

---

## 🔧 Technical Details

### Database Changes
- Removed 4 tables
- Removed 3 views
- Removed 3 stored procedures  
- Removed 2 functions
- Removed 2 triggers
- Simplified sample data

### Code Changes
- Simplified role checking logic
- Removed staff subrole dashboards
- Cleaner session management
- Updated UI for 3-role system

---

## ✨ Benefits of This Simplification

1. **Easier to maintain** - Less code, fewer tables
2. **Clearer permissions** - Only 3 distinct roles
3. **Simpler onboarding** - New staff don't need multiple role assignments
4. **Better performance** - Fewer joins, simpler queries
5. **Flexible** - Staff can be granted admin role if needed for advanced features

---

## 📧 Support

For any issues or questions, refer to the application's built-in help or contact the system administrator.

**System Version:** v2.0 (Simplified 3-Role System)
**Last Updated:** November 6, 2025
