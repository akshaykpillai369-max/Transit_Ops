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
    st.info("Dashboard statistics coming soon! Use the sidebar to register vehicles and drivers.")
    
elif choice == "Manage Vehicles":
    menu.add_vehicle()
    
elif choice == "Manage Drivers":
    menu.add_driver()
    
elif choice == "Trip Dispatch":
    menu.add_trip()
