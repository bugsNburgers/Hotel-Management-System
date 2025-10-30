import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='MySQL@123', database='hotel_booking')
cursor = conn.cursor()

# Insert User_Roles for admin user (user_id=1, role_id=1 for admin)
cursor.execute('INSERT IGNORE INTO User_Roles (user_id, role_id) VALUES (1, 1)')

conn.commit()
cursor.close()
conn.close()
print('User_Roles inserted for admin')
