-- seed.sql
USE hms;

-- users + login (admin)
INSERT INTO users (user_name, user_email, user_mobile, user_address)
VALUES ('Admin User', 'admin@pesu.edu', '9999999999', 'PES University');

INSERT INTO login (user_id, username, password_hash)
VALUES (LAST_INSERT_ID(), 'admin', SHA2('admin123',256));

-- roles and assign admin to role
INSERT INTO roles (role_name, role_desc) VALUES ('Admin', 'Full access'), ('Receptionist', 'Booking & customers');
INSERT INTO user_roles (user_id, role_id) VALUES (1, 1);

-- hotel
INSERT INTO hotels (hotel_name, hotel_type, hotel_desc, hotel_rent, manager_user_id)
VALUES ('PES Guesthouse', 'Guesthouse', 'For campus visitors', 0.00, 1);

-- rooms
INSERT INTO room (rno, type, price, vacancy) VALUES
(101, 'Single', 1000.00, 'Vacant'),
(102, 'Double', 1500.00, 'Vacant'),
(201, 'Single', 900.00, 'Vacant'),
(202, 'Deluxe', 2500.00, 'Vacant');

-- small sample customer (already checked out example)
INSERT INTO customer (name, proof, checkin, checkout, room, cost, status)
VALUES ('Test Customer','ID123','2025-09-01','2025-09-03',101,2000.00,'Checked Out');

-- sample booking + payment (for reports)
INSERT INTO booking (cust_id, hotel_id, book_date, book_type, book_desc)
VALUES (1, 1, CURDATE(), 'Guest Booking','Sample booking');

INSERT INTO payment (book_id, pay_date, pay_amt, pay_desc)
VALUES (1, CURDATE(), 500.00, 'Sample payment');
