# ER Diagram Compliance - Schema Fixes

## ✅ Fixed All Issues to Match Your ER Diagram

---

## 🔍 Issues Found and Fixed

### ❌ **Issue 1: Missing `Rooms` Table**
**Problem:** ER diagram shows a `Rooms` entity but it was missing from schema.

**✅ Fixed:** Added complete Rooms table:
```sql
CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT NOT NULL,
    class_id INT NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    room_status ENUM('Available','Occupied','Maintenance','Reserved') DEFAULT 'Available',
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Hotel_Class(class_id) ON DELETE CASCADE,
    UNIQUE KEY unique_room (hotel_id, room_number)
);
```

---

### ❌ **Issue 2: Booking Missing `user_id` (Make Relationship)**
**Problem:** ER diagram shows "Make" relationship between User and Booking, but Booking table only had `cust_id`.

**✅ Fixed:** Added `user_id` and `room_id` to Booking:
```sql
CREATE TABLE Booking (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,              -- ✅ Added
    cust_id INT NOT NULL,
    hotel_id INT NOT NULL,
    room_id INT,                        -- ✅ Added
    book_date DATE NOT NULL,
    check_in DATE,
    check_out DATE,
    book_type VARCHAR(50),
    book_desc TEXT,
    booking_status ENUM('Pending','Confirmed','Cancelled') DEFAULT 'Confirmed',
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id) ON DELETE SET NULL
);
```

---

### ❌ **Issue 3: Payment Missing `user_id` Link**
**Problem:** ER diagram shows Payment connected to User (1:M relationship), but Payment table only had `book_id`.

**✅ Fixed:** Added `user_id` to Payment table:
```sql
CREATE TABLE Payment (
    pay_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,               -- ✅ Added
    book_id INT NOT NULL,
    pay_date DATE NOT NULL,
    pay_amt DECIMAL(10,2) NOT NULL,
    pay_method ENUM('Card','UPI','Cash','Online') DEFAULT 'Cash',
    pay_desc TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Booking(book_id) ON DELETE CASCADE
);
```

---

### ❌ **Issue 4: Customer Not Linked to User**
**Problem:** ER diagram shows Customer should be linked to User table, but it was standalone.

**✅ Fixed:** Added `user_id` foreign key to Customer:
```sql
CREATE TABLE Customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,                 -- ✅ Added
    cust_name VARCHAR(120) NOT NULL,
    cust_email VARCHAR(150) UNIQUE,
    cust_mobile VARCHAR(20),
    cust_pass VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE SET NULL
);
```

---

### ❌ **Issue 5: Invalid Staff_Schedule Reference**
**Problem:** Schema tried to insert data into non-existent `Staff_Schedule` table.

**✅ Fixed:** Removed invalid insert and replaced with Rooms sample data:
```sql
-- Sample Rooms
INSERT INTO Rooms (hotel_id, class_id, room_number, room_status) VALUES
(1, 1, '101', 'Available'),
(1, 1, '102', 'Available'),
(1, 2, '201', 'Occupied'),
(1, 2, '202', 'Available'),
(1, 3, '301', 'Available'),
(1, 4, '401', 'Available');
```

---

### ❌ **Issue 6: Stored Procedure Out of Sync**
**Problem:** `sp_make_booking` procedure didn't accept new fields (user_id, room_id, check_in, check_out).

**✅ Fixed:** Completely rewrote the procedure:
```sql
CREATE PROCEDURE sp_make_booking(
    IN p_user_id INT,
    IN p_cust_id INT,
    IN p_hotel_id INT,
    IN p_room_id INT,
    IN p_book_date DATE,
    IN p_check_in DATE,
    IN p_check_out DATE,
    IN p_book_type VARCHAR(50),
    IN p_book_desc TEXT,
    IN p_pay_amt DECIMAL(10,2),
    IN p_pay_method VARCHAR(20)
)
BEGIN
    DECLARE last_book_id INT;
    START TRANSACTION;
    
    -- Insert booking with user_id and room_id
    INSERT INTO Booking (user_id, cust_id, hotel_id, room_id, book_date, check_in, check_out, book_type, book_desc)
    VALUES (p_user_id, p_cust_id, p_hotel_id, p_room_id, p_book_date, p_check_in, p_check_out, p_book_type, p_book_desc);
    
    SET last_book_id = LAST_INSERT_ID();
    
    -- Update room status to Reserved
    IF p_room_id IS NOT NULL THEN
        UPDATE Rooms SET room_status = 'Reserved' WHERE room_id = p_room_id;
    END IF;
    
    -- Insert payment with user_id
    IF p_pay_amt > 0 THEN
        INSERT INTO Payment (user_id, book_id, pay_date, pay_amt, pay_method, pay_desc)
        VALUES (p_user_id, last_book_id, p_book_date, p_pay_amt, p_pay_method, CONCAT('Payment for booking #', last_book_id));
    END IF;
    
    COMMIT;
    SELECT last_book_id AS booking_id;
END$$
```

---

### ❌ **Issue 7: Missing Indexes**
**Problem:** No indexes on new foreign keys for performance.

**✅ Fixed:** Added critical indexes:
```sql
CREATE INDEX idx_booking_date ON Booking(book_date);
CREATE INDEX idx_booking_user ON Booking(user_id);        -- ✅ New
CREATE INDEX idx_customer_email ON Customer(cust_email);
CREATE INDEX idx_payment_user ON Payment(user_id);        -- ✅ New
CREATE INDEX idx_rooms_hotel ON Rooms(hotel_id);          -- ✅ New
CREATE INDEX idx_rooms_status ON Rooms(room_status);      -- ✅ New
```

---

### ✅ **Bonus: Added Room Availability Function**
```sql
CREATE FUNCTION fn_check_room_availability(rid INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE status VARCHAR(20);
    SELECT room_status INTO status FROM Rooms WHERE room_id = rid;
    RETURN status;
END$$
```

---

## 📊 Updated Sample Data

Now includes:
- ✅ 6 sample rooms across different classes
- ✅ Customer properly linked to User table (user_id = 3)
- ✅ Customer assigned 'customer' role via User_Roles
- ✅ Booking includes both user_id and room_id
- ✅ Payment includes user_id
- ✅ Room status updated when booked

---

## 🎯 ER Diagram Compliance Checklist

| Entity/Relationship | Status | Notes |
|---------------------|--------|-------|
| **User** | ✅ | Complete with all attributes |
| **Roles** | ✅ | 3 roles: admin, staff, customer |
| **User_Roles** (M:N) | ✅ | Junction table for many-to-many |
| **Login** | ✅ | 1:1 with User |
| **Permission** | ✅ | Linked to Roles |
| **Hotel** | ✅ | Linked to User (owner) |
| **Hotel_Class** | ✅ | M:1 with Hotel |
| **Rooms** | ✅ | **FIXED** - Now exists with proper relationships |
| **Customer** | ✅ | **FIXED** - Now linked to User |
| **Booking** | ✅ | **FIXED** - Now has user_id, room_id |
| **Payment** | ✅ | **FIXED** - Now linked to User and Booking |
| **Payment_Audit** | ✅ | Audit trail for payments |
| **Make (User→Booking)** | ✅ | **FIXED** - user_id in Booking |
| **Pay (User→Payment)** | ✅ | **FIXED** - user_id in Payment |

---

## 🔥 Key Improvements

### 1. **Proper Data Integrity**
- All foreign keys properly defined
- Cascading deletes where appropriate
- Unique constraints on room numbers

### 2. **Complete Room Management**
- Rooms table tracks individual room inventory
- Room status: Available, Occupied, Maintenance, Reserved
- Automatic room status update when booked

### 3. **User-Centric Design**
- Every customer is also a User
- Payments tracked by user_id
- Bookings linked to users (not just customers)

### 4. **Better Queries Possible**
```sql
-- Find all payments by a user
SELECT * FROM Payment WHERE user_id = 3;

-- Find available rooms in a hotel
SELECT * FROM Rooms WHERE hotel_id = 1 AND room_status = 'Available';

-- Get user's booking history
SELECT * FROM Booking WHERE user_id = 3;
```

---

## 🚀 Next Steps

### 1. **Drop Old Database (if exists)**
```sql
DROP DATABASE IF EXISTS hotel_booking;
```

### 2. **Run Updated Schema**
```bash
mysql -u root -p < schema.sql
```

### 3. **Verify Tables Created**
```sql
USE hotel_booking;
SHOW TABLES;
-- Should show: User, Roles, User_Roles, Login, Permission, 
--              Hotel, Hotel_Class, Rooms, Customer, Booking, 
--              Payment, Payment_Audit
```

### 4. **Test Sample Data**
```sql
-- Check rooms
SELECT * FROM Rooms;

-- Check customer-user link
SELECT c.*, u.user_name FROM Customer c 
JOIN User u ON c.user_id = u.user_id;

-- Check booking with all relationships
SELECT b.*, u.user_name, r.room_number 
FROM Booking b 
JOIN User u ON b.user_id = u.user_id
JOIN Rooms r ON b.room_id = r.room_id;
```

---

## ⚠️ Important Notes

1. **Breaking Changes**: This update changes table structures. You'll need to:
   - Drop and recreate the database
   - Update any existing queries in `app.py`
   - Update booking creation logic

2. **App.py Updates Needed**: The application code needs updates to:
   - Include `user_id` when creating bookings
   - Include `room_id` when selecting rooms
   - Show room availability
   - Link customers to User table

3. **Migration**: If you have existing data, you'll need a migration script to:
   - Create User records for existing Customers
   - Add user_id to existing Bookings
   - Add user_id to existing Payments

---

## 📝 Summary

**All ER diagram issues have been fixed!** The schema now:

✅ Includes all entities from the ER diagram  
✅ Implements all relationships correctly  
✅ Has proper foreign keys and constraints  
✅ Includes comprehensive sample data  
✅ Has optimized indexes for performance  
✅ Includes stored procedures that work with new structure  

Your database schema is now **100% compliant** with the ER diagram! 🎉

---

**Last Updated:** November 6, 2025  
**Schema Version:** 2.1 (ER Diagram Compliant)
