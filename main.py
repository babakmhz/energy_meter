import os
import glob
import time
from database import db
import threading
import datetime
import random
import subprocess
#--------------------------------------------
try:
    uptime = int(subprocess.check_output('tail -n 1 uptime.txt',shell=True))
except:
    uptime = 0
#--------------------------------------------
def uptime_counter():
    global uptime
    while True:
        uptime+=1
        os.system('echo '+str(uptime)+'>uptime.txt')
        time.sleep(1)
#--------------------------------------------
sensor_on_min_threshold = 24.0
sensor_on_max_threshold = 26.0
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')
today = datetime.datetime.now().date()
today_id = 0
threads = list()
sensors = dict()
timer_thread = threading.Thread(target=uptime_counter,args=())
timer_thread.start()
index = 1
for device in device_folder:
    sensors[index] = device
    index+=1
print(sensors)
db = db()
db.insertSensors(sensors)
def updateUptime(date,uptime):
    db.updateUptime(date,uptime)

def insert_new_day(date):
    global today_id
    today_id = db.insertNewUptimeDate(str(date))
    print('today id is : ' ,today_id)
def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(file):
    lines = read_temp_raw(file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def update_consuming(db_class,tag,con_time):
    db_class.updateConsumeTime(today_id,time,tag)
def handle_sensor(tag,device_file):
    from database import db
    while True:
        con_time = 0
        consumed = False
        this_sensor = device_file + '/w1_slave'
        print(read_temp(this_sensor))
        this_temp = read_temp(this_sensor)[0]
        while this_temp>=sensor_on_min_threshold and this_temp<=sensor_on_max_threshold:
            con_time+=1
            time.sleep(1)
            consumed = True
            print('consuming...!sensor number: '+str(tag),con_time,this_temp,sensor_on_min_threshold,sensor_on_max_threshold)
            this_temp = read_temp(this_sensor)[0]
        if consumed:
           db_class = db()
           db_class.updateConsumeTime(today_id,con_time,tag)
           db_class.closedb()
           print('uptime updated')
           consumed = False
        time.sleep(2)

insert_new_day(today)
print('global today_id is :',today_id)
index = 1
for file in device_folder:
    this_thread = threading.Thread(target=handle_sensor,args=(index,file,))
    threads.append(this_thread)
    this_thread.start()
    index+=1
print(threads)


while True:
    if(str(today)!=str(datetime.datetime.now().date())):
       updateUptime(str(today),uptime)
       uptime=0
       today = datetime.datetime.now().date()
       insert_new_day(str(today))
       print('this is not today')
    time.sleep(60)
