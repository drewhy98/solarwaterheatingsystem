import time
import os
import mysql.connector

# ---------------- MySQL Setup ----------------
db_host = os.getenv("MYSQL_HOST", "db")
db_user = os.getenv("MYSQL_USER", "user")
db_password = os.getenv("MYSQL_PASSWORD", "password")
db_name = os.getenv("MYSQL_DATABASE", "solarwaterheatingsystem_db")

conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

# Create table for logging temperatures
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ts1 FLOAT,
    ts2 FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def log_temperature(ts1, ts2):
    cursor.execute("INSERT INTO temperature_logs (ts1, ts2) VALUES (%s, %s)", (ts1, ts2))
    conn.commit()

# ---------------- Countdown Function ----------------
def countdown(t):
    while t > 0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

# ---------------- SWHS Class ----------------
class SolarWaterHeatingSystem:
    def __init__(self):
        self.ts1 = 0
        self.ts2 = 0
        self.pump = False
        self.heater = False
        self.valve = True

    def read_sensors(self):
        self.ts1 = float(input("Enter Temperature Sensor 1 (Gas): "))
        self.ts2 = float(input("Enter Temperature Sensor 2 (Solar): "))
        log_temperature(self.ts1, self.ts2)

    def control_pump(self):
        self.pump = self.ts2 > 4

    def control_heater(self):
        self.heater = (self.ts1 < 4 and self.ts2 < 4) or (self.ts1 - self.ts2 > 20)

    def optimize_temperature_difference(self):
        self.tempdifference = self.ts1 - self.ts2
        print("\nTemperature difference:", self.tempdifference)
        if self.tempdifference >= 20:
            print("High difference: Heating solar tank...")
            while self.tempdifference >= 20:
                self.ts2 += 1
                self.tempdifference -= 1
                print(f"Gas: {self.ts1}, Solar: {self.ts2}, Diff: {self.tempdifference}")
        elif 16 <= self.tempdifference < 20:
            print("Moderate difference: Adjusting pump...")
        elif self.tempdifference < 15:
            print("Low difference: Increasing gas temp...")
            while self.tempdifference < 15:
                self.ts1 += 1
                self.tempdifference += 1
                print(f"Gas: {self.ts1}, Solar: {self.ts2}, Diff: {self.tempdifference}")
        else:
            print("Temperature difference OK.")

    def handle_overheating(self):
        if self.ts1 >= 70:
            print("Emergency: Gas tank overheating!")
            countdown(6)  # For testing
            while self.ts1 >= 70:
                self.ts1 -= 1
                self.valve = False
                self.pump = False
                self.heater = False
                print("Reducing Gas Temp:", self.ts1)
                time.sleep(0.5)
            self.valve = True

    def handle_leakage(self):
        manual_stop = input("Enter 'STOP' to simulate leakage or ENTER to continue: ")
        if manual_stop == 'STOP':
            self.valve = False
            self.pump = False
            self.heater = False
            print("Leakage Emergency!")
            countdown(6)
            check_resolved = input("Issue fixed? (YES/NO): ")
            while check_resolved != 'YES':
                countdown(6)
                check_resolved = input("Issue fixed? (YES/NO): ")
            self.valve = True

    def display_status(self):
        print(f"\nTS1: {self.ts1}°C, TS2: {self.ts2}°C")
        print(f"Pump: {'ON' if self.pump else 'OFF'}, Heater: {'ON' if self.heater else 'OFF'}")
        print("Temp Difference:", self.tempdifference)

    def run(self):
        while True:
            self.read_sensors()
            self.control_pump()
            self.control_heater()
            self.handle_overheating()
            self.optimize_temperature_difference()
            self.display_status()
            self.handle_leakage()
            time.sleep(0.3)

if __name__ == "__main__":
    system = SolarWaterHeatingSystem()
    system.run()
