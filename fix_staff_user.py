# fix_staff_user.py
from database import execute, fetch_one
from auth import hash_pass

# Check if staff user exists
staff_user = fetch_one("SELECT * FROM User WHERE user_email = %s", ('staff@hotel.com',))

if not staff_user:
    # Create staff user with email staff@hotel.com
    print("Creating staff user...")
    user_id = execute(
        "INSERT INTO User (user_name, user_email, user_mobile, user_address) VALUES (%s,%s,%s,%s)",
        ('Staff Member', 'staff@hotel.com', '8888888888', 'Staff Quarters')
    )
    print(f"Created user ID: {user_id}")
else:
    user_id = staff_user['user_id']
    print(f"Staff user exists with ID: {user_id}")

# Check if Login entry exists
login_entry = fetch_one("SELECT * FROM Login WHERE user_id = %s", (user_id,))

if not login_entry:
    # Create Login entry with hashed password
    print("Creating Login entry...")
    hashed_pw = hash_pass('staffpass')
    execute(
        "INSERT INTO Login (user_id, username, password) VALUES (%s,%s,%s)",
        (user_id, 'staff', hashed_pw)
    )
    print("Login entry created with username 'staff' and password 'staffpass'")
else:
    print(f"Login entry already exists with username: {login_entry['username']}")

# Assign staff role (not manager)
print("Assigning staff role...")
role_entry = fetch_one("SELECT role_id FROM Roles WHERE role_name = %s", ('staff',))
if role_entry:
    role_id = role_entry['role_id']
    try:
        execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s,%s)", (user_id, role_id))
        print("Staff role assigned successfully!")
    except Exception as e:
        print(f"Role assignment note: {e}")
else:
    print("Staff role not found in Roles table")

print("\n✅ Staff user setup complete!")
print(f"Login with:")
print(f"  Username: staff")
print(f"  Password: staffpass")
print(f"  Email: staff@hotel.com")
