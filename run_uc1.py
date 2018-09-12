from settings import *

print(irl1)

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