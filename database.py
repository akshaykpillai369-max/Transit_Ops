import sqlite3

class Database:

    def __init__(self, db_name= "transport.db"):
        
        self.db_name = db_name
        self.create_table()

    def create_table(self):

        with sqlite3.connect(self.db_name) as conn:

            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vehicles (
                registration_number TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                vehicle_type TEXT NOT NULL,
                max_capacity INTEGER NOT NULL,
                status TEXT DEFAULT 'Available🟢'
            );
            """)


            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Drivers (
                license_number TEXT PRIMARY KEY,
                driver_name TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                status TEXT DEFAULT 'Available🟢'
            );
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Trips (
                trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_reg TEXT NOT NULL,
                driver_license TEXT NOT NULL,
                route_from TEXT NOT NULL,
                route_to TEXT NOT NULL,
                dispatch_date TEXT NOT NULL,
                trip_status TEXT DEFAULT 'Dispatched🟡',
                FOREIGN KEY (vehicle_reg) REFERENCES Vehicles(registration_number),
                FOREIGN KEY (driver_license) REFERENCES Drivers(license_number)
            );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MaintenanceLogs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT,
                    description TEXT,
                    cost REAL,
                    status TEXT, -- 'Open' or 'Closed'
                    start_date TEXT,
                    FOREIGN KEY (registration_number) REFERENCES Vehicles(registration_number)
                )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS FuelLogs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration_number TEXT,
                liters REAL NOT NULL,
                cost REAL NOT NULL,
                log_date TEXT NOT NULL,
                FOREIGN KEY (registration_number) REFERENCES Vehicles(registration_number)
            );
            """)

            conn.commit()

    
    def add_vehicle(self, reg_no, model, v_type, capacity):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO Vehicles (registration_number, model_name, vehicle_type, max_capacity, status)
            VALUES (?, ?, ?, ?, 'Available🟢')
            """
            cursor.execute(query, (reg_no, model, v_type, capacity))
            conn.commit()

    def add_driver(self, license_no, name, expiry):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO Drivers (license_number, driver_name, expiry_date, status)
            VALUES (?, ?, ?, 'Available🟢')
            """
            cursor.execute(query, (license_no, name, expiry))
            conn.commit()

    def get_all_vehicles(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Vehicles")
            return cursor.fetchall()

    def get_all_drivers(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT driver_name, expiry_date, status, license_number FROM Drivers")
            return cursor.fetchall()
        
    def dispatch_trip(self, vehicle_reg, driver_license, route_from, route_to, date_str):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            query = """
            INSERT INTO Trips (vehicle_reg, driver_license, route_from, route_to, dispatch_date)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (vehicle_reg, driver_license, route_from, route_to, date_str))
            
    
            cursor.execute("UPDATE Vehicles SET status = 'On Trip🔴' WHERE registration_number = ?", (vehicle_reg,))
            cursor.execute("UPDATE Drivers SET status = 'On Trip🔴' WHERE license_number = ?", (driver_license,))
            
            conn.commit()

    def get_all_trips(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query = """
            SELECT t.trip_id, v.model_name, d.driver_name, t.route_from, t.route_to, t.dispatch_date, t.trip_status
            FROM Trips t
            JOIN Vehicles v ON t.vehicle_reg = v.registration_number
            JOIN Drivers d ON t.driver_license = d.license_number
            """
            cursor.execute(query)
            return cursor.fetchall()

    def get_available_vehicles(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
          
            cursor.execute("SELECT registration_number, model_name, max_capacity FROM Vehicles WHERE status = 'Available🟢'")
            return cursor.fetchall()

    def get_available_drivers(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT license_number, driver_name FROM Drivers WHERE status = 'Available🟢'")
            return cursor.fetchall()
    
    def complete_trip(self, trip_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
             
            cursor.execute("SELECT vehicle_reg, driver_license FROM Trips WHERE trip_id = ?", (trip_id,))
            result = cursor.fetchone()
            
            if result:
                vehicle_reg, driver_license = result
                
                
                cursor.execute("UPDATE Trips SET trip_status = 'Completed🟢' WHERE trip_id = ?", (trip_id,))
                
                 
                cursor.execute("UPDATE Vehicles SET status = 'Available🟢' WHERE registration_number = ?", (vehicle_reg,))
                cursor.execute("UPDATE Drivers SET status = 'Available🟢' WHERE license_number = ?", (driver_license,))
                
                conn.commit()

    
    def get_dashboard_stats(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM Vehicles")
            total_vehicles = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Vehicles WHERE status = 'On Trip🔴'")
            active_vehicles = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Drivers")
            total_drivers = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Drivers WHERE status = 'Available🟢'")
            available_drivers = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Trips")
            total_trips = cursor.fetchone()[0]
            
            return {
                "total_vehicles": total_vehicles,
                "active_vehicles": active_vehicles,
                "total_drivers": total_drivers,
                "available_drivers": available_drivers,
                "total_trips": total_trips
            }
        
    def add_to_maintenance(self, registration_number, description, cost, start_date):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
             
            cursor.execute("""
                INSERT INTO MaintenanceLogs (registration_number, description, cost, status, start_date)
                VALUES (?, ?, ?, 'Open', ?)
            """, (registration_number, description, cost, start_date))
            
            
            cursor.execute("UPDATE Vehicles SET status = 'In Shop' WHERE registration_number = ?", (registration_number,))
            conn.commit()

    def close_maintenance(self, log_id, registration_number):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
           
            cursor.execute("UPDATE MaintenanceLogs SET status = 'Closed' WHERE log_id = ?", (log_id,))
            
            
            cursor.execute("UPDATE Vehicles SET status = 'Available🟢' WHERE registration_number = ?", (registration_number,))
            conn.commit()

    def get_open_maintenance(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT log_id, registration_number, description, cost, start_date FROM MaintenanceLogs WHERE status = 'Open'")
            return cursor.fetchall()
        

    
    def add_fuel_log(self, reg_no, liters, cost, log_date):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO FuelLogs (registration_number, liters, cost, log_date)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (reg_no, liters, cost, log_date))
            conn.commit()

    def get_vehicle_financials(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query = """
            SELECT 
                v.registration_number, 
                v.model_name,
                COALESCE((SELECT SUM(f.cost) FROM FuelLogs f WHERE f.registration_number = v.registration_number), 0) as total_fuel,
                COALESCE((SELECT SUM(m.cost) FROM MaintenanceLogs m WHERE m.registration_number = v.registration_number), 0) as total_maint
            FROM Vehicles v
            """
            cursor.execute(query)
            return cursor.fetchall()