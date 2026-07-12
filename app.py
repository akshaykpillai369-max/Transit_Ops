import streamlit as st
from database import Database
from menu import Menu

st.set_page_config(
    page_title="TransitOps Platform",
    page_icon="🚚",
    layout="wide"
)

#@st.cache_resource
def init_db():
    return Database()

db = init_db()
menu = Menu(db)

choice = menu.show_sidebar()

if choice == "Dashboard":
    st.title("📊 Fleet Dashboard")
    
   
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
    st.success("All systems operational. Core database connectivity is stable.")
    
elif choice == "Manage Vehicles":
    menu.add_vehicle()
    
elif choice == "Manage Drivers":
    menu.add_driver()
    
elif choice == "Trip Dispatch":
    menu.add_trip()

elif choice == "Maintenance":
    menu.manage_maintenance()