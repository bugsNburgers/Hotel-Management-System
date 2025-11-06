# check_users.py
from database import fetch_all

try:
    users = fetch_all("""
        SELECT u.user_id, u.user_name, u.user_email, l.username, l.password
        FROM User u 
        LEFT JOIN Login l ON u.user_id = l.user_id
    """)
    
    print("\n=== SYSTEM USERS ===")
    for u in users:
        print(f"ID: {u['user_id']}")
        print(f"  Name: {u['user_name']}")
        print(f"  Email: {u['user_email']}")
        print(f"  Username: {u.get('username', 'N/A')}")
        pwd = u.get('password')
        if pwd:
            print(f"  Password: {pwd[:20]}...")
        else:
            print(f"  Password: None (No Login entry)")
        print()
        
    print("\n=== CUSTOMERS ===")
    customers = fetch_all("SELECT cust_id, cust_name, cust_email FROM Customer")
    for c in customers:
        print(f"ID: {c['cust_id']}, Name: {c['cust_name']}, Email: {c['cust_email']}")
        
except Exception as e:
    print(f"Error: {e}")
