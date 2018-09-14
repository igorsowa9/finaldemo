from settings import *
from time import time, sleep
import psycopg2
import sys
import numpy as np
from datetime import datetime
import paho.mqtt.client as paho
import CI_SOC_Simulator_mod


Z_treshold_default = 0.1  # Hz
reconnection_delay_default = 10  # seconds


def db_connection(dbname):
    """
    Connection to the database of SAU
    :param: str of db name
    :return: instance pf connection from psycopg2 pointing at dbname from input.
    """
    try:
        global conn
        conn = psycopg2.connect("dbname='" + dbname + "' user='postgres' host='" + ip_database + "' password='postgres'")
        print("DB: " + dbname + " connected.")
        return(conn)
    except:
        print("I am unable to connect to the database ("+dbname+"). STOP.")
        sys.exit(0)


def on_publish(client, userdata, result):
    print("data of instability published.")
    pass


def verify_stability(reconnection_delay=reconnection_delay_default, Z_treshold=Z_treshold_default):

    # download recent Rocof based on PMU from DB
    conn = db_connection("irldb")
    cursor = conn.cursor()

    lab_ts_utc = datetime.utcnow()

    cursor.execute(
        "SELECT * FROM public.irldata_pmu WHERE server_time > " + str(lab_ts_utc) + "ORDER BY server_time;")
        # further selection to select the last value of the appropriate PMU etc. Only one should be left
    rocof = cursor.fetchall()
    if not len(rocof) == 1:
        print("too many SELECTED.")

    # compare with Z_treshold
    if rocof > Z_treshold:

        # disconnect_cb()
        broker = "10.12.0.1"  # CB control module should subscribe to this broker and the topic below
        port = 1883
        client1 = paho.Client("control1")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        ret = client1.publish("norm1/cb", "1")  # 1 means trigger CB

        # send to dashboard and cisan:
        message = "norm1 disconnected"
        CI_SOC_Simulator_mod.run_it(message)
        # send_to_dashboard() - send change to the webpage to show result of instability detection

        # reconnect after reconnection_delay value
        sleep(reconnection_delay)
        ret = client1.publish("norm1/cb", "0")
        # send_to_dashboard() - send change to the webpage to show result of instability detection


if __name__ == '__main__':

    np.set_printoptions(suppress=True)
    # catch the request from TSO
    # ...
    Z_treshold = 0.1  # from TSO message
    reconnection_delay = 1  # from TSO message

    TSOrequest = False
    while True:
        sleep(1)
        # check TSO
        if TSOrequest:
            verify_stability(reconnection_delay, Z_treshold)




### BASIC LOOP - not necessary
    # SecA sends measures to CI-SOC
    # CI-SOC detects threats, if so sends to CI-SOC Dashboard
    # CI-SOC Dashboard applies conutermesaures if detected

### IRISH SCENARIO - simplifications:
    # CI-SOC and Dashboard together
    # SecA and NORM/SMX together

# TSO sends break circuit request of check the grid stability to Dashboard
    # TSOrequest.py script executing the request send

# Dashboard-CISOC receives the request and sends it the "grid stability check" request to SecA
    #

# SecA forwards the request to NORM/SMX actuator

# SMX triggers the CB, reconnects after some time