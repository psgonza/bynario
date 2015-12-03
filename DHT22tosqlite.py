#!/usr/bin/env python
import os,sys,sqlite3,datetime
import Adafruit_DHT


def add2DB(temp,hum):
    dbname = "temperatures.db"
    mytime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

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
            c.execute('''CREATE TABLE DHT22 (date text, temp rel, humidity real)''')
        except Exception as e:
            print("Error creating DHT22 table in %s" % dbname)
            print(e)
            return False

    #Inserting data
    try:
        c.execute("INSERT INTO DHT22 VALUES ('" + mytime + "'," + str(temp) + "," + str(hum) + ")")
    except Exception as e:
        print("Error inserting data into DHT22")
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

    return True

sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
        if not add2DB(temperature,humidity):
            print("Error while adding data into DB")
else:
        print 'Failed to get reading. Try again!'
