import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='MySQL@123', database='hotel_booking')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Hotel_Class')
cursor.execute('''CREATE TABLE Hotel_Class (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    class_rent DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id) ON DELETE CASCADE
)''')

cursor.execute('''INSERT INTO Hotel_Class (hotel_id, class_name, class_rent) VALUES
    (1, 'Standard', 2500.00),
    (1, 'Deluxe', 3500.00),
    (1, 'Suite', 5000.00)''')

conn.commit()
cursor.close()
conn.close()
print('Hotel_Class table created and populated')
