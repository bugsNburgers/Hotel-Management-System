# ============================================
# app.py - Simplified 3-Role Version
# ============================================
import streamlit as st
from auth import login_user, create_system_user, register_customer
from database import fetch_all, fetch_one, execute, call_proc
from datetime import date, timedelta
from collections import defaultdict

# Page config with custom theme
st.set_page_config(
    page_title="Hotel Booking System", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Hotel Booking Management System v2.0"
    }
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Login page hero section */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200');
        background-size: cover;
        background-position: center;
        padding: 80px 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Card styling */
    .auth-card {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Hotel card styling */
    .hotel-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .hotel-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* Stats card */
    .stats-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stats-label {
        font-size: 1rem;
        color: #666;
        margin-top: 10px;
    }
    
    /* Booking card */
    .booking-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    /* Feature icons */
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    /* Image gallery */
    .hotel-image {
        border-radius: 15px;
        width: 100%;
        height: 200px;
        object-fit: cover;
        margin-bottom: 15px;
    }
    
    /* Role badge */
    .role-badge {
        display: inline-block;
        padding: 5px 12px;
        margin: 5px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Task card */
    .task-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        border-left: 3px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Session defaults
if 'auth' not in st.session_state:
    st.session_state['auth'] = {"logged_in": False, "type": None, "user": None, "roles": [], "login": None}

def logout():
    st.session_state['auth'] = {"logged_in": False, "type": None, "user": None, "roles": [], "login": None}
    st.rerun()

# Role emoji mapping (simplified to 3 roles only)
ROLE_EMOJIS = {
    'admin': '🔧',
    'staff': '👔',
    'customer': '🛎️'
}

# ---------- AUTH UI ----------
if not st.session_state['auth']['logged_in']:
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">🏨 Hotel Booking</div>
            <div class="hero-subtitle">Experience world-class hospitality at your fingertips</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="feature-icon">🌟</div>', unsafe_allow_html=True)
        st.markdown("**Premium Hotels**")
        st.caption("Curated collection")
    with col2:
        st.markdown('<div class="feature-icon">💳</div>', unsafe_allow_html=True)
        st.markdown("**Secure Payment**")
        st.caption("Safe & encrypted")
    with col3:
        st.markdown('<div class="feature-icon">⚡</div>', unsafe_allow_html=True)
        st.markdown("**Instant Booking**")
        st.caption("Real-time confirmation")
    with col4:
        st.markdown('<div class="feature-icon">🎁</div>', unsafe_allow_html=True)
        st.markdown("**Best Prices**")
        st.caption("Guaranteed deals")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login forms - THREE COLUMNS
    left, middle, right = st.columns(3)

    # ADMIN LOGIN
    with left:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Admin Login")
        st.caption("System administrators")
        
        identifier = st.text_input("📧 Username/Email", key="admin_login_identifier", placeholder="admin")
        password = st.text_input("🔑 Password", type="password", key="admin_login_password", placeholder="••••••")
        
        if st.button("🚀 Admin Login", type="primary", use_container_width=True, key="btn_admin"):
            if not identifier or not password:
                st.error("⚠️ Please enter credentials")
            else:
                with st.spinner("Authenticating..."):
                    res = login_user(identifier.strip(), password)
                    if res and res.get('type') == 'system':
                        st.session_state['auth']['logged_in'] = True
                        st.session_state['auth']['type'] = 'system'
                        st.session_state['auth']['roles'] = res.get('roles', [])
                        st.session_state['auth']['user'] = res.get('user')
                        st.session_state['auth']['login'] = res.get('login')
                        st.success("✅ Welcome Admin!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # STAFF LOGIN
    with middle:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("### 👔 Staff Login")
        st.caption("Hotel staff members")
        
        staff_identifier = st.text_input("📧 Staff ID/Email", key="staff_login_identifier", placeholder="staff@hotel.com")
        staff_password = st.text_input("🔑 Password", type="password", key="staff_login_password", placeholder="••••••")
        
        if st.button("🚀 Staff Login", type="primary", use_container_width=True, key="btn_staff"):
            if not staff_identifier or not staff_password:
                st.error("⚠️ Please enter credentials")
            else:
                with st.spinner("Authenticating..."):
                    res = login_user(staff_identifier.strip(), staff_password)
                    if res and res.get('type') == 'system':
                        # Accept any system user who has the 'staff' role
                        roles = res.get('roles', [])
                        if 'staff' in roles:
                            st.session_state['auth']['logged_in'] = True
                            st.session_state['auth']['type'] = 'staff'
                            st.session_state['auth']['roles'] = ['staff']
                            st.session_state['auth']['user'] = res.get('user')
                            st.session_state['auth']['login'] = res.get('login')
                            st.success("✅ Welcome Staff!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ This user is not a staff member")
                    else:
                        st.error("❌ Invalid staff credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # CUSTOMER LOGIN/SIGNUP
    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        customer_tab = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        
        if customer_tab == "Login":
            st.markdown("### 🔐 Customer Login")
            st.caption("Welcome back!")
            
            cust_email = st.text_input("📧 Email", key="cust_login_email", placeholder="your@email.com")
            cust_pass = st.text_input("🔑 Password", type="password", key="cust_login_pass", placeholder="••••••")
            
            if st.button("🚀 Login", type="primary", use_container_width=True, key="btn_cust_login"):
                if not cust_email or not cust_pass:
                    st.error("⚠️ Please enter credentials")
                else:
                    with st.spinner("Authenticating..."):
                        from auth import hash_pass
                        # Try both hashed and plaintext for backward compatibility
                        cust = fetch_one("SELECT * FROM Customer WHERE cust_email = %s", (cust_email,))
                        
                        if cust:
                            stored_pass = cust.get('cust_pass', '')
                            hashed_input = hash_pass(cust_pass)
                            
                            # Check if password matches (hashed or plaintext)
                            if stored_pass == hashed_input or stored_pass == cust_pass:
                                st.session_state['auth']['logged_in'] = True
                                st.session_state['auth']['type'] = 'customer'
                                st.session_state['auth']['roles'] = ['customer']
                                st.session_state['auth']['user'] = cust
                                st.success("✅ Welcome back!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Invalid credentials")
                        else:
                            st.error("❌ Invalid credentials")
        
        else:  # Sign Up
            st.markdown("### 📝 New Customer")
            st.caption("Create your account")
            
            cn = st.text_input("👤 Full Name", key="signup_name", placeholder="John Doe")
            ce = st.text_input("📧 Email", key="signup_email", placeholder="john@example.com")
            cm = st.text_input("📱 Mobile", key="signup_mobile", placeholder="+91 98765 43210")
            cp = st.text_input("🔒 Password", key="signup_pw", type="password", placeholder="Create password")
            
            if st.button("✨ Create Account", type="primary", use_container_width=True, key="btn_signup"):
                if not ce or not cp:
                    st.error("⚠️ Email and password required")
                elif len(cp) < 6:
                    st.warning("⚠️ Password should be at least 6 characters")
                else:
                    try:
                        with st.spinner("Creating your account..."):
                            cid = register_customer(cn or "Guest", ce, cm, cp)
                            st.success(f"🎉 Welcome! Account created (ID: {cid})")
                            st.balloons()
                    except Exception as e:
                        st.error(f"❌ Registration failed: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Info section
    st.markdown("<br>", unsafe_allow_html=True)
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.info("🔑 **Admin:** admin / adminpass")
    with info_col2:
        st.info("👔 **Staff:** staff@hotel.com / staffpass")
    with info_col3:
        st.info("💼 **Support:** support@hotelbooking.com")

# ---------- Main app ----------
else:
    roles = st.session_state['auth']['roles'] or []
    user = st.session_state['auth']['user']
    user_name = user.get('user_name') if user.get('user_name') else user.get('cust_name', 'Guest')
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: white; border-radius: 15px; margin-bottom: 20px;">
                <div style="font-size: 4rem;">👤</div>
                <h3 style="margin: 10px 0; color: #667eea;">{user_name}</h3>
                <p style="color: #666; margin: 5px 0;">{'🎭 ' + ', '.join(roles)}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            logout()
        
        st.markdown("---")

    # ADMIN view
    if 'admin' in roles:
        st.markdown("""
            <div class="dashboard-header">
                <h1>🔧 Admin Control Panel</h1>
                <p>Manage your entire hotel booking system</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Statistics Dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = fetch_one("SELECT COUNT(*) as cnt FROM `User`")
            st.markdown(f"""
                <div class="stats-card">
                    <div style="font-size: 2rem;">👥</div>
                    <div class="stats-number">{total_users['cnt']}</div>
                    <div class="stats-label">Total Users</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_hotels = fetch_one("SELECT COUNT(*) as cnt FROM Hotel")
            st.markdown(f"""
                <div class="stats-card">
                    <div style="font-size: 2rem;">🏨</div>
                    <div class="stats-number">{total_hotels['cnt']}</div>
                    <div class="stats-label">Hotels</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_bookings = fetch_one("SELECT COUNT(*) as cnt FROM Booking")
            st.markdown(f"""
                <div class="stats-card">
                    <div style="font-size: 2rem;">📅</div>
                    <div class="stats-number">{total_bookings['cnt']}</div>
                    <div class="stats-label">Bookings</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_revenue = fetch_one("SELECT COALESCE(SUM(pay_amt),0) as revenue FROM Payment")
            st.markdown(f"""
                <div class="stats-card">
                    <div style="font-size: 2rem;">💰</div>
                    <div class="stats-number">₹{total_revenue['revenue']:,.0f}</div>
                    <div class="stats-label">Revenue</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        tabs = st.tabs(["👥 Users", "👔 Staff Management", "🏨 Hotels", "📅 Bookings", "📊 Reports"])
        
        # Users Tab
        with tabs[0]:
            st.markdown("### 👥 System Users Management")
            users = fetch_all("""
                SELECT DISTINCT u.user_id, u.user_name, u.user_email, u.user_mobile,
                       GROUP_CONCAT(r.role_name SEPARATOR ', ') as roles
                FROM `User` u
                LEFT JOIN User_Roles ur ON u.user_id = ur.user_id
                LEFT JOIN Roles r ON ur.role_id = r.role_id
                GROUP BY u.user_id, u.user_name, u.user_email, u.user_mobile
                ORDER BY u.user_id
            """)
            st.dataframe(users, use_container_width=True, height=300)
            
            with st.expander("➕ Create New System User", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("👤 Full Name", key="adm_name")
                    email = st.text_input("📧 Email", key="adm_email")
                    mobile = st.text_input("📱 Mobile", key="adm_mobile")
                with col2:
                    addr = st.text_input("📍 Address", key="adm_addr")
                    uname = st.text_input("🔑 Username", key="adm_uname")
                    pw = st.text_input("🔒 Password", key="adm_pw", type="password")
                
                role_name = st.selectbox("🎭 Assign Role", options=["admin", "staff", "customer"], key="adm_role")
                
                if st.button("✨ Create User", type="primary"):
                    if not uname or not pw:
                        st.error("⚠️ Username & password required")
                    else:
                        try:
                            uid = create_system_user(name, email, mobile, addr, uname, pw, assign_role_name=role_name)
                            st.success(f"✅ User created successfully! ID: {uid} | Role: {role_name}")
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        # Staff Management Tab (simplified)
        with tabs[1]:
            st.markdown("### 👔 Staff Management Dashboard")

            # Staff count
            staff_count = fetch_one("SELECT COUNT(DISTINCT u.user_id) as cnt FROM `User` u JOIN User_Roles ur ON u.user_id = ur.user_id JOIN Roles r ON ur.role_id = r.role_id WHERE r.role_name = 'staff'")
            cnt = staff_count.get('cnt', 0) if staff_count else 0
            st.markdown(f"\n<div class=\"stats-card\">\n  <div style=\"font-size: 2rem;\">{ROLE_EMOJIS.get('staff','👔')}</div>\n  <div class=\"stats-number\">{cnt}</div>\n  <div class=\"stats-label\">Staff Members</div>\n</div>\n", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # View All Staff (from User_Roles)
            st.markdown("#### 📋 All Staff Members")
            all_staff = fetch_all("""
                SELECT DISTINCT u.user_id, u.user_name, u.user_email
                FROM `User` u
                JOIN User_Roles ur ON u.user_id = ur.user_id
                JOIN Roles r ON ur.role_id = r.role_id
                WHERE r.role_name = 'staff'
                ORDER BY u.user_name
            """)

            if all_staff:
                for staff in all_staff:
                    with st.expander(f"👤 {staff['user_name']} ({staff['user_email']})"):
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.write(f"**User ID:** {staff['user_id']}")
                            st.write(f"**Email:** {staff['user_email']}")
                        with col2:
                            if st.button("🗑️ Remove Staff Role", key=f"btn_remove_staff_{staff['user_id']}"):
                                # remove staff role from User_Roles
                                execute("DELETE ur FROM User_Roles ur JOIN Roles r ON ur.role_id = r.role_id WHERE ur.user_id = %s AND r.role_name = 'staff'", (staff['user_id'],))
                                st.success("✅ Staff role removed")
                                st.rerun()
            else:
                st.info("No staff members assigned yet")

            st.markdown("---")

            # Assign Staff Role
            with st.expander("➕ Assign Staff Role", expanded=False):
                all_users = fetch_all("SELECT user_id, user_name, user_email FROM `User`")
                user_options = {f"{u['user_name']} ({u['user_email']})": u['user_id'] for u in all_users}
                selected_user = st.selectbox("Select User", options=list(user_options.keys()))
                selected_user_id = user_options[selected_user]

                if st.button("✨ Assign Staff Role", type="primary"):
                    try:
                        # find staff role id
                        r = fetch_one("SELECT role_id FROM Roles WHERE role_name=%s", ('staff',))
                        if not r:
                            role_id = execute("INSERT INTO Roles (role_name, role_desc) VALUES (%s,%s)", ('staff','Hotel staff'))
                        else:
                            role_id = r['role_id']
                        execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s,%s)", (selected_user_id, role_id))
                        st.success("✅ Staff role assigned")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

            # Create New Staff Member (simple)
            with st.expander("➕ Create New Staff Member", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    staff_name = st.text_input("👤 Full Name", key="staff_name")
                    staff_email = st.text_input("📧 Email", key="staff_email")
                    staff_mobile = st.text_input("📱 Mobile", key="staff_mobile")
                with col2:
                    staff_addr = st.text_input("📍 Address", key="staff_addr")
                    staff_uname = st.text_input("🔑 Username", key="staff_uname")
                    staff_pw = st.text_input("🔒 Password", key="staff_pw", type="password")

                if st.button("✨ Create Staff Member", type="primary"):
                    if not staff_uname or not staff_pw:
                        st.error("⚠️ Username & password required")
                    else:
                        try:
                            uid = create_system_user(staff_name, staff_email, staff_mobile, staff_addr, staff_uname, staff_pw, assign_role_name='staff')
                            st.success(f"✅ Staff member created! ID: {uid}")
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        # Hotels Tab
        with tabs[2]:
            st.markdown("### 🏨 Hotels & Rooms Management")
            hotels = fetch_all("SELECT * FROM Hotel")
            
            for hotel in hotels:
                with st.expander(f"🏨 {hotel['hotel_name']} - {hotel.get('hotel_type', 'Standard')}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Description:** {hotel.get('hotel_desc', 'N/A')}")
                        
                        # Show room classes for this hotel
                        st.markdown("#### 🛏️ Room Classes")
                        room_classes = fetch_all("""
                            SELECT class_id, class_name, class_rent, room_count
                            FROM Hotel_Class
                            WHERE hotel_id = %s
                        """, (hotel['hotel_id'],))
                        
                        if room_classes:
                            for rc in room_classes:
                                st.write(f"- **{rc['class_name']}**: ₹{rc['class_rent']}/night ({rc['room_count']} rooms)")
                        else:
                            st.info("No room classes defined yet")
                        
                        # Show individual rooms
                        st.markdown("#### 🏠 Room Inventory")
                        rooms = fetch_all("""
                            SELECT r.room_id, r.room_number, r.room_status, hc.class_name
                            FROM Rooms r
                            JOIN Hotel_Class hc ON r.class_id = hc.class_id
                            WHERE r.hotel_id = %s
                            ORDER BY r.room_number
                        """, (hotel['hotel_id'],))
                        
                        if rooms:
                            room_df = [{
                                'Room #': r['room_number'],
                                'Class': r['class_name'],
                                'Status': r['room_status']
                            } for r in rooms]
                            st.dataframe(room_df, use_container_width=True, height=200)
                        else:
                            st.info("No rooms added yet")
                        
                        # Add room form
                        with st.form(f"add_room_{hotel['hotel_id']}"):
                            st.markdown("**➕ Add New Room**")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                room_num = st.text_input("Room Number", key=f"rnum_{hotel['hotel_id']}")
                            with col_b:
                                if room_classes:
                                    class_options = {rc['class_name']: rc['class_id'] for rc in room_classes}
                                    selected_class = st.selectbox("Room Class", options=list(class_options.keys()), 
                                                                  key=f"rclass_{hotel['hotel_id']}")
                                    class_id = class_options[selected_class]
                                else:
                                    st.warning("Add room class first")
                                    class_id = None
                            
                            if st.form_submit_button("Add Room") and class_id and room_num:
                                try:
                                    execute("""
                                        INSERT INTO Rooms (hotel_id, class_id, room_number, room_status)
                                        VALUES (%s, %s, %s, 'Available')
                                    """, (hotel['hotel_id'], class_id, room_num))
                                    st.success(f"✅ Room {room_num} added!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error: {e}")
                    
                    with col2:
                        st.image("https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400", use_container_width=True)
            
            st.markdown("---")
            with st.expander("➕ Add New Hotel", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    hname = st.text_input("🏨 Hotel Name", key="adm_hname", placeholder="Grand Plaza Hotel")
                    htype = st.text_input("⭐ Hotel Type", key="adm_htype", placeholder="5-Star Luxury")
                with col2:
                    hdesc = st.text_area("📝 Description", key="adm_hdesc", placeholder="Luxury hotel with world-class amenities...")
                
                if st.button("🏨 Create Hotel", type="primary"):
                    hid = execute("INSERT INTO Hotel (hotel_name, hotel_type, hotel_desc, user_id) VALUES (%s,%s,%s,%s)",
                                  (hname, htype, hdesc, None))
                    st.success(f"✅ Hotel created successfully! ID: {hid}")
                    st.balloons()
                    st.rerun()
        
        # Bookings Tab
        with tabs[3]:
            st.markdown("### 📅 All Bookings")
            rows = fetch_all("""
                SELECT b.book_id, b.book_date, b.check_in, b.check_out, b.book_type, b.booking_status,
                       c.cust_name, c.cust_email, h.hotel_name, 
                       r.room_number, hc.class_name as room_class,
                       u.user_name as booked_by,
                       p.pay_amt, p.pay_method
                FROM Booking b
                JOIN Customer c ON c.cust_id=b.cust_id
                JOIN Hotel h ON h.hotel_id=b.hotel_id
                JOIN User u ON u.user_id=b.user_id
                LEFT JOIN Rooms r ON r.room_id=b.room_id
                LEFT JOIN Hotel_Class hc ON r.class_id=hc.class_id
                LEFT JOIN Payment p ON p.book_id=b.book_id
                ORDER BY b.book_date DESC
            """)
            st.dataframe(rows, use_container_width=True, height=400)
        
        # Reports Tab
        with tabs[4]:
            st.markdown("### 📊 Revenue Analytics")
            rpt = fetch_all("""
                SELECT h.hotel_id, h.hotel_name, COALESCE(SUM(p.pay_amt),0) AS total_revenue,
                       COUNT(DISTINCT b.book_id) as booking_count
                FROM Hotel h
                LEFT JOIN Booking b ON b.hotel_id = h.hotel_id
                LEFT JOIN Payment p ON p.book_id = b.book_id
                GROUP BY h.hotel_id, h.hotel_name
                ORDER BY total_revenue DESC
            """)
            st.dataframe(rpt, use_container_width=True, height=350)

    # MANAGER role removed — managers are now staff. No specific manager UI.

    # STAFF view (generic)
    elif 'staff' in roles:
        st.markdown("""
            <div class="dashboard-header">
                <h1>👔 Staff Dashboard</h1>
                <p>Manage bookings, guests and daily operations</p>
            </div>
        """, unsafe_allow_html=True)

        # Simple staff dashboard focused on bookings and quick actions
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 Today's Bookings & Check-ins")
            recent_bookings = fetch_all("""
                SELECT b.book_id, b.check_in, b.check_out, b.booking_status,
                       c.cust_name, c.cust_email, h.hotel_name,
                       r.room_number, hc.class_name as room_type
                FROM Booking b
                JOIN Customer c ON c.cust_id = b.cust_id
                JOIN Hotel h ON h.hotel_id = b.hotel_id
                LEFT JOIN Rooms r ON r.room_id = b.room_id
                LEFT JOIN Hotel_Class hc ON r.class_id = hc.class_id
                WHERE b.check_in >= CURDATE()
                ORDER BY b.check_in ASC
                LIMIT 10
            """)
            st.dataframe(recent_bookings, use_container_width=True)

        with col2:
            st.markdown("#### 🏠 Room Management")
            
            # Room status overview
            room_stats = fetch_one("""
                SELECT 
                    COUNT(*) as total_rooms,
                    SUM(CASE WHEN room_status = 'Available' THEN 1 ELSE 0 END) as available,
                    SUM(CASE WHEN room_status = 'Occupied' THEN 1 ELSE 0 END) as occupied,
                    SUM(CASE WHEN room_status = 'Reserved' THEN 1 ELSE 0 END) as reserved,
                    SUM(CASE WHEN room_status = 'Maintenance' THEN 1 ELSE 0 END) as maintenance
                FROM Rooms
            """)
            
            if room_stats:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("🟢 Available", room_stats.get('available', 0))
                    st.metric("🔴 Occupied", room_stats.get('occupied', 0))
                with col_b:
                    st.metric("🟡 Reserved", room_stats.get('reserved', 0))
                    st.metric("🔧 Maintenance", room_stats.get('maintenance', 0))
            
            st.markdown("---")
            
            # Quick Actions with functionality
            st.markdown("#### ⚡ Quick Actions")
            
            # Guest Search
            with st.expander("🔍 Search Guest", expanded=False):
                search_email = st.text_input("Enter guest email", key="staff_search_email")
                if st.button("Search", key="btn_search_guest"):
                    if search_email:
                        guest_bookings = fetch_all("""
                            SELECT b.book_id, b.check_in, b.check_out, b.booking_status,
                                   c.cust_name, c.cust_email, h.hotel_name,
                                   r.room_number, hc.class_name
                            FROM Booking b
                            JOIN Customer c ON c.cust_id = b.cust_id
                            JOIN Hotel h ON h.hotel_id = b.hotel_id
                            LEFT JOIN Rooms r ON r.room_id = b.room_id
                            LEFT JOIN Hotel_Class hc ON r.class_id = hc.class_id
                            WHERE c.cust_email LIKE %s
                            ORDER BY b.book_date DESC
                        """, (f"%{search_email}%",))
                        
                        if guest_bookings:
                            st.success(f"Found {len(guest_bookings)} booking(s)")
                            st.dataframe(guest_bookings, use_container_width=True)
                        else:
                            st.warning("No bookings found for this email")
                    else:
                        st.error("Please enter an email")
            
            # Mark Check-in
            with st.expander("✅ Mark Check-in", expanded=False):
                booking_id = st.number_input("Booking ID", min_value=1, step=1, key="staff_checkin_id")
                if st.button("Confirm Check-in", key="btn_mark_checkin"):
                    try:
                        # Update booking status
                        execute("UPDATE Booking SET booking_status = 'Confirmed' WHERE book_id = %s", (booking_id,))
                        
                        # Get room and update to Occupied
                        room_info = fetch_one("""
                            SELECT room_id FROM Booking WHERE book_id = %s
                        """, (booking_id,))
                        
                        if room_info and room_info.get('room_id'):
                            execute("UPDATE Rooms SET room_status = 'Occupied' WHERE room_id = %s", 
                                    (room_info['room_id'],))
                        
                        st.success(f"✅ Check-in completed for Booking #{booking_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            # Update Room Status
            with st.expander("🔧 Update Room Status", expanded=False):
                all_rooms = fetch_all("""
                    SELECT r.room_id, r.room_number, h.hotel_name, r.room_status
                    FROM Rooms r
                    JOIN Hotel h ON r.hotel_id = h.hotel_id
                    ORDER BY h.hotel_name, r.room_number
                """)
                
                if all_rooms:
                    room_options = {f"{r['hotel_name']} - Room {r['room_number']} (Current: {r['room_status']})": r['room_id'] 
                                    for r in all_rooms}
                    selected_room = st.selectbox("Select Room", options=list(room_options.keys()), key="staff_room_select")
                    new_status = st.selectbox("New Status", 
                                              ["Available", "Occupied", "Reserved", "Maintenance"],
                                              key="staff_new_status")
                    
                    if st.button("Update Status", key="btn_update_room_status"):
                        try:
                            room_id = room_options[selected_room]
                            execute("UPDATE Rooms SET room_status = %s WHERE room_id = %s", 
                                    (new_status, room_id))
                            st.success(f"✅ Room status updated to {new_status}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.info("No rooms available in the system")
        st.markdown("---")

    # CUSTOMER view
    elif 'customer' in roles or st.session_state['auth']['type'] == 'customer':
        st.markdown("""
            <div class="dashboard-header">
                <h1>🛎️ Discover Your Perfect Stay</h1>
                <p>Browse and book from our collection of premium hotels</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Available Hotels
        hotels = fetch_all("""
            SELECT h.*, hc.class_id, hc.class_name, hc.class_rent, hc.room_count 
            FROM Hotel h 
            LEFT JOIN Hotel_Class hc ON hc.hotel_id=h.hotel_id
        """)
        
        # Hotel images for variety
        hotel_images = [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600",
            "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=600",
            "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600",
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=600",
            "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600"
        ]
        
        grouped = defaultdict(list)
        for h in hotels:
            grouped[h['hotel_id']].append(h)
        
        # Display hotels in grid
        cols = st.columns(2)
        for idx, (hid, rows) in enumerate(grouped.items()):
            base = rows[0]
            with cols[idx % 2]:
                st.image(hotel_images[idx % len(hotel_images)], use_container_width=True)
                
                st.markdown(f"""
                    <div class="hotel-card">
                        <h3 style="color: #333; margin: 0 0 10px 0;">🏨 {base['hotel_name']}</h3>
                        <p style="color: #667eea; margin: 10px 0; font-weight: 500;">⭐ {base.get('hotel_type', 'Standard Hotel')}</p>
                        <p style="color: #555; margin: 15px 0; line-height: 1.6;">{base.get('hotel_desc', 'Luxury accommodation with premium amenities')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📋 View Details & Book"):
                    st.markdown("#### 🛏️ Available Room Classes")
                    has_rooms = False
                    for r in rows:
                        if r['class_id']:
                            has_rooms = True
                            # Get available room count for this class
                            available_count = fetch_one("""
                                SELECT COUNT(*) as cnt FROM Rooms 
                                WHERE hotel_id = %s AND class_id = %s AND room_status = 'Available'
                            """, (hid, r['class_id']))
                            
                            avail_cnt = available_count['cnt'] if available_count else 0
                            total_cnt = r.get('room_count', 0)
                            
                            col_a, col_b, col_c = st.columns([2, 1, 1])
                            with col_a:
                                st.write(f"**{r['class_name']}**")
                            with col_b:
                                status_color = "🟢" if avail_cnt > 0 else "🔴"
                                st.write(f"{status_color} {avail_cnt}/{total_cnt} available")
                            with col_c:
                                st.write(f"**₹{r['class_rent']:,.0f}**/night")
                    
                    if not has_rooms:
                        st.info("Room classes will be available soon")
                    
                    st.markdown("---")
                    if st.button(f"📅 Book {base['hotel_name']}", key=f"book_{hid}", type="primary", use_container_width=True):
                        st.session_state['booking_hotel_id'] = hid
                        st.rerun()

        # Booking Form
        if 'booking_hotel_id' in st.session_state:
            st.markdown("<br><br>", unsafe_allow_html=True)
            hid = st.session_state['booking_hotel_id']
            hotel_info = fetch_one("SELECT * FROM Hotel WHERE hotel_id = %s", (hid,))
            
            st.markdown(f"""
                <div class="dashboard-header">
                    <h2>📝 Complete Your Booking</h2>
                    <p>You're booking: {hotel_info['hotel_name']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Get available rooms for this hotel
            available_rooms = fetch_all("""
                SELECT r.room_id, r.room_number, hc.class_name, hc.class_rent, r.room_status
                FROM Rooms r
                JOIN Hotel_Class hc ON r.class_id = hc.class_id
                WHERE r.hotel_id = %s AND r.room_status = 'Available'
                ORDER BY hc.class_rent
            """, (hid,))
            
            col1, col2 = st.columns(2)
            
            with col1:
                c_email = st.text_input("📧 Your Email", 
                                        value=user.get('cust_email', '') if st.session_state['auth']['type'] == 'customer' else '',
                                        placeholder="your.email@example.com")
                checkin = st.date_input("📅 Check-in Date", value=date.today(), min_value=date.today())
                btype = st.selectbox("👥 Booking Type", ["single", "double", "family"], 
                                    format_func=lambda x: f"{'👤' if x=='single' else '👥' if x=='double' else '👨‍👩‍👧‍👦'} {x.title()}")
                
                # Room selection
                if available_rooms:
                    room_options = {f"Room {r['room_number']} - {r['class_name']} (₹{r['class_rent']:.0f}/night)": r['room_id'] 
                                    for r in available_rooms}
                    selected_room = st.selectbox("🏠 Select Room", options=list(room_options.keys()))
                    room_id = room_options[selected_room]
                    selected_room_info = next(r for r in available_rooms if r['room_id'] == room_id)
                else:
                    st.warning("⚠️ No rooms available at this hotel")
                    room_id = None
                    selected_room_info = None
            
            with col2:
                checkout = st.date_input("📅 Check-out Date", value=date.today() + timedelta(days=1), 
                                        min_value=date.today() + timedelta(days=1))
                pay_method = st.selectbox("💳 Payment Method", ["Card", "UPI", "Cash", "Online"])
                bdesc = st.text_area("📝 Special Requests", placeholder="Any special requirements...")
            
            # Calculate nights and total
            pay_amt = 0.0
            if checkout > checkin and selected_room_info:
                nights = (checkout - checkin).days
                pay_amt = selected_room_info['class_rent'] * nights
                st.info(f"🌙 Total nights: **{nights}** | Total amount: **₹{pay_amt:,.2f}**")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Booking", type="primary", use_container_width=True):
                    if not c_email:
                        st.error("⚠️ Email is required")
                    elif checkout <= checkin:
                        st.error("⚠️ Check-out must be after check-in")
                    elif not room_id:
                        st.error("⚠️ Please select a room")
                    else:
                        try:
                            with st.spinner("Processing your booking..."):
                                # Check if customer exists
                                cust = fetch_one("SELECT * FROM Customer WHERE cust_email=%s", (c_email,))
                                
                                if cust:
                                    cust_id = cust['cust_id']
                                    user_id = cust.get('user_id')
                                    
                                    # If customer doesn't have user_id, create User entry
                                    if not user_id:
                                        user_id = execute("""
                                            INSERT INTO User (user_name, user_email, user_mobile, user_address)
                                            VALUES (%s, %s, %s, %s)
                                        """, (cust['cust_name'], c_email, cust.get('cust_mobile', ''), 'Customer Address'))
                                        
                                        # Link customer to user
                                        execute("UPDATE Customer SET user_id = %s WHERE cust_id = %s", (user_id, cust_id))
                                        
                                        # Assign customer role
                                        customer_role = fetch_one("SELECT role_id FROM Roles WHERE role_name='customer'")
                                        if customer_role:
                                            execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s, %s)",
                                                    (user_id, customer_role['role_id']))
                                else:
                                    # Create new User first
                                    user_id = execute("""
                                        INSERT INTO User (user_name, user_email, user_mobile, user_address)
                                        VALUES (%s, %s, %s, %s)
                                    """, (c_email.split('@')[0], c_email, '', 'Customer Address'))
                                    
                                    # Create Customer linked to User
                                    cust_id = execute("""
                                        INSERT INTO Customer (user_id, cust_name, cust_email, cust_mobile, cust_pass)
                                        VALUES (%s, %s, %s, %s, %s)
                                    """, (user_id, c_email.split('@')[0], c_email, '', 'defaultpass'))
                                    
                                    # Assign customer role
                                    customer_role = fetch_one("SELECT role_id FROM Roles WHERE role_name='customer'")
                                    if customer_role:
                                        execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s, %s)",
                                                (user_id, customer_role['role_id']))
                                
                                # Call stored procedure with all new parameters
                                call_proc('sp_make_booking', [
                                    user_id,        # p_user_id
                                    cust_id,        # p_cust_id
                                    hid,            # p_hotel_id
                                    room_id,        # p_room_id
                                    date.today(),   # p_book_date
                                    checkin,        # p_check_in
                                    checkout,       # p_check_out
                                    btype,          # p_book_type
                                    bdesc,          # p_book_desc
                                    pay_amt,        # p_pay_amt
                                    pay_method      # p_pay_method
                                ])
                                
                                st.success("🎉 Booking confirmed successfully!")
                                st.balloons()
                                del st.session_state['booking_hotel_id']
                                st.rerun()
                        except Exception as e:
                            st.error(f"❌ Booking failed: {e}")
            
            with col_cancel:
                if st.button("❌ Cancel", use_container_width=True):
                    del st.session_state['booking_hotel_id']
                    st.rerun()

    # My Bookings Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style="background: white; padding: 15px; border-radius: 12px; margin-bottom: 15px;">
            <h3 style="margin: 0; color: #667eea;">📋 My Bookings</h3>
        </div>
    """, unsafe_allow_html=True)
    
    cust_email = None
    if st.session_state['auth']['type'] == 'system' and st.session_state['auth']['user']:
        ue = fetch_one("SELECT user_email FROM `User` WHERE user_id = %s", 
                       (st.session_state['auth']['user']['user_id'],))
        if ue:
            cust_email = ue.get('user_email')
    elif st.session_state['auth']['type'] == 'customer' and st.session_state['auth']['user']:
        cust_email = st.session_state['auth']['user'].get('cust_email')

    if cust_email:
        cust = fetch_one("SELECT * FROM Customer WHERE cust_email=%s", (cust_email,))
        if cust:
            bookings = fetch_all("""
                SELECT b.book_id, b.book_date, b.check_in, b.check_out, b.booking_status, 
                       h.hotel_name, b.book_type,
                       r.room_number, hc.class_name as room_class,
                       p.pay_amt, p.pay_method
                FROM Booking b
                JOIN Hotel h ON h.hotel_id = b.hotel_id
                LEFT JOIN Rooms r ON r.room_id = b.room_id
                LEFT JOIN Hotel_Class hc ON r.class_id = hc.class_id
                LEFT JOIN Payment p ON p.book_id = b.book_id
                WHERE b.cust_id = %s
                ORDER BY b.book_date DESC
                LIMIT 5
            """, (cust['cust_id'],))
            
            if bookings:
                for bk in bookings:
                    status_emoji = "✅" if bk['booking_status'] == 'Confirmed' else "⏳" if bk['booking_status'] == 'Pending' else "❌"
                    room_info = f"🏠 Room {bk['room_number']} ({bk['room_class']})" if bk.get('room_number') else "🏠 Room TBD"
                    payment_info = f"💳 ₹{bk['pay_amt']:,.0f} ({bk['pay_method']})" if bk.get('pay_amt') else "💳 Payment Pending"
                    check_dates = f"📅 {bk['check_in']} to {bk['check_out']}" if bk.get('check_in') else f"📅 {bk['book_date']}"
                    
                    st.sidebar.markdown(f"""
                        <div class="booking-card">
                            <div style="font-weight: 600; margin-bottom: 5px;">
                                {status_emoji} Booking #{bk['book_id']}
                            </div>
                            <div style="font-size: 0.9rem; color: #555;">
                                🏨 {bk['hotel_name']}<br>
                                {check_dates}<br>
                                {room_info}<br>
                                {payment_info}<br>
                                <span style="background: {'#4CAF50' if bk['booking_status']=='Confirmed' else '#FF9800'}; 
                                      color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem;">
                                    {bk['booking_status'].upper()}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.sidebar.info("📭 No bookings yet")
                st.sidebar.caption("Start exploring hotels above!")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; padding: 30px; background: white; border-radius: 15px; margin-top: 50px;">
            <h4 style="color: #667eea; margin-bottom: 15px;">🏨 Hotel Booking System v2.0</h4>
            <p style="color: #666; margin: 5px 0;">Experience luxury at your fingertips</p>
            <p style="color: #999; font-size: 0.9rem;">
                📞 24/7 Support • 💳 Secure Payments • ⚡ Instant Confirmation
            </p>
        </div>
    """, unsafe_allow_html=True)