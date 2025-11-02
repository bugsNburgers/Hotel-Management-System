# app.py
import streamlit as st
from auth import login_user, create_system_user, register_customer
from database import fetch_all, fetch_one, execute, call_proc
from datetime import date
from collections import defaultdict

st.set_page_config(page_title="Hotel Booking System", layout="wide")

# session defaults
if 'auth' not in st.session_state:
    st.session_state['auth'] = {"logged_in": False, "type": None, "user": None, "roles": [], "login": None}

def logout():
    st.session_state['auth'] = {"logged_in": False, "type": None, "user": None, "roles": [], "login": None}
    # rerun safely: use st.rerun() if available, else fallback
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ---------- AUTH UI ----------
if not st.session_state['auth']['logged_in']:
    st.title("Hotel Booking System — Login / Signup")
    left, right = st.columns(2)

    with left:
        st.subheader("Login")
        identifier = st.text_input("Username or Customer Email", key="login_identifier")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            res = login_user(identifier.strip(), password)
            if res:
                st.session_state['auth']['logged_in'] = True
                st.session_state['auth']['type'] = res.get('type')
                st.session_state['auth']['roles'] = res.get('roles', [])
                if res.get('type') == 'system':
                    st.session_state['auth']['user'] = res.get('user')
                    st.session_state['auth']['login'] = res.get('login')
                else:
                    st.session_state['auth']['user'] = res.get('customer')
                st.success("Login successful")
                # rerun
                if hasattr(st, "rerun"):
                    st.rerun()
                else:
                    st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    with right:
        st.subheader("Customer Signup")
        cn = st.text_input("Full name", key="signup_name")
        ce = st.text_input("Email", key="signup_email")
        cm = st.text_input("Mobile", key="signup_mobile")
        cp = st.text_input("Password", key="signup_pw", type="password")
        if st.button("Register as Customer"):
            if not ce or not cp:
                st.error("Email and password required")
            else:
                cid = register_customer(cn or "Guest", ce, cm, cp)
                st.success(f"Customer registered (id={cid}). Use your email to log in.")

    st.write("---")
    st.info("System users (admin/staff) must be created by admin. Seeded admin: username `admin`, password `adminpass` (seed).")

# ---------- Main app ----------
else:
    roles = st.session_state['auth']['roles'] or []
    user = st.session_state['auth']['user']
    st.sidebar.write(f"Logged in: {user.get('user_name') if user else user.get('cust_name')}")
    st.sidebar.write("Roles: " + ", ".join(roles))
    if st.sidebar.button("Logout"):
        logout()

    # ADMIN view
    if 'admin' in roles:
        st.title("Admin Dashboard")
        tabs = st.tabs(["Users", "Hotels", "Bookings", "Reports"])
        # Users
        with tabs[0]:
            st.header("System Users")
            users = fetch_all("SELECT user_id, user_name, user_email, user_mobile FROM `User`")
            st.dataframe(users)
            st.subheader("Create system user")
            name = st.text_input("Name", key="adm_name")
            email = st.text_input("Email", key="adm_email")
            mobile = st.text_input("Mobile", key="adm_mobile")
            addr = st.text_input("Address", key="adm_addr")
            uname = st.text_input("Username", key="adm_uname")
            pw = st.text_input("Password", key="adm_pw", type="password")
            role_name = st.selectbox("Assign role", options=["admin", "manager", "customer"], key="adm_role")
            if st.button("Create System User"):
                if not uname or not pw:
                    st.error("Username & password required")
                else:
                    uid = create_system_user(name, email, mobile, addr, uname, pw, assign_role_name=role_name)
                    st.success(f"Created user {uid} and assigned role {role_name}")
        # Hotels
        with tabs[1]:
            st.header("Hotels")
            hotels = fetch_all("SELECT * FROM Hotel")
            st.dataframe(hotels)
            st.subheader("Create Hotel")
            hname = st.text_input("Hotel name", key="adm_hname")
            htype = st.text_input("Hotel type", key="adm_htype")
            hdesc = st.text_area("Hotel desc", key="adm_hdesc")
            manager_user_id = st.number_input("Manager user_id (optional)", min_value=0, value=0, key="adm_mgr")
            if st.button("Create Hotel"):
                mgr = manager_user_id if manager_user_id > 0 else None
                hid = execute("INSERT INTO Hotel (hotel_name, hotel_type, hotel_desc, user_id) VALUES (%s,%s,%s,%s)",
                              (hname, htype, hdesc, mgr))
                st.success(f"Hotel created id {hid}")
        # Bookings
        with tabs[2]:
            st.header("All Bookings")
            rows = fetch_all("""
                SELECT b.book_id, b.book_date, b.book_type, b.book_desc, c.cust_name, h.hotel_name
                FROM Booking b
                JOIN Customer c ON c.cust_id=b.cust_id
                JOIN Hotel h ON h.hotel_id=b.hotel_id
                ORDER BY b.book_date DESC
            """)
            st.dataframe(rows)
        # Reports
        with tabs[3]:
            st.header("Revenue per Hotel")
            rpt = fetch_all("""
                SELECT h.hotel_id, h.hotel_name, COALESCE(SUM(p.pay_amt),0) AS total_revenue
                FROM Hotel h
                LEFT JOIN Booking b ON b.hotel_id = h.hotel_id
                LEFT JOIN Payment p ON p.book_id = b.book_id
                GROUP BY h.hotel_id, h.hotel_name
                ORDER BY total_revenue DESC
            """)
            st.table(rpt)

    # MANAGER view
    if 'manager' in roles:
        st.title("Manager Dashboard")
        st.subheader("Hotels you manage")
        my_hotels = fetch_all("SELECT * FROM Hotel WHERE user_id = %s", (user['user_id'],))
        st.write(my_hotels or "No hotels assigned")
        st.subheader("Classes for your hotels")
        if my_hotels:
            for h in my_hotels:
                st.markdown(f"**{h['hotel_name']}**")
                classes = fetch_all("SELECT * FROM Hotel_Class WHERE hotel_id=%s", (h['hotel_id'],))
                st.write(classes)
            st.write("Add class")
            sel = st.selectbox("Select hotel", options=my_hotels, format_func=lambda x: x['hotel_name'])
            cname = st.text_input("Class name", key="mgr_cname")
            crent = st.number_input("Class rent", key="mgr_crent", value=0.0)
            if st.button("Add Class"):
                execute("INSERT INTO Hotel_Class (hotel_id, class_name, class_rent) VALUES (%s,%s,%s)",
                        (sel['hotel_id'], cname, crent))
                st.success("Class added")
        st.subheader("Bookings for your hotels")
        hotel_ids = [h['hotel_id'] for h in my_hotels]
        if hotel_ids:
            qs = "SELECT b.book_id, b.book_date, b.book_type, b.book_desc, c.cust_name, h.hotel_name FROM Booking b JOIN Customer c ON c.cust_id=b.cust_id JOIN Hotel h ON h.hotel_id=b.hotel_id WHERE b.hotel_id IN (" + ",".join(["%s"]*len(hotel_ids)) + ") ORDER BY b.book_date DESC"
            bookings = fetch_all(qs, tuple(hotel_ids))
            st.dataframe(bookings)
        else:
            st.info("No bookings - you don't manage hotels yet.")

    # CUSTOMER view (includes users with only 'customer' role or login via customer email)
    if 'customer' in roles or st.session_state['auth']['type'] == 'customer':
        st.title("Customer Dashboard")
        st.subheader("Available Hotels & Classes")
        hotels = fetch_all("SELECT h.*, hc.class_id, hc.class_name, hc.class_rent FROM Hotel h LEFT JOIN Hotel_Class hc ON hc.hotel_id=h.hotel_id")
        grouped = defaultdict(list)
        for h in hotels:
            grouped[h['hotel_id']].append(h)
        for hid, rows in grouped.items():
            base = rows[0]
            st.markdown(f"### {base['hotel_name']} — {base.get('hotel_type')}")
            st.write(base.get('hotel_desc'))
            for r in rows:
                if r['class_id']:
                    st.write(f"- {r['class_name']} : ₹{r['class_rent']}")
            if st.button(f"Book at {base['hotel_name']}", key=f"book_{hid}"):
                st.session_state['booking_hotel_id'] = hid
                if hasattr(st, "rerun"):
                    st.rerun()
                else:
                    st.experimental_rerun()

        if 'booking_hotel_id' in st.session_state:
            hid = st.session_state['booking_hotel_id']
            st.subheader("Booking Form")
            c_email = st.text_input("Your registered customer email (required)")
            checkin = st.date_input("Check-in", value=date.today())
            checkout = st.date_input("Check-out", value=date.today())
            btype = st.selectbox("Booking type", ["single","double","family"])
            bdesc = st.text_area("Booking notes")
            pay_amt = st.number_input("Payment amount (for auto payment)", value=0.0)
            if st.button("Confirm Booking"):
                if not c_email:
                    st.error("Email required")
                else:
                    # find or create customer
                    cust = fetch_one("SELECT * FROM Customer WHERE cust_email=%s", (c_email,))
                    if cust:
                        cust_id = cust['cust_id']
                    else:
                        cust_id = execute("INSERT INTO Customer (cust_name, cust_email, cust_mobile) VALUES (%s,%s,%s)",
                                          (c_email.split('@')[0], c_email, ""))
                    # call stored procedure - if present
                    try:
                        call_proc('sp_make_booking', [cust_id, hid, checkin, btype, bdesc, pay_amt])
                        st.success("Booking created successfully")
                        del st.session_state['booking_hotel_id']
                    except Exception as e:
                        # fallback: manual
                        execute("INSERT INTO Booking (cust_id, hotel_id, book_date, book_type, book_desc) VALUES (%s,%s,%s,%s,%s)",
                                (cust_id, hid, date.today(), btype, bdesc))
                        st.success("Booking created (fallback)")

    # Sidebar: quick My Bookings (for any logged-in customer mapped from login)
    st.sidebar.markdown("---")
    st.sidebar.header("My Bookings")
    # Try map from system user email to Customer
    cust_email = None
    if st.session_state['auth']['type'] == 'system' and st.session_state['auth']['user']:
        ue = fetch_one("SELECT user_email FROM `User` WHERE user_id = %s", (st.session_state['auth']['user']['user_id'],))
        if ue:
            cust_email = ue.get('user_email')
    elif st.session_state['auth']['type'] == 'customer' and st.session_state['auth']['user']:
        cust_email = st.session_state['auth']['user'].get('cust_email')

    if cust_email:
        cust = fetch_one("SELECT * FROM Customer WHERE cust_email=%s", (cust_email,))
        if cust:
            bookings = fetch_all("""
                SELECT b.book_id, b.book_date, b.book_type, b.book_desc, h.hotel_name
                FROM Booking b
                JOIN Hotel h ON h.hotel_id = b.hotel_id
                WHERE b.cust_id = %s
                ORDER BY b.book_date DESC
            """, (cust['cust_id'],))
            for bk in bookings:
                st.sidebar.write(f"{bk['book_id']} | {bk['hotel_name']} | {bk['book_date']}")

