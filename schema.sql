-- ===============================================
-- HOTEL BOOKING SYSTEM - ENHANCED SQL SCHEMA
-- Base: Your Original Database + Upgrades for Streamlit Integration
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
-- 3️⃣ CUSTOMER & BOOKING MODULE
-- ==========================
CREATE TABLE Customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(120) NOT NULL,
    cust_email VARCHAR(150) UNIQUE,
    cust_mobile VARCHAR(20),
    cust_pass VARCHAR(255)
);

CREATE TABLE Booking (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT NOT NULL,
    hotel_id INT NOT NULL,
    book_date DATE NOT NULL,
    check_in DATE,
    check_out DATE,
    book_type VARCHAR(50),
    book_desc TEXT,
    booking_status ENUM('Pending','Confirmed','Cancelled') DEFAULT 'Confirmed',
    FOREIGN KEY (cust_id) REFERENCES Customer(cust_id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id) ON DELETE CASCADE
);

-- ==========================
-- 4️⃣ PAYMENT MODULE
-- ==========================
CREATE TABLE Payment (
    pay_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    pay_date DATE NOT NULL,
    pay_amt DECIMAL(10,2) NOT NULL,
    pay_method ENUM('Card','UPI','Cash','Online') DEFAULT 'Cash',
    pay_desc TEXT,
    FOREIGN KEY (book_id) REFERENCES Booking(book_id) ON DELETE CASCADE
);

-- ==========================
-- 5️⃣ AUDIT MODULE
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
-- 6️⃣ PROCEDURE + FUNCTION + TRIGGER
-- ==========================

DELIMITER $$

-- PROCEDURE: BOOKING
CREATE PROCEDURE sp_make_booking(
    IN p_cust_id INT,
    IN p_hotel_id INT,
    IN p_book_date DATE,
    IN p_book_type VARCHAR(50),
    IN p_book_desc TEXT,
    IN p_pay_amt DECIMAL(10,2)
)
BEGIN
    DECLARE last_book_id INT;
    START TRANSACTION;
    INSERT INTO Booking (cust_id, hotel_id, book_date, book_type, book_desc)
    VALUES (p_cust_id, p_hotel_id, p_book_date, p_book_type, p_book_desc);
    
    SET last_book_id = LAST_INSERT_ID();
    
    IF p_pay_amt > 0 THEN
        INSERT INTO Payment (book_id, pay_date, pay_amt, pay_desc)
        VALUES (last_book_id, p_book_date, p_pay_amt, CONCAT('Auto payment for booking ', last_book_id));
    END IF;
    
    COMMIT;
    SELECT last_book_id AS booking_id;
END$$

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
-- 7️⃣ SAMPLE DATA
-- ==========================
INSERT INTO Roles (role_name, role_desc) VALUES
('admin','System administrator'),
('manager','Hotel manager'),
('customer','Registered user');

INSERT INTO User (user_name, user_email, user_mobile, user_address)
VALUES ('Admin User','admin@example.com','9999999999','PES University');

INSERT INTO Login (user_id, username, password)
VALUES (1,'admin','adminpass');

INSERT INTO Hotel (hotel_name, hotel_type, hotel_desc, user_id)
VALUES ('Sunrise Hotel','3-star','Comfortable midrange hotel',1);

INSERT INTO Hotel_Class (hotel_id, class_name, class_rent, room_count)
VALUES (1, 'Standard', 2500.00, 10),
       (1, 'Deluxe', 3500.00, 5),
       (1, 'Suite', 5000.00, 2);

INSERT INTO Customer (cust_name, cust_email, cust_mobile, cust_pass)
VALUES ('John Doe','johndoe@example.com','8888888888','secret');

INSERT INTO Booking (cust_id, hotel_id, book_date, book_type, book_desc)
VALUES (1,1,CURDATE(),'single','One-night booking');

INSERT INTO Payment (book_id, pay_date, pay_amt, pay_desc)
VALUES (1,CURDATE(),2500.00,'Payment for one night');

-- ==========================
-- 8️⃣ USEFUL QUERIES
-- ==========================

-- Top customers by spending
SELECT cust_id, cust_name
FROM Customer
WHERE cust_id IN (
  SELECT b.cust_id
  FROM Booking b
  JOIN Payment p ON p.book_id = b.book_id
  GROUP BY b.cust_id
  HAVING SUM(p.pay_amt) > (
    SELECT AVG(total_spent)
    FROM (
      SELECT SUM(pay_amt) AS total_spent
      FROM Payment p2
      JOIN Booking b2 ON b2.book_id = p2.book_id
      GROUP BY b2.cust_id
    ) AS t
  )
);

-- Revenue per hotel
SELECT h.hotel_id, h.hotel_name,
       COALESCE(SUM(p.pay_amt),0) AS total_revenue
FROM Hotel h
LEFT JOIN Booking b ON b.hotel_id = h.hotel_id
LEFT JOIN Payment p ON p.book_id = b.book_id
GROUP BY h.hotel_id, h.hotel_name
ORDER BY total_revenue DESC;
