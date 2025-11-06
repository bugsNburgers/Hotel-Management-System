-- ===============================================
-- HOTEL BOOKING SYSTEM - ENHANCED SQL SCHEMA
-- With Staff Management Module
-- ===============================================

CREATE DATABASE IF NOT EXISTS hotel_booking;
USE hotel_booking;

-- ==========================
-- 1️⃣ USER & LOGIN MODULE
-- ==========================
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(150) UNIQUE NOT NULL,
    user_mobile VARCHAR(20),
    user_address TEXT
);

CREATE TABLE Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_desc TEXT
);

CREATE TABLE User_Roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE CASCADE
);

CREATE TABLE Login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Permission (
    perm_id INT AUTO_INCREMENT PRIMARY KEY,
    perm_name VARCHAR(100) NOT NULL,
    perm_module VARCHAR(100),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE SET NULL
);

-- ==========================
-- 2️⃣ HOTEL MODULE
-- ==========================
CREATE TABLE Hotel (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name VARCHAR(150) NOT NULL,
    hotel_type VARCHAR(50),
    hotel_desc TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE SET NULL
);

CREATE TABLE Hotel_Class (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    class_rent DECIMAL(10,2) NOT NULL,
    room_count INT DEFAULT 0,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id) ON DELETE CASCADE
);

-- ==========================
-- 3️⃣ ROOMS MODULE
-- ==========================
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

-- ==========================
-- 4️⃣ CUSTOMER & BOOKING MODULE
-- ==========================
CREATE TABLE Customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    cust_name VARCHAR(120) NOT NULL,
    cust_email VARCHAR(150) UNIQUE,
    cust_mobile VARCHAR(20),
    cust_pass VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE SET NULL
);

CREATE TABLE Booking (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    cust_id INT NOT NULL,
    hotel_id INT NOT NULL,
    room_id INT,
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

-- ==========================
-- 5️⃣ PAYMENT MODULE
-- ==========================
CREATE TABLE Payment (
    pay_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    pay_date DATE NOT NULL,
    pay_amt DECIMAL(10,2) NOT NULL,
    pay_method ENUM('Card','UPI','Cash','Online') DEFAULT 'Cash',
    pay_desc TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Booking(book_id) ON DELETE CASCADE
);

-- ==========================
-- 6️⃣ AUDIT MODULE
-- ==========================
CREATE TABLE IF NOT EXISTS Payment_Audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    pay_id INT,
    book_id INT,
    pay_date DATE,
    pay_amt DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- 6️⃣ INDEXES FOR PERFORMANCE
-- ==========================
CREATE INDEX idx_booking_date ON Booking(book_date);
CREATE INDEX idx_booking_user ON Booking(user_id);
CREATE INDEX idx_customer_email ON Customer(cust_email);
CREATE INDEX idx_payment_user ON Payment(user_id);
CREATE INDEX idx_rooms_hotel ON Rooms(hotel_id);
CREATE INDEX idx_rooms_status ON Rooms(room_status);

-- ==========================
-- 7️⃣ VIEWS
-- ==========================

-- View: Hotel Revenue Summary
CREATE OR REPLACE VIEW vw_hotel_revenue AS
SELECT 
    h.hotel_id,
    h.hotel_name,
    h.hotel_type,
    COUNT(DISTINCT b.book_id) as total_bookings,
    COALESCE(SUM(p.pay_amt), 0) as total_revenue,
    AVG(p.pay_amt) as avg_payment
FROM Hotel h
LEFT JOIN Booking b ON h.hotel_id = b.hotel_id
LEFT JOIN Payment p ON b.book_id = p.book_id
GROUP BY h.hotel_id, h.hotel_name, h.hotel_type;

-- ==========================
-- 9️⃣ STORED PROCEDURES
-- ==========================

DELIMITER $$

-- PROCEDURE: BOOKING
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

-- ==========================
-- 9️⃣ FUNCTIONS
-- ==========================

-- FUNCTION: Total payments for a booking
CREATE FUNCTION fn_get_booking_total(bid INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT COALESCE(SUM(pay_amt),0.00) INTO total
    FROM Payment WHERE book_id = bid;
    RETURN total;
END$$

-- FUNCTION: Check room availability
CREATE FUNCTION fn_check_room_availability(rid INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE status VARCHAR(20);
    SELECT room_status INTO status FROM Rooms WHERE room_id = rid;
    RETURN status;
END$$

-- ==========================
-- 🔟 TRIGGERS
-- ==========================

-- TRIGGER: Auto-insert into Payment_Audit
CREATE TRIGGER trg_after_payment
AFTER INSERT ON Payment
FOR EACH ROW
BEGIN
    INSERT INTO Payment_Audit (pay_id, book_id, pay_date, pay_amt)
    VALUES (NEW.pay_id, NEW.book_id, NEW.pay_date, NEW.pay_amt);
END$$

DELIMITER ;

-- ==========================
-- 1️⃣1️⃣ SAMPLE DATA
-- ==========================

-- Base Roles (only 3 roles)
INSERT INTO Roles (role_name, role_desc) VALUES
('admin','System administrator with full access'),
('staff','Hotel staff managing bookings and operations'),
('customer','Registered customer user');

-- Admin User
INSERT INTO User (user_name, user_email, user_mobile, user_address)
VALUES ('Admin User','admin@example.com','9999999999','PES University, Bangalore');

INSERT INTO Login (user_id, username, password)
VALUES (1,'admin','adminpass');

INSERT INTO User_Roles (user_id, role_id)
VALUES (1, 1); -- Admin role

-- Sample Staff Member
INSERT INTO User (user_name, user_email, user_mobile, user_address)
VALUES ('John Smith','staff@hotel.com','8888888888','Staff Quarters, Hotel');

INSERT INTO Login (user_id, username, password)
VALUES (2,'staff','staffpass');

-- Assign staff role (role_id 2 = staff)
INSERT INTO User_Roles (user_id, role_id)
VALUES (2, 2);

-- Sample Hotel (no manager assignment)
INSERT INTO Hotel (hotel_name, hotel_type, hotel_desc, user_id)
VALUES ('Grand Sunrise Hotel','5-Star Luxury','Premium luxury hotel with world-class amenities', NULL);

INSERT INTO Hotel_Class (hotel_id, class_name, class_rent, room_count) VALUES
(1, 'Standard Room', 2500.00, 10),
(1, 'Deluxe Room', 3500.00, 8),
(1, 'Executive Suite', 5000.00, 5),
(1, 'Presidential Suite', 10000.00, 2);

-- Sample Customer (linked to User)
INSERT INTO User (user_name, user_email, user_mobile, user_address)
VALUES ('Jane Doe','jane.doe@example.com','7777777777','Bangalore, India');

INSERT INTO Customer (user_id, cust_name, cust_email, cust_mobile, cust_pass)
VALUES (3, 'Jane Doe','jane.doe@example.com','7777777777','customerpass');

INSERT INTO User_Roles (user_id, role_id)
VALUES (3, 3); -- Customer role

-- Sample Booking (now includes user_id and room_id)
INSERT INTO Booking (user_id, cust_id, hotel_id, room_id, book_date, check_in, check_out, book_type, book_desc)
VALUES (3, 1, 1, 3, CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'double', 'Honeymoon package');

-- Sample Payment (now includes user_id)
INSERT INTO Payment (user_id, book_id, pay_date, pay_amt, pay_method, pay_desc)
VALUES (3, 1, CURDATE(), 7000.00, 'Card', 'Payment for 2 nights - Deluxe Room');

-- Sample Rooms
INSERT INTO Rooms (hotel_id, class_id, room_number, room_status) VALUES
(1, 1, '101', 'Available'),
(1, 1, '102', 'Available'),
(1, 2, '201', 'Occupied'),
(1, 2, '202', 'Available'),
(1, 3, '301', 'Available'),
(1, 4, '401', 'Available');

-- ==========================
-- 1️⃣3️⃣ USEFUL QUERIES
-- ==========================

-- Top customers by spending
SELECT 
    c.cust_id, 
    c.cust_name,
    c.cust_email,
    COUNT(b.book_id) as total_bookings,
    SUM(p.pay_amt) as total_spent
FROM Customer c
JOIN Booking b ON c.cust_id = b.cust_id
JOIN Payment p ON b.book_id = p.book_id
GROUP BY c.cust_id, c.cust_name, c.cust_email
HAVING total_spent > (
    SELECT AVG(customer_total)
    FROM (
        SELECT SUM(p2.pay_amt) as customer_total
        FROM Payment p2
        JOIN Booking b2 ON b2.book_id = p2.book_id
        GROUP BY b2.cust_id
    ) AS avg_calc
)
ORDER BY total_spent DESC;

-- Revenue per hotel
SELECT 
    h.hotel_id, 
    h.hotel_name,
    h.hotel_type,
    COUNT(DISTINCT b.book_id) as total_bookings,
    COALESCE(SUM(p.pay_amt), 0) AS total_revenue,
    AVG(p.pay_amt) as avg_booking_value
FROM Hotel h
LEFT JOIN Booking b ON b.hotel_id = h.hotel_id
LEFT JOIN Payment p ON p.book_id = b.book_id
GROUP BY h.hotel_id, h.hotel_name, h.hotel_type
ORDER BY total_revenue DESC;

-- ==========================
-- END OF SCHEMA
-- ==========================