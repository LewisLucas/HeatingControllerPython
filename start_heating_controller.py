
import sqlite3
import datetime
import time as t


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

    return time, temperature, humidity, target_temperature, power

def update_current_temperate(temperature):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE HeatingApp_info SET temperature = {temperature} WHERE id = 1")
    conn.commit()
    conn.close()

def send_signal(state):
    if state == "on":
        print("Turning on")
    else:
        print("Turning off")

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
    return timer

while True:
    # path to the database
    db_path = 'db.sqlite3'

    # try to get the info from the database
    try:
        time, temperature, humidity, target_temperature, power = get_info()
    except:
        print("Error getting info")
        continue

    while power:
        t.sleep(1) # sleep for 1 second
        try:
            time, temperature, humidity, target_temperature, power = get_info()
        except:
            print("Error getting info")
            continue

        delete_old_timers()
        check_and_activate_timers()








