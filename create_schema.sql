CREATE DATABASE IF NOT EXISTS hotel_booking;
USE hotel_booking;

-- Users
CREATE TABLE `User` (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  user_name VARCHAR(100) NOT NULL,
  user_email VARCHAR(150) UNIQUE NOT NULL,
  user_mobile VARCHAR(20),
  user_address TEXT
);

CREATE TABLE `Login` (
  login_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  username VARCHAR(80) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES `User`(user_id) ON DELETE CASCADE
);

-- Roles & permissions
CREATE TABLE `Roles` (
  role_id INT AUTO_INCREMENT PRIMARY KEY,
  role_name VARCHAR(50) NOT NULL UNIQUE,
  role_desc TEXT
);

CREATE TABLE `User_Roles` (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES `User`(user_id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES `Roles`(role_id) ON DELETE CASCADE
);

CREATE TABLE `Permission` (
  perm_id INT AUTO_INCREMENT PRIMARY KEY,
  perm_name VARCHAR(100) NOT NULL,
  perm_module VARCHAR(100),
  role_id INT,
  FOREIGN KEY (role_id) REFERENCES `Roles`(role_id) ON DELETE SET NULL
);

-- Hotel
CREATE TABLE `Hotel` (
  hotel_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_name VARCHAR(150) NOT NULL,
  hotel_type VARCHAR(50),
  hotel_desc TEXT,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES `User`(user_id) ON DELETE SET NULL
);

-- Hotel Classes (e.g., 3-star, 5-star under same hotel)
CREATE TABLE `Hotel_Class` (
  class_id INT AUTO_INCREMENT PRIMARY KEY,
  hotel_id INT NOT NULL,
  class_name VARCHAR(50) NOT NULL,
  class_rent DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (hotel_id) REFERENCES `Hotel`(hotel_id) ON DELETE CASCADE
);

-- Customer
CREATE TABLE `Customer` (
  cust_id INT AUTO_INCREMENT PRIMARY KEY,
  cust_name VARCHAR(120) NOT NULL,
  cust_email VARCHAR(150) UNIQUE,
  cust_mobile VARCHAR(20),
  cust_pass VARCHAR(255)
);

-- Booking
CREATE TABLE `Booking` (
  book_id INT AUTO_INCREMENT PRIMARY KEY,
  cust_id INT NOT NULL,
  hotel_id INT NOT NULL,
  book_date DATE NOT NULL,
  book_type VARCHAR(50),
  book_desc TEXT,
  FOREIGN KEY (cust_id) REFERENCES `Customer`(cust_id) ON DELETE CASCADE,
  FOREIGN KEY (hotel_id) REFERENCES `Hotel`(hotel_id) ON DELETE CASCADE
);

-- Payment
CREATE TABLE `Payment` (
  pay_id INT AUTO_INCREMENT PRIMARY KEY,
  book_id INT NOT NULL,
  pay_date DATE NOT NULL,
  pay_amt DECIMAL(10,2) NOT NULL,
  pay_desc TEXT,
  FOREIGN KEY (book_id) REFERENCES `Booking`(book_id) ON DELETE CASCADE
);

INSERT INTO `Roles` (role_name, role_desc) VALUES
('admin','System administrator'),
('manager','Hotel manager');

INSERT INTO `User` (user_name, user_email, user_mobile, user_address)
VALUES ('Admin User','admin@example.com','9999999999','PES University');

INSERT INTO `Login` (user_id, username, password)
VALUES (1,'admin','adminpass'); 

INSERT INTO `Hotel` (hotel_name, hotel_type, hotel_desc, user_id)
VALUES ('Sunrise Hotel','3-star','Comfortable midrange hotel',1);

INSERT INTO `Hotel_Class` (hotel_id, class_name, class_rent)
VALUES (1, 'Standard', 2500.00), (1, 'Deluxe', 3500.00), (1, 'Suite', 5000.00);

INSERT INTO `Customer` (cust_name, cust_email, cust_mobile, cust_pass)
VALUES ('John Doe','johndoe@example.com','8888888888','secret');

INSERT INTO `Booking` (cust_id, hotel_id, book_date, book_type, book_desc)
VALUES (1,1,CURDATE(),'single','One-night booking');

INSERT INTO `Payment` (book_id, pay_date, pay_amt, pay_desc)
VALUES (1,CURDATE(),2500.00,'Payment for one night');
