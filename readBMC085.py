#!/usr/bin/env python
import os,sys,sqlite3,time,paramiko
import Adafruit_BMP.BMP085 as BMP085

remote_host = "<FQDN/IP>"
remote_user = "<user>"
remote_user_priv_key = "/home/pi/.ssh/id_rsa_<user_key>"
remote_script = "/home/<rasp1>/add2rdd.py"

def add2DB(temp,press,my_time):
    mytime = 0
    dbname = "/home/pi/BMP085.db"

    createDB = True if not os.path.isfile(dbname) else False

    #Connecting to the DB
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
    except Exception as e:
        print("Error connecting to %s" % dbname)
        print(e)
        return False

    #If the DB didnt exist, let's create the table
    if createDB:
        try:
            c.execute('''CREATE TABLE BMP085 (date float, temp real, pressure real)''')
        except Exception as e:
            print("Error creating BMP085 table in %s" % dbname)
            print(e)
            return False

    #Inserting data
    try:
        time_mod = int(my_time) % 10
        if time_mod != 0:
            mytime = int(my_time) - time_mod
        else:
            mytime=int(my_time)
        c.execute("INSERT INTO BMP085 VALUES (%f,%r,%r)" % (mytime,temp,press))
    except Exception as e:
        print("Error inserting data into BMP085")
        print(e)
        return False

    #Commit changes
    try:
        conn.commit()
    except Exception as e:
        print("Error commiting changes")
        print(e)
        return False

    conn.close()

    #sending data to external host
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshkey = paramiko.RSAKey.from_private_key_file(remote_user_priv_key)

    try:
        ssh.connect( hostname=remote_host, username=remote_user, pkey=sshkey)
    except paramiko.ssh_exception as e:
    	print("Error connecting to %s" % remote_host)
        print(e)

    try:
    	ssh.exec_command("python %s %s %s %s" % (remote_script,str(mytime),str(temp),str(press)))
    except paramiko.ssh_exception as e:
    	print("Error wrinting temps report to %s" % remote_host)
        print(e)

    ssh.close()

    return True

mytime = int(time.time())
sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
pressure = sensor.read_pressure()
temperature = sensor.read_temperature()

if pressure is not None and temperature is not None:
        if not add2DB(temperature,pressure,mytime):
            print("Error while adding data into DB")
else:
        print 'Failed to get reading. Try again!'
