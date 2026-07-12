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
            
        self.get_all_vehicles()
        

    def get_all_vehicles(self):
        st.subheader("Current Fleet Registry🚚")
        vehicles = self.db.get_all_vehicles()

        cols = st.columns(3) 

        if vehicles:

            for index, vehicle in enumerate(vehicles):
                

                with cols[index % 3]: 
                    
                    with st.container(border= True) :

                        st.markdown(f"### MODEL : {vehicles[index][1]}")
                        st.write(f"**REG NUMBER** : {vehicles[index][0]}")
                        st.write(f"**TYPE** : {vehicles[index][2]}")
                        st.write(f"**CAPACITY(kg)** : {vehicles[index][3]}")
                        st.write(f"**CURRENT STATUS** : {vehicles[index][4]}")
        else:
            st.info("No Vehicles Registered Yet.")


    def add_driver(self):
        st.title("👤 Driver Directory")
        
        #Driver Registration Form
        st.subheader("Register New Driver")
        with st.form("driver_form", clear_on_submit=True):
            license_no = st.text_input("License Number")
            name = st.text_input("Full Name")
            expiry = st.date_input("License Expiry Date")
            
            submit = st.form_submit_button("Add Driver")
            if submit:
                if license_no and name:
                    expiry_str = expiry.strftime("%Y-%m-%d")
                    try:
                        self.db.add_driver(license_no.upper().strip(), name, expiry_str)
                        st.success(f"Driver {name} registered successfully!")
                    except Exception as e:
                        st.error(f"Error adding driver: {e}")
                else:
                    st.warning("Please fill out all fields.")
                    
        self.get_all_drivers()

    
    def get_all_drivers(self):
        st.subheader("Registered Drivers")
        drivers = self.db.get_all_drivers()

        cols = st.columns(3) 

        if drivers:

            for index, driver in enumerate(drivers):
                

                with cols[index % 3]: 
                    
                    with st.container(border= True) :

                        st.markdown(f"### NAME : {drivers[index][0]}")
                        st.write(f"**LICENSE NUMBER** : {drivers[index][3]}")
                        st.write(f"**EXPIRY** : {drivers[index][1]}")
                        st.write(f"**CURRENT STATUS** : {drivers[index][2]}")
        else:
            st.info("**No Drivers Registered Yet.**")