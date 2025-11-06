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
                        cust = fetch_one("SELECT * FROM Customer WHERE cust_email = %s AND cust_pass = %s", 
                                        (cust_email, cust_pass))
                        if cust:
                            st.session_state['auth']['logged_in'] = True
                            st.session_state['auth']['type'] = 'customer'
                            st.session_state['auth']['roles'] = ['customer']
                            st.session_state['auth']['user'] = cust
                            st.success("✅ Welcome back!")
                            st.balloons()
                            st.rerun()
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
            users = fetch_all("SELECT user_id, user_name, user_email, user_mobile FROM `User`")
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
            st.markdown("### 🏨 Hotels Management")
            hotels = fetch_all("SELECT * FROM Hotel")
            
            for hotel in hotels:
                with st.expander(f"🏨 {hotel['hotel_name']} - {hotel.get('hotel_type', 'Standard')}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Description:** {hotel.get('hotel_desc', 'N/A')}")
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
                SELECT b.book_id, b.book_date, b.book_type, b.booking_status, 
                       c.cust_name, h.hotel_name
                FROM Booking b
                JOIN Customer c ON c.cust_id=b.cust_id
                JOIN Hotel h ON h.hotel_id=b.hotel_id
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
                SELECT b.book_id, c.cust_name, h.hotel_name, b.booking_status
                FROM Booking b
                JOIN Customer c ON c.cust_id = b.cust_id
                JOIN Hotel h ON h.hotel_id = b.hotel_id
                ORDER BY b.book_date DESC
                LIMIT 10
            """)
            st.dataframe(recent_bookings, use_container_width=True)

        with col2:
            st.markdown("#### Quick Actions")
            if st.button("➕ New Walk-in Booking", use_container_width=True):
                st.info("Walk-in booking form would appear here")
            if st.button("🔍 Search Guest", use_container_width=True):
                st.info("Guest search interface would appear here")
            if st.button("✅ Mark Check-in", use_container_width=True):
                st.info("Check-in marked")
        st.markdown("---")

    # CUSTOMER view
    elif 'customer' in roles or st.session_state['auth']['type'] == 'customer':
        st.markdown("""
            <div class="dashboard-header">
                <h1>🛎️ Discover Your Perfect Stay</h1>
                <p>Browse and book from our collection of premium hotels</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Search and filter section
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_term = st.text_input("🔍 Search hotels", placeholder="Search by name or location...")
        with col2:
            filter_type = st.selectbox("⭐ Filter by type", ["All", "5-Star", "4-Star", "3-Star", "Budget"])
        with col3:
            sort_by = st.selectbox("📊 Sort by", ["Name", "Price", "Rating"])
        
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
                        <h3>🏨 {base['hotel_name']}</h3>
                        <p style="color: #666; margin: 10px 0;">⭐ {base.get('hotel_type', 'Standard Hotel')}</p>
                        <p style="margin: 15px 0;">{base.get('hotel_desc', 'Luxury accommodation with premium amenities')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📋 View Details & Book"):
                    st.markdown("#### 🛏️ Available Room Classes")
                    has_rooms = False
                    for r in rows:
                        if r['class_id']:
                            has_rooms = True
                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.write(f"**{r['class_name']}** • {r.get('room_count', 0)} rooms available")
                            with col_b:
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                c_email = st.text_input("📧 Your Email", 
                                        value=user.get('cust_email', '') if st.session_state['auth']['type'] == 'customer' else '',
                                        placeholder="your.email@example.com")
                checkin = st.date_input("📅 Check-in Date", value=date.today(), min_value=date.today())
                btype = st.selectbox("👥 Booking Type", ["single", "double", "family"], 
                                    format_func=lambda x: f"{'👤' if x=='single' else '👥' if x=='double' else '👨‍👩‍👧‍👦'} {x.title()}")
            
            with col2:
                checkout = st.date_input("📅 Check-out Date", value=date.today() + timedelta(days=1), 
                                        min_value=date.today() + timedelta(days=1))
                pay_amt = st.number_input("💳 Payment Amount (₹)", value=0.0, min_value=0.0, step=500.0)
                bdesc = st.text_area("📝 Special Requests", placeholder="Any special requirements...")
            
            # Calculate nights and total
            if checkout > checkin:
                nights = (checkout - checkin).days
                st.info(f"🌙 Total nights: **{nights}** | Estimated amount: **₹{pay_amt * nights:,.2f}**")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Booking", type="primary", use_container_width=True):
                    if not c_email:
                        st.error("⚠️ Email is required")
                    elif checkout <= checkin:
                        st.error("⚠️ Check-out must be after check-in")
                    else:
                        try:
                            with st.spinner("Processing your booking..."):
                                cust = fetch_one("SELECT * FROM Customer WHERE cust_email=%s", (c_email,))
                                if cust:
                                    cust_id = cust['cust_id']
                                else:
                                    cust_id = execute("INSERT INTO Customer (cust_name, cust_email) VALUES (%s,%s)",
                                                      (c_email.split('@')[0], c_email))
                                
                                call_proc('sp_make_booking', [cust_id, hid, checkin, btype, bdesc, pay_amt])
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
                SELECT b.book_id, b.book_date, b.booking_status, h.hotel_name, b.book_type
                FROM Booking b
                JOIN Hotel h ON h.hotel_id = b.hotel_id
                WHERE b.cust_id = %s
                ORDER BY b.book_date DESC
                LIMIT 5
            """, (cust['cust_id'],))
            
            if bookings:
                for bk in bookings:
                    status_emoji = "✅" if bk['booking_status'] == 'Confirmed' else "⏳" if bk['booking_status'] == 'Pending' else "❌"
                    st.sidebar.markdown(f"""
                        <div class="booking-card">
                            <div style="font-weight: 600; margin-bottom: 5px;">
                                {status_emoji} Booking #{bk['book_id']}
                            </div>
                            <div style="font-size: 0.9rem; color: #555;">
                                🏨 {bk['hotel_name']}<br>
                                📅 {bk['book_date']}<br>
                                👥 {bk['book_type'].title()}<br>
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