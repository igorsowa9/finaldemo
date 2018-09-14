#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2017

@author: Manuel , Alaa
'''
from __future__ import print_function
from time import time, sleep
from datetime import datetime
import sys
import argparse
import requests
from random import randint
import threading
from flask import Flask, jsonify, abort, make_response, request
from json import dumps 

app = Flask(__name__)

xml_file ='log_msg.xml'

iodef_msg = "{ \"version\": \"2.0\",\
\"xml:lang\": \"en\",\
\"Incident\": [\
{\
\"purpose\": \"ext-value\",\
\"ext-purpose\": \"countermeasurs\", \"IncidentID\": {\
\"id\": 2,\
\"name\": \"CI-SOC1\"\
},\
\"RelatedActivity\": {\
\"IncidentID\": {\
\"id\": \"1\",\
\"name\": \"CI-SOC1\"\
}\
},\
\"GenerationTime\": \"2018-01-18T09:00:00-05:00\",\
\"Contact\": {\
\"type\": \"organization\",\
\"role\": \"creator\"\
},\
\"EventData\":\
{\
\"DetectTime\": \"2018-01-18T09:00:00-05:00\",\
\"Flow\": {\
\"System\": {\
\"category\": \"target\",\
\"Description\": \"37cdc21ab826f120c62a7e9b43faed32\"\
}}},\
\"History\": [\
{\
\"HistoryItem\": {\
\"action\": \"ext-value\",\
\"ext-action\": \"1\",\
\"Description\": \"Update puf\",\
\"DateTime\": \"2018-01-10T07:00:00-02:00\",\
\"AdditionalData\": [\
{\
\"name\": \"CmID\",\
\"dtype\": \"string\",\
\"text\": \"1\"\
},\
{\
\"name\": \"CmDescription\",\
\"dtype\": \"string\",\
\"text\": \"Re-sync PUF challenge\"\
},\
{\
\"name\": \"duration\",\
\"dtype\": \"real\",\
\"text\": \"0.133505\"\
},\
{\
\"name\": \"status\",\
\"dtype\": \"boolean\",\
\"text\": true\
},\
{\
\"name\": \"logtext\",\
\"dtype\": \"string\",\
\"text\": \"{'msg': 'update ok', 'code': 200}\"\
},\
{\
\"name\": \"index\",\
\"dtype\": \"integer\",\
\"text\": 0\
},\
{\
\"name\": \"count\",\
\"dtype\": \"integer\",\
\"text\": 1\
}]}},\
{\
\"HistoryItem\": {\
\"action\": \"ext-value\",\
\"ext-action\": \"2\",\
\"Description\": \"Update puf2\",\
\"DateTime\": \"2018-01-11T07:00:00-02:00\",\
\"AdditionalData\": [\
{\
\"name\": \"CmID\",\
\"dtype\": \"string\",\
\"text\": \"1\"\
},\
{\
\"name\": \"CmDescription\",\
\"dtype\": \"string\",\
\"text\": \"Re-sync PUF challenge\"\
},\
{\
\"name\": \"duration\",\
\"dtype\": \"real\",\
\"text\": \"0.133508\"\
},\
{\
\"name\": \"status\",\
\"dtype\": \"boolean\",\
\"text\": true\
},\
{\
\"name\": \"logtext\",\
\"dtype\": \"string\",\
\"text\": \"{'msg': 'update ok', 'code': 200}\"\
},\
{\
\"name\": \"index\",\
\"dtype\": \"integer\",\
\"text\": 1\
},\
{\
\"name\": \"count\",\
\"dtype\": \"integer\",\
\"text\": 2\
}]}}],\
\"AdditionalData\":\
{\
\"name\": \"CI\",\
\"dtype\": \"string\",\
\"text\": \"Energy\"\
}\
}]\
}"

# will create a idmef object with sample log data 
#idmef_msg= full_message(CI= 'Energy', analyzer_id= 'SA1', analyzer_name ='SA Node 1',\
#                                                    _text="Oct 6 08:24:35: %LINK-3-UPDOWN: Interface FastEthernet5/1.1, changed state to up Oct 6 08:24:35: %LINK-3-UPDOWN: Interface FastEthernet5/1.2, changed state to up Oct 6 08:24:35: %LINK-3-UPDOWN: Interface FastEthernet5/1.3, changed state to up Oct 6 08:24:35: %LINK-3-UPDOWN: Interface FastEthernet5/1.4, changed state to up Oct 6 08:24:36: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet5/1.1, changed state to up Oct 6 08:24:36: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet5/1.2, changed state to up Oct 6 08:24:36: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet5/1.3, changed state to up Oct 6 08:24:36: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet5/1.4, changed state to up Jun 29 12:51:26.887 : ifmgr[142]:%PKT_INFRA-LINK-3-UPDOWN : Interface GigabitEthernet0/4/0/0, changed state to Up Jun 29 12:51:26.897 : ifmgr[142]:%PKT_INFRA-LINEPROTO-6-UPDOWN : Line protocol on Interface GigabitEthernet0/4/0/0, changed state to Up Jun 29 12:51:32.375 : ifmgr[142]: %PKT_INFRA-LINK-3-UPDOWN : Interface GigabitEthernet0/4/0/0, changed state to Down")  
#suppress flask output
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def _send(payload):
    """Send payload to SDC"""
    if type(payload) != "str":
        payload = dumps(payload)

    con = True
    while con:
        try:
            r = requests.post(args.sdc_rest_uri, json=payload)
            print("%s - CISOC-Simulator: Send payload: %s" %(current_time(), str(payload)[:50]))
            con = False
        except Exception as e:
            print("%s - CISOC-Simulator: Cannot connect to SDC... waiting" %current_time())
            sleep(1)
            
def _send_xml(payload): 
    """Send log file xml payload to SDC"""
    con = True
    while con:
        try:
            #r = requests.post(args.sdc_rest_uri, data=open(payload).read())
            #print("%s - CISOC-Simulator: Send xml payload: %s" %(current_time(), payload))
            r = requests.post(args.sdc_rest_uri, json=payload)
            print("%s - CISOC-Simulator: Send xml payload: %s" %(current_time(), str(payload)[:100]))
            con = False
        except Exception as e:
            print("%s - CISOC-Simulator: Cannot connect to SDC... waiting" %current_time())
            sleep(1)
    
def simulate():
    while True:
        #message = "{\"attr1\": %s}" %randint(0, 100)
        #message = {"attr1": randint(0, 100)}
        
        #simulate incident report
       _send(iodef_msg)
        
        #simulate log file 
        #idmef_msg =  ('../data/log_msg.xml') # just example of recieved idmef message in xml format contains log data SAVED LOCALY
        #print(idmef_msg)
        #print ('sending xml log file to SDC')
        #print ("%s" %idmef_msg)
       #_send_xml("%s" %idmef_msg)      
        
        
       sleep(args.sleep_time)
    
def current_time():
    """return the current time in the format YYYY-mm-dd HH:MM.SS"""
    return datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/rest/api/data', methods=['POST'])
def create_new_line():
    # check if request is of type json and every required variable is filled
    if (not request.json):
        print('Request not of type JSON')
        abort(400)
    
    print("%s - CISOC-Simulator: Received payload: %s" %(current_time(), request.json[:250]))
    return "Success!\n", 201


def run_it(message):
    parser = argparse.ArgumentParser(description='Start the KDD Data Simulator')
    parser.add_argument("--sleep_time", dest="sleep_time", type=float, default=1, help="Set time to sleep between two messages (default: 1)")
    parser.add_argument("--api_port", dest="api_port", type=int, default=5002, help="Port of REST API (default: 5002)")
    parser.add_argument("--sdc_rest_uri", dest="sdc_rest_uri", type=str, default="http://10.12.0.74:5000/rest/api/v1/new/cisoc", \
                        help="REST URI for SDC (default: http://10.12.0.74:5000/rest/api/v1/new/cisoc)")
    
    args = parser.parse_args()

    t1 = threading.Thread(target=simulate)
    t1.daemon = True
    t2 = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": args.api_port})
    t2.daemon = True
     
    t1.start()
    t2.start()

    while True:
        sleep(1)

