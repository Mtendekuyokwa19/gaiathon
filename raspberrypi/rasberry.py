import time
from datetime import datetime
import sqlitecloud

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print("RPi.GPIO module not found. This code must be run on a Raspberry Pi with RPi.GPIO installed.")
    exit(1)

from dotenv import dotenv_values
config = dotenv_values(".env")
conn = sqlitecloud.connect(config["SQLITE"])
GAS_PIN = 22
TRIG_PIN = 17
ECHO_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(GAS_PIN, GPIO.IN)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.5)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = None
    pulse_end = None

    timeout = time.time() + 1
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            print("Timeout waiting for echo to start.")
            return None

    timeout = time.time() + 1
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            print("Timeout waiting for echo to end.")
            return None

    if pulse_start is None or pulse_end is None:
        print("Echo timings not captured.")
        return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

try:
    while True:
        raw_gas_value = GPIO.input(GAS_PIN)
        gas_detected = raw_gas_value == 0
        gas_sensor_value = 1 if gas_detected else 0
        ultrasonic_value = measure_distance()
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        location = "mubas@designStudio"

        print(f"time: {time_str}, date: {date_str}, location: {location}, ultrasonic_value: {ultrasonic_value}, gas_sensor_value: {gas_sensor_value}")

        query = """
        INSERT INTO sensor_data (time, date, location, ultrasonic_value, gas_sensor_value)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            conn.execute(query, (time_str, date_str, location, ultrasonic_value, gas_sensor_value))
            conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Failed to insert data: {e}")

        time.sleep(3)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
    conn.close()
