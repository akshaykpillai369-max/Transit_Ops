import streamlit as st
import time

class Menu:
    def __init__(self, db):
        self.db = db

    def show_sidebar(self):
        st.sidebar.title("🚚 TransitOps Menu")
        choice = st.sidebar.radio(
            label= "Navigate to:",
            options= ["Dashboard", "Manage Vehicles", "Manage Drivers", "Trip Dispatch", "Maintenance"]
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

    
    def add_trip(self):
        st.title("🔀 Trip Dispatch & Logistics")
        
        available_vehicles = self.db.get_available_vehicles()
        available_drivers = self.db.get_available_drivers()
        
        st.subheader("Dispatch New Route")
        with st.form("trip_form", clear_on_submit=True):
            
            vehicle_options = [f"{v[0]} ({v[1]})" for v in available_vehicles]
            driver_options = [f"{d[0]} ({d[1]})" for d in available_drivers]
            
            selected_v = st.selectbox("Assign Available Vehicle", options=vehicle_options)
            selected_d = st.selectbox("Assign Available Driver", options=driver_options)
            
            route_from = st.text_input("Origin City (e.g., Kochi)")
            route_to = st.text_input("Destination City (e.g., Bangalore)")
            dispatch_date = st.date_input("Dispatch Date")
            
            submit = st.form_submit_button("Confirm Dispatch 🚀")
            
            if submit:
                if selected_v and selected_d and route_from and route_to:
                
                    vehicle_reg = selected_v.split(" ")[0]
                    driver_license = selected_d.split(" ")[0]
                    date_str = dispatch_date.strftime("%Y-%m-%d")
                    
                    try:
                        self.db.dispatch_trip(vehicle_reg, driver_license, route_from.strip(), route_to.strip(), date_str)
                        st.success(f"Trip successfully dispatched from {route_from} to {route_to}!")
                        time.sleep(2) 
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error dispatching trip: {e}")
                else:
                    st.warning("Please fill out all route details. Ensure you have an available vehicle and driver.")

         
        st.subheader("Active Shipments & Routes")
        trips = self.db.get_all_trips()
        
        if trips:
            cols = st.columns(3)
            for index, trip in enumerate(trips):
                with cols[index % 3]:
                    with st.container(border=True):
                        st.markdown(f"### TRIP ID : #{trips[index][0]}")
                        st.write(f"**易 VEHICLE** : {trips[index][1]}")
                        st.write(f"**👤 DRIVER** : {trips[index][2]}")
                        st.write(f"**📍 ROUTE** : {trips[index][3]} ➡️ {trips[index][4]}")
                        st.write(f"**📅 DATE** : {trips[index][5]}")
                        st.write(f"**STATUS** : {trips[index][6]}")
                        
                        
                        if trips[index][6] == 'Dispatched🟡':
                           
                            if st.button("Mark Completed ✅", key=f"complete_{trips[index][0]}"):
                                self.db.complete_trip(trips[index][0])
                                st.success(f"Trip #{trips[index][0]} completed successfully!")
                                time.sleep(2)
                                st.rerun()
        else:
            st.info("No active trips scheduled at the moment.")


            