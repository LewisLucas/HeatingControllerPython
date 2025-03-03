
import sqlite3
import datetime
import time as t
import requests


def create_info_if_not_exists():
    # if the info table is empty create an entry
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HeatingApp_info")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO HeatingApp_info VALUES (1, '2021-01-01 00:00:00', 21, 50, 10, 1, 0)")

def get_info():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HeatingApp_info WHERE id = 1")
    info = cursor.fetchone()
    conn.close()
    id = info[0]
    time = info[1]
    temperature = info[2]
    humidity = info[3]
    target_temperature = info[4]
    power = info[5]
    updated = info[6]
    return time, temperature, humidity, target_temperature, power, updated

def update_current_temperature_and_humidity(humidity, temperature):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE HeatingApp_info SET temperature = {temperature} WHERE id = 1")
    cursor.execute(f"UPDATE HeatingApp_info SET humidity = {humidity} WHERE id = 1")
    conn.commit()
    conn.close()

def set_target_temperature(target_temperature):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE HeatingApp_info SET target_temperature = {target_temperature} WHERE id = 1")
    conn.commit()
    conn.close()

def set_power(power):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE HeatingApp_info SET power = {power} WHERE id = 1")
    conn.commit()
    conn.close()

def send_signal(state):
    if state == "on":
        try:
            print(requests.get(f"{url}/on"))
        except:
            print("Error sending signal")
    else:
        try:
            print(requests.get(f"{url}/off"))
        except:
            print("Error sending signal")

def get_timers():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HeatingApp_timer")
    timers = cursor.fetchall()
    conn.close()
    return timers

def delete_timer(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM HeatingApp_timer WHERE id = {id}")
    conn.commit()
    conn.close()

def activate_timer(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE HeatingApp_timer SET active = 1 WHERE id = {id}")
    conn.commit()
    conn.close()

def delete_old_timers():
    timers = get_timers()
    for timer in timers:
        start = datetime.datetime.strptime(timer[1], "%Y-%m-%d %H:%M:%S").timestamp()
        end = datetime.datetime.strptime(timer[2], "%Y-%m-%d %H:%M:%S").timestamp()
        if end < datetime.datetime.now().timestamp():
            delete_timer(timer[0])
            print(f"Deleted timer {timer[0]}")

def check_and_activate_timers():
    for timer in get_timers():
        start = datetime.datetime.strptime(timer[1], "%Y-%m-%d %H:%M:%S").timestamp()
        if start <= datetime.datetime.now().timestamp() and not timer[3]:
            activate_timer(timer[0])
            print(f"Activated timer {timer[0]}")

def get_active_timer():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HeatingApp_timer WHERE active = 1")
    timer = cursor.fetchone()
    conn.close()
    if timer:
        return timer
    else:
        return None
    
def clear_updated():
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()
    cursor.execute("UPDATE HeatingApp_info SET updated = 0 WHERE id = 1")
    conn.commit()
    conn.close()
    
def maintain_temperature(temperature, target_temperature):
    if temperature < target_temperature:
        send_signal("on")
    else:
        send_signal("off")
# path to the database
db_path = 'db.sqlite3'
url = "http://192.168.0.87"
create_info_if_not_exists()

# signal delay timer in minutes to not send too many signals
signal_delay = 5
signal_delay_ignore = True
last_signal = datetime.datetime.now()
while True:
    # Wait for the power to be on else just loop infinitely
    power = get_info()[5]
    while power:
        try:
            time, temperature, humidity, target_temperature, power, updated = get_info()
        except:
            print("Error getting info")
            continue

        delete_old_timers()
        check_and_activate_timers()
        timer = get_active_timer()
        if timer:
            if timer[4] != target_temperature:
                set_target_temperature(timer[4])
                print(f"Changed target temperature to {timer[4]}")
        
        if updated:
            clear_updated()
            signal_delay_ignore = True

        if (datetime.datetime.now() - last_signal).seconds > signal_delay * 60 or signal_delay_ignore:
            maintain_temperature(temperature, target_temperature)
            last_signal = datetime.datetime.now()
            signal_delay_ignore = False
        else:
            print("Delaying signal")
            continue
    t.sleep(10)
