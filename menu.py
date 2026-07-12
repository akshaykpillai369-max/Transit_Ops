import streamlit as st

class Menu:
    def __init__(self, db):
        self.db = db

    def show_sidebar(self):
        st.sidebar.title("🚚 TransitOps Menu")
        choice = st.sidebar.radio(
            label= "Navigate to:",
            options= ["Dashboard", "Manage Vehicles", "Manage Drivers", "Trip Dispatch"]
        )
        return choice
    
    def add_vehicle(self):
        st.title("🚛 Vehicle Fleet Management")
        
        #Registration Form
        st.subheader("Register New Vehicle")
        with st.form("vehicle_form", clear_on_submit=True):
            reg_no = st.text_input("Registration Number (e.g., KL-01-AB-1234)")
            model = st.text_input("Model Name (e.g., Tata Ultra)")
            v_type = st.selectbox(label="Vehicle Type",options= ["Truck", "Mini-Van", "Container", "Flatbed"])
            capacity = st.number_input("Max Capacity (in kg)", min_value=1, step=100)
            
            submit = st.form_submit_button("Add Vehicle")
            if submit:
                if reg_no and model:
                    try:
                        self.db.add_vehicle(reg_no.upper().strip(), model, v_type, capacity)
                        st.success(f"Vehicle {reg_no} successfully added to the fleet!")
                    except Exception as e:
                        st.error(f"Error adding vehicle: {e} (Check for duplicate numbers)")
                else:
                    st.warning("Please fill out all fields.")
        
        #Display existing vehicles
        st.subheader("Current Fleet Registry")
        vehicles = self.db.get_all_vehicles()
        if vehicles:
            st.dataframe(vehicles, column_config={
                0: "Reg Number",
                1: "Model",
                2: "Type",
                3: "Capacity (kg)",
                4: "Current Status"
            })
        else:
            st.info("No vehicles registered yet.")