-- schema.sql
-- Drop and recreate DB for a clean start
DROP DATABASE IF EXISTS hms;
CREATE DATABASE hms;
USE hms;

-- ========== Audit / Helper tables ==========
CREATE TABLE audit_logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  event_type VARCHAR(60),
  event_desc TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ========== users & auth & roles ==========
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(100) NOT NULL,
  user_email VARCHAR(150),
  user_mobile VARCHAR(20),
  user_address TEXT
);

CREATE TABLE login (
  login_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  username VARCHAR(80) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE roles (
  role_id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(80) UNIQUE NOT NULL,
  role_desc TEXT
);

CREATE TABLE user_roles (
  ur_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
  UNIQUE KEY (user_role_unique) (user_id, role_id)
);

-- ========== hotels, rooms, customer, booking, payment ==========
CREATE TABLE hotels (
  hotel_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_name VARCHAR(150) NOT NULL,
  hotel_type VARCHAR(80),
  hotel_desc TEXT,
  hotel_rent DECIMAL(10,2) DEFAULT 0.00,
  manager_user_id INT,
  FOREIGN KEY (manager_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE room (
  rno INT PRIMARY KEY,                      -- room number
  type VARCHAR(80),
  price DECIMAL(10,2) NOT NULL,
  vacancy ENUM('Vacant','Occupied') DEFAULT 'Vacant'
);

CREATE TABLE customer (
  cid INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  proof VARCHAR(200),
  checkin DATE,
  checkout DATE,
  room INT,
  cost DECIMAL(10,2) DEFAULT 0,
  status ENUM('Checked In','Checked Out') DEFAULT 'Checked In',
  FOREIGN KEY (room) REFERENCES room(rno) ON DELETE SET NULL
);

CREATE TABLE booking (
  book_id INT AUTO_INCREMENT PRIMARY KEY,
  cust_id INT,
  hotel_id INT,
  book_date DATE,
  book_type VARCHAR(100),
  book_desc TEXT,
  FOREIGN KEY (cust_id) REFERENCES customer(cid) ON DELETE SET NULL,
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE SET NULL
);

CREATE TABLE payment (
  pay_id INT AUTO_INCREMENT PRIMARY KEY,
  book_id INT,
  pay_date DATE,
  pay_amt DECIMAL(10,2),
  pay_desc TEXT,
  FOREIGN KEY (book_id) REFERENCES booking(book_id) ON DELETE CASCADE
);

-- Indexes to speed queries used by reports
CREATE INDEX idx_room_vacancy ON room(vacancy);
CREATE INDEX idx_customer_status ON customer(status);
CREATE INDEX idx_booking_date ON booking(book_date);
CREATE INDEX idx_payment_date ON payment(pay_date);

-- ========== FUNCTIONS / PROCEDURES ==========
DELIMITER $$

-- cost function: nights * price
CREATE FUNCTION fn_cost(nights INT, unit_price DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  RETURN nights * unit_price;
END$$

-- Procedure: Add customer (transactional)
-- Returns a single-row resultset with out_cid (positive ID) or negative code for error
CREATE PROCEDURE proc_add_customer(
  IN p_name VARCHAR(150),
  IN p_proof VARCHAR(200),
  IN p_checkin DATE,
  IN p_checkout DATE,
  IN p_rno INT
)
BEGIN
  DECLARE room_price DECIMAL(10,2);
  DECLARE room_vacancy VARCHAR(20);
  DECLARE nights INT;
  DECLARE total_cost DECIMAL(10,2);
  DECLARE out_cid INT DEFAULT 0;

  START TRANSACTION;

  -- Lock the room row to prevent race conditions
  SELECT price, vacancy INTO room_price, room_vacancy FROM room WHERE rno = p_rno FOR UPDATE;

  IF room_price IS NULL THEN
    SET out_cid = -1; -- room not found
    ROLLBACK;
    SELECT out_cid AS result;
    LEAVE proc_add_customer;
  END IF;

  IF room_vacancy <> 'Vacant' THEN
    SET out_cid = -2; -- occupied
    ROLLBACK;
    SELECT out_cid AS result;
    LEAVE proc_add_customer;
  END IF;

  SET nights = DATEDIFF(p_checkout, p_checkin);
  IF nights < 0 THEN
    SET out_cid = -3; -- invalid dates
    ROLLBACK;
    SELECT out_cid AS result;
    LEAVE proc_add_customer;
  END IF;

  SET total_cost = fn_cost(nights, room_price);

  INSERT INTO customer (name, proof, checkin, checkout, room, cost, status)
    VALUES (p_name, p_proof, p_checkin, p_checkout, p_rno, total_cost, 'Checked In');

  SET out_cid = LAST_INSERT_ID();

  UPDATE room SET vacancy = 'Occupied' WHERE rno = p_rno;

  INSERT INTO audit_logs (event_type, event_desc)
    VALUES ('CHECKIN', CONCAT('CID=', out_cid, ' Name=', p_name, ' Room=', p_rno, ' Cost=', total_cost));

  COMMIT;

  SELECT out_cid AS result;
END$$

-- Procedure: Create booking and payment atomically, return book_id (>0) or negative error
CREATE PROCEDURE proc_create_booking_with_payment(
  IN p_cust_id INT,
  IN p_hotel_id INT,
  IN p_type VARCHAR(100),
  IN p_desc TEXT,
  IN p_pay_amt DECIMAL(10,2)
)
BEGIN
  DECLARE out_book_id INT DEFAULT 0;

  START TRANSACTION;

  INSERT INTO booking (cust_id, hotel_id, book_date, book_type, book_desc)
    VALUES (p_cust_id, p_hotel_id, CURDATE(), p_type, p_desc);
  SET out_book_id = LAST_INSERT_ID();

  INSERT INTO payment (book_id, pay_date, pay_amt, pay_desc)
    VALUES (out_book_id, CURDATE(), p_pay_amt, CONCAT('Payment for booking ', out_book_id));

  INSERT INTO audit_logs (event_type, event_desc)
    VALUES ('BOOKPAY', CONCAT('BOOK=', out_book_id, ' CUST=', p_cust_id, ' AMT=', p_pay_amt));

  COMMIT;
  SELECT out_book_id AS result;
END$$

DELIMITER ;

-- ========== TRIGGERS ==========
DELIMITER $$

-- When customer status is updated to Checked Out, set room vacancy to Vacant
CREATE TRIGGER tr_customer_status_after_update
AFTER UPDATE ON customer
FOR EACH ROW
BEGIN
  IF OLD.status <> NEW.status AND NEW.status = 'Checked Out' THEN
    IF NEW.room IS NOT NULL THEN
      UPDATE room SET vacancy = 'Vacant' WHERE rno = NEW.room;
      INSERT INTO audit_logs (event_type, event_desc)
        VALUES ('CHECKOUT', CONCAT('CID=', NEW.cid, ' Room=', NEW.room));
    END IF;
  END IF;
END$$

-- When a new payment is inserted, insert a log
CREATE TRIGGER tr_payment_after_insert
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs (event_type, event_desc)
    VALUES ('PAYMENT', CONCAT('PAYID=', NEW.pay_id, ' BOOK=', NEW.book_id, ' AMT=', NEW.pay_amt));
END$$

-- When a room row is deleted, log it
CREATE TRIGGER tr_room_after_delete
AFTER DELETE ON room
FOR EACH ROW
BEGIN
  INSERT INTO audit_logs (event_type, event_desc)
    VALUES ('ROOM_DELETE', CONCAT('RNO=', OLD.rno, ' TYPE=', OLD.type));
END$$

DELIMITER ;

-- Done with DDL
