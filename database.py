import sqlite3

class Database:

    def __init__(self, db_name= "transport.db"):
        
        self.db_name = db_name
        self.create_table

    def create_table(self):

        with sqlite3.connect(self.db_name) as conn:

            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Vehicles (
                registration_number TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                vehicle_type TEXT NOT NULL,
                max_capacity INTEGER NOT NULL,
                status TEXT DEFAULT 'Available'
            );
            """)


            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Drivers (
                license_number TEXT PRIMARY KEY,
                driver_name TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                status TEXT DEFAULT 'Available'
            );
            """)
            conn.commit()