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
        

    
        
    