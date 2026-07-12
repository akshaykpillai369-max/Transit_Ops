import streamlit as st
import time

class Menu:
    def __init__(self, db):
        self.db = db

    def show_sidebar(self):
        st.sidebar.title("🚚 TransitOps Menu")
        choice = st.sidebar.radio(
            label= "Navigate to:",
            options= ["Dashboard", "Manage Vehicles", "Manage Drivers", "Trip Dispatch", "Maintenance", "Fuel & Expenses", "Reports & Analytics"]
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

        if vehicles:
            cols = st.columns(3)
            for index, vehicle in enumerate(vehicles):
                with cols[index % 3]: 
                    with st.container(border=True):
                        st.markdown(f"### MODEL : {vehicle[1]}")
                        st.write(f"**REG NUMBER** : {vehicle[0]}")
                        st.write(f"**TYPE** : {vehicle[2]}")
                        st.write(f"**CAPACITY(kg)** : {vehicle[3]}")
                        st.write(f"**CURRENT STATUS** : {vehicle[4]}")
        else:
            st.info("No Vehicles Registered Yet.")


    def add_driver(self):
        st.title("👤 Driver Directory")
        import datetime
        
        # Driver Registration Form
        st.subheader("Register New Driver")
        with st.form("driver_form", clear_on_submit=True):
            license_no = st.text_input("License Number")
            name = st.text_input("Full Name")
            expiry = st.date_input("License Expiry Date")
            
            submit = st.form_submit_button("Add Driver")
            if submit:
                if license_no and name:
        
                    if expiry < datetime.date.today():
                        st.error(f"❌ Registration Denied: Driver's license expired on {expiry.strftime('%Y-%m-%d')}!")
                    else:
                        expiry_str = expiry.strftime("%Y-%m-%d")
                        try:
                            self.db.add_driver(license_no.upper().strip(), name, expiry_str)
                            st.success(f"Driver {name} registered successfully!")
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding driver: {e}")
                else:
                    st.warning("Please fill out all fields.")
                    
        self.get_all_drivers()
    
    def get_all_drivers(self):
        st.subheader("Registered Drivers")
        import datetime
        drivers = self.db.get_all_drivers()
        current_date = datetime.date.today().strftime("%Y-%m-%d")

        if drivers:
            cols = st.columns(3)
            for index, driver in enumerate(drivers):
                 
                is_expired = driver[1] < current_date
                display_status = "⚠️ EXPIRED / NON-COMPLIANT" if is_expired else driver[2]
                
                with cols[index % 3]: 
                    with st.container(border=True):
                        st.markdown(f"### NAME : {driver[0]}")
                        st.write(f"**LICENSE NUMBER** : {driver[3]}")
                        st.write(f"**EXPIRY** : {driver[1]}")
                        
                        if is_expired:
                            st.markdown(f"**CURRENT STATUS** : :red[{display_status}]")
                        else:
                            st.write(f"**CURRENT STATUS** : {display_status}")
        else:
            st.info("**No Drivers Registered Yet.**")

    
    def add_trip(self):
        st.title("🔀 Trip Dispatch & Logistics")
        
        available_vehicles = self.db.get_available_vehicles()
        available_drivers = self.db.get_available_drivers()
        
        st.subheader("Dispatch New Route")
        with st.form("trip_form", clear_on_submit=True):
            vehicle_options = [f"{v[0]} | {v[1]} (Max: {v[2]}kg)" for v in available_vehicles]
            driver_options = [f"{d[0]} | {d[1]}" for d in available_drivers]
            
            selected_v = st.selectbox("Assign Available Vehicle", options=vehicle_options)
            selected_d = st.selectbox("Assign Available Driver", options=driver_options)
            
            route_from = st.text_input("Origin City (e.g., Kochi)")
            route_to = st.text_input("Destination City (e.g., Bangalore)")
            cargo_weight = st.number_input("Cargo Weight (in kg)", min_value=1, step=50)
            dispatch_date = st.date_input("Dispatch Date")
            
            submit = st.form_submit_button("Confirm Dispatch 🚀")
            
            if submit:
                if selected_v and selected_d and route_from and route_to:
                     
                    vehicle_reg = selected_v.split(" | ")[0].strip()
                    driver_license = selected_d.split(" | ")[0].strip()
                    date_str = dispatch_date.strftime("%Y-%m-%d")
                    
                    try:
                        max_capacity = int(selected_v.split("(Max: ")[1].split("kg)")[0])
                    except:
                        max_capacity = 0

                    if cargo_weight > max_capacity:
                        st.error(f"❌ Dispatch Denied: Cargo weight ({cargo_weight}kg) exceeds capacity ({max_capacity}kg)!")
                    else:
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
                        st.markdown(f"### TRIP ID : #{trip[0]}")
                        st.write(f"**🚛 VEHICLE** : {trip[1]}")
                        st.write(f"**👤 DRIVER** : {trip[2]}")
                        st.write(f"**📍 ROUTE** : {trip[3]} ➡️ {trip[4]}")
                        st.write(f"**📅 DATE** : {trip[5]}")
                        st.write(f"**STATUS** : {trip[6]}")
                        
                        if trip[6] == 'Dispatched🟡':
                            if st.button("Mark Completed ✅", key=f"complete_{trip[0]}"):
                                self.db.complete_trip(trip[0])
                                st.success(f"Trip #{trip[0]} completed successfully!")
                                time.sleep(2)
                                st.rerun()
        else:
            st.info("No active trips scheduled at the moment.")

    def manage_maintenance(self):
        st.title("🔧 Maintenance & Shop Log")
        
        tab1, tab2 = st.tabs(["⚠️ Send Vehicle to Shop", "✅ Active Workshop Logs"])
        
        with tab1:
            st.subheader("Log New Maintenance Order")
           
            available_vehicles = self.db.get_available_vehicles()
            
            if not available_vehicles:
                st.info("No available vehicles to send to maintenance.")
            else:
                with st.form("maintenance_form", clear_on_submit=True):
                
                    vehicle_options = [f"{v[0]} - {v[1]}" for v in available_vehicles]
                    selected_v = st.selectbox("Select Vehicle", vehicle_options)
                    
                    desc = st.text_area("Issue Description (e.g., Oil Change, Brake Replacement)")
                    cost = st.number_input("Estimated Cost", min_value=0.0, step=500.0)
                    date = st.date_input("Service Date")
                    
                    submit_m = st.form_submit_button("Send to Workshop")
                    if submit_m and desc:
                        reg_num = selected_v.split(" - ")[0]
                        try:
                            self.db.add_to_maintenance(reg_num, desc, cost, str(date))
                            st.success(f"Vehicle {reg_num} status changed to 'In Shop'!")
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error logging maintenance: {e}")

        with tab2:
            st.subheader("Vehicles Currently In Shop")
            open_logs = self.db.get_open_maintenance()
            
            if not open_logs:
                st.success("🎉 Workshop clear! No vehicles currently under maintenance.")
            else:
                for log in open_logs:
                    log_id, reg, desc, cost, start_date = log
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**Vehicle:** {reg}")
                            st.markdown(f"**Issue:** {desc}")
                            st.caption(f"Started: {start_date} | Est. Cost: {cost}")
                        with col2:
                            if st.button("Complete & Release", key=f"rel_{log_id}"):
                                self.db.close_maintenance(log_id, reg)
                                st.success(f"Vehicle {reg} released back to operational service!")
                                time.sleep(2)
                                st.rerun()
    

    def manage_expenses(self):
        st.title("⛽ Fuel & Expense Management")
        
        tab1, tab2 = st.tabs(["📝 Log Fuel Purchase", "📊 Fleet Expense Summary"])
        
        with tab1:
            st.subheader("Record Fuel Receipt")
            all_vehicles = self.db.get_all_vehicles()
            
            if not all_vehicles:
                st.info("Please register a vehicle first.")
            else:
                with st.form("fuel_form", clear_on_submit=True):
                    vehicle_options = [f"{v[0]} ({v[1]})" for v in all_vehicles]
                    selected_v = st.selectbox("Select Vehicle", options=vehicle_options)
                    
                    liters = st.number_input("Fuel Volume (Liters)", min_value=1, step=10)
                    cost = st.number_input("Total Cost (₹)", min_value=0, step=1000)
                    log_date = st.date_input("Transaction Date")
                    
                    submit = st.form_submit_button("Save Fuel Log")
                    if submit:
                        reg_no = selected_v.split(" ")[0]
                        self.db.add_fuel_log(reg_no, liters, cost, log_date.strftime("%Y-%m-%d"))
                        st.success(f"Fuel log successfully recorded for {reg_no}!")
                        import time
                        time.sleep(2)
                        st.rerun()
                        
        with tab2:
            st.subheader("Operational Expense Ledger")
            financials = self.db.get_vehicle_financials()
            
            if not financials:
                st.info("No logs on record.")
            else:
                for row in financials:
                    reg, model, fuel_cost, maint_cost = row
                    total_combined = fuel_cost + maint_cost
                    
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.markdown(f"**{reg}**  \n*{model}*")
                        c2.metric("Fuel Costs", f"₹{fuel_cost:,.2f}")
                        c3.metric("Maintenance Costs", f"₹{maint_cost:,.2f}")
                        c4.metric("Total Cost", f"₹{total_combined:,.2f}")

    

    def manage_reports(self):
        import pandas as pd
        st.title("📊 Reports & Performance Analytics")
        
        raw_data = self.db.get_analytics_report()
        
        if not raw_data:
            st.info("No system metrics recorded yet to process analytical tracking data.")
            return

        processed_rows = []
        for row in raw_data:
            reg, model, v_type, liters, fuel_cost, maint_cost, trips = row
            
            total_op_cost = fuel_cost + maint_cost
            estimated_distance = trips * 150 # Mock assumption of baseline route distance (150km)
            fuel_efficiency = round(estimated_distance / liters, 2) if liters > 0 else 0.0
            
            # ROI Formula: (Revenue - Expenses) / Assumed Asset Baseline
            mock_revenue = trips * 12000
            mock_acquisition_cost = 2500000 
            roi = round(((mock_revenue - total_op_cost) / mock_acquisition_cost) * 100, 2)
            
            processed_rows.append({
                "Vehicle Reg": reg,
                "Model Name": model,
                "Type": v_type,
                "Completed Trips": trips,
                "Est Distance (km)": estimated_distance,
                "Fuel Liters": liters,
                "Total Op Cost (₹)": total_op_cost,
                "Efficiency (km/L)": fuel_efficiency,
                "Estimated ROI (%)": f"{roi}%"
            })
            
        df = pd.DataFrame(processed_rows)
        
        st.subheader("🚚 Fleet Efficiency & ROI Summary Table")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.subheader("💾 Export Document Records")
        csv_data = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Analytics Report as CSV",
            data=csv_data,
            file_name="transitops_fleet_analytics.csv",
            mime="text/csv"
        )