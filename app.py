import streamlit as st
import time
from database import Database
from menu import Menu

st.set_page_config(
    page_title="TransitOps Platform",
    page_icon="🚚",
    layout="wide"
)

# Initialize Database and Menu controllers
def init_db():
    return Database()

db = init_db()
menu = Menu(db)

# --- ROLE-BASED AUTHENTICATION SECTION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if not st.session_state.authenticated:
    st.title("🔐 TransitOps Gatekeeper Access")
    st.subheader("Please sign in to manage logistics operations")
    
    with st.container(border=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Login as Fleet Manager 🏗️", use_container_width=True):
                if username == "manager" and password == "ops123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Fleet Manager"
                    st.success("Access Granted! Loading Fleet Matrix...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials for Fleet Manager account.")
                    
        with col2:
            if st.button("Login as Financial Analyst 📈", use_container_width=True):
                if username == "analyst" and password == "cash123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Financial Analyst"
                    st.success("Access Granted! Loading Ledger System...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials for Financial Analyst account.")

        with col3:
            if st.button("Login as Super Admin 👑", use_container_width=True):
                if username == "admin" and password == "superops123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Admin"
                    st.success("Access Granted! Loading Master Control Console...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials for Super Admin account.")
                    
    st.info("""💡 **Quick Pass Passwords:**
* **Super Admin (All Access):** `admin` / `superops123`
* **Fleet Manager:** `manager` / `ops123`
* **Financial Analyst:** `analyst` / `cash123`""")
    st.stop() 

# --- LOGOUT BUTTON IN SIDEBAR ---
if st.sidebar.button("Log Out 🚪", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.rerun()

# --- RBAC VIEW NAVIGATION INTERACTION ---
choice = menu.show_sidebar()

# Define explicit view restrictions based on active role profile
manager_only_views = ["Manage Vehicles", "Manage Drivers", "Trip Dispatch", "Maintenance"]
analyst_only_views = ["Fuel & Expenses", "Reports & Analytics"]

# If the logged-in user is 'Admin', they completely bypass these authorization walls
if st.session_state.user_role != "Admin":
    if choice in manager_only_views and st.session_state.user_role != "Fleet Manager":
        st.error(f"🚫 Access Denied: The '{choice}' pane is explicitly restricted to Fleet Manager clearance level only.")
        st.stop()

    if choice in analyst_only_views and st.session_state.user_role != "Financial Analyst":
        st.error(f"🚫 Access Denied: The '{choice}' pane is explicitly restricted to Financial Analyst clearance level only.")
        st.stop()

# --- ROUTING LOGIC BLOCK ---
if choice == "Dashboard":
    st.title("📊 Fleet Dashboard")
    st.caption(f"Active Session Security Context: **{st.session_state.user_role}**")
    
    stats = db.get_dashboard_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.metric(
                label="Fleet Utilization", 
                value=f"{stats['active_vehicles']} / {stats['total_vehicles']}",
                delta="Vehicles currently on road"
            )
            
    with col2:
        with st.container(border=True):
            if stats['available_drivers'] > 0:
                driver_delta = "Drivers ready for dispatch"
                driver_color = "normal"  
                driver_arrow = "auto"
            else:
                driver_delta = "⚠️ NO DRIVERS AVAILABLE"
                driver_color = "red"       
                driver_arrow = "down"      
                
            st.metric(
                label="Driver Availability", 
                value=f"{stats['available_drivers']} / {stats['total_drivers']}",
                delta=driver_delta,
                delta_color=driver_color,
                delta_arrow=driver_arrow
            )
            
    with col3:
        with st.container(border=True):
            st.metric(
                label="Total Operations", 
                value=stats['total_trips'],
                delta="Total shipments handled"
            )
            
    st.markdown("---")
    st.subheader("System Status Overview")
    st.success(f"System fully operational. Authenticated session verified securely as: {st.session_state.user_role}.")
    
elif choice == "Manage Vehicles":
    menu.add_vehicle()
    
elif choice == "Manage Drivers":
    menu.add_driver()
    
elif choice == "Trip Dispatch":
    menu.add_trip()

elif choice == "Maintenance":
    menu.manage_maintenance()

elif choice == "Fuel & Expenses":
    menu.manage_expenses()

elif choice == "Reports & Analytics":
    menu.manage_reports()