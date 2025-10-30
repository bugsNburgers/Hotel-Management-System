DELIMITER $$
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
DELIMITER ;
-- Function: fn_get_booking_total
-- Returns total payments for a booking.
DELIMITER $$
CREATE FUNCTION fn_get_booking_total(bid INT) RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE total DECIMAL(10,2);
  SELECT COALESCE(SUM(pay_amt),0.00) INTO total FROM Payment WHERE book_id = bid;
  RETURN total;
END$$
DELIMITER ;
-- Trigger: trg_after_payment
-- Audit inserts into a Payment_Audit table (create audit table first)
CREATE TABLE IF NOT EXISTS Payment_Audit (
  audit_id INT AUTO_INCREMENT PRIMARY KEY,
  pay_id INT,
  book_id INT,
  pay_date DATE,
  pay_amt DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER trg_after_payment
AFTER INSERT ON Payment
FOR EACH ROW
BEGIN
  INSERT INTO Payment_Audit (pay_id, book_id, pay_date, pay_amt)
  VALUES (NEW.pay_id, NEW.book_id, NEW.pay_date, NEW.pay_amt);
END$$
DELIMITER ;

SELECT cust_id, cust_name FROM Customer
WHERE cust_id IN (
  SELECT b.cust_id FROM Booking b
  JOIN Payment p ON p.book_id = b.book_id
  GROUP BY b.cust_id
  HAVING SUM(p.pay_amt) > (
    SELECT AVG(total_spent) FROM (
      SELECT SUM(pay_amt) AS total_spent FROM Payment p2
      JOIN Booking b2 ON b2.book_id = p2.book_id
      GROUP BY b2.cust_id
    ) AS t
  )
);

SELECT b.book_id, c.cust_name, h.hotel_name, p.pay_amt, b.book_date
FROM Booking b
JOIN Customer c ON c.cust_id = b.cust_id
JOIN Hotel h ON h.hotel_id = b.hotel_id
LEFT JOIN Payment p ON p.book_id = b.book_id;
-- •	Aggregate query (revenue per hotel):
SELECT h.hotel_id, h.hotel_name, COALESCE(SUM(p.pay_amt),0) AS total_revenue
FROM Hotel h
LEFT JOIN Booking b ON b.hotel_id = h.hotel_id
LEFT JOIN Payment p ON p.book_id = b.book_id
GROUP BY h.hotel_id, h.hotel_name
ORDER BY total_revenue DESC;
