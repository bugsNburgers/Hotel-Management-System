# auth.py
import hashlib
from database import fetch_one, fetch_all, execute

def hash_pass(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def verify_password(stored: str, provided: str) -> bool:
    # Accept seeded plaintext or sha256-hashed stored values
    if stored == provided:
        return True
    return stored == hash_pass(provided)

def login_user(identifier: str, password: str):
    """
    Try to login:
    1) Check Login table (system users)
    2) If not found, check Customer table (customer login via email)
    Returns dict with keys: type ('system' or 'customer'), login_row/user_row/roles
    """
    # 1) System user login (Login.username)
    row = fetch_one("SELECT * FROM Login WHERE username = %s", (identifier,))
    if row:
        if verify_password(row['password'], password):
            user = fetch_one("SELECT * FROM `User` WHERE user_id = %s", (row['user_id'],))
            roles_rows = fetch_all("""
                SELECT r.role_name FROM Roles r
                JOIN User_Roles ur ON ur.role_id = r.role_id
                WHERE ur.user_id = %s
            """, (row['user_id'],))
            roles = [r['role_name'] for r in roles_rows]

            # If no roles found, auto-assign admin to first seeded user (id=1) for compatibility
            if not roles:
                if row['user_id'] == 1:
                    # ensure admin role exists
                    r = fetch_one("SELECT role_id FROM Roles WHERE role_name='admin'")
                    if not r:
                        role_id = execute("INSERT INTO Roles (role_name, role_desc) VALUES (%s,%s)", ('admin','System administrator'))
                    else:
                        role_id = r['role_id']
                    # assign
                    try:
                        execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s,%s)", (row['user_id'], role_id))
                    except Exception:
                        pass
                    roles = ['admin']

            return {"type":"system", "login": row, "user": user, "roles": roles}

    # 2) Customer login (allow customer to login by email)
    cust = fetch_one("SELECT * FROM Customer WHERE cust_email = %s", (identifier,))
    if cust:
        stored = cust.get('cust_pass') or ''
        if stored and verify_password(stored, password):
            return {"type":"customer", "customer": cust, "roles": ['customer']}
        # also accept if stored plaintext equals provided
        if stored == password:
            return {"type":"customer", "customer": cust, "roles": ['customer']}

    return None

def create_system_user(user_name, user_email, user_mobile, user_address, username, password, assign_role_name=''):
    # creates User + Login, stores hashed password in Login
    user_id = execute("INSERT INTO `User` (user_name, user_email, user_mobile, user_address) VALUES (%s,%s,%s,%s)",
                      (user_name, user_email, user_mobile, user_address))
    hp = hash_pass(password)
    execute("INSERT INTO Login (user_id, username, password) VALUES (%s,%s,%s)", (user_id, username, hp))
    if assign_role_name:
        r = fetch_one("SELECT role_id FROM Roles WHERE role_name=%s", (assign_role_name,))
        if not r:
            role_id = execute("INSERT INTO Roles (role_name, role_desc) VALUES (%s,%s)", (assign_role_name, ''))
        else:
            role_id = r['role_id']
        try:
            execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s,%s)", (user_id, role_id))
        except Exception:
            pass
    return user_id

def register_customer(cust_name, cust_email, cust_mobile, password):
    # store hashed password
    hp = hash_pass(password)
    cust_id = execute("INSERT INTO Customer (cust_name, cust_email, cust_mobile, cust_pass) VALUES (%s,%s,%s,%s)",
                      (cust_name, cust_email, cust_mobile, hp))
    return cust_id
