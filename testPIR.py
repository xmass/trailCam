from gpiozero import MotionSensor
import logging
from datetime import datetime
from subprocess import call
import picamera
import time
import os

pir = MotionSensor(17)

print('Starting')

# Wait an initial duration to allow PIR to settle
time.sleep(10)
print('Ready to capture')

ts2 = datetime.now()

while True:
    pir.wait_for_motion()
    logging.info('Motion detected')

    ts1 = datetime.now()
    ts = '{:%Y-%m-%d %H:%M:%S}'.format(ts1)
    delta = ts1-ts2
    print('Motion detected: ' + str(ts) + '=', delta)
   
    # End recording 10s after there is no motion 
    while pir.motion_detected:
        pir.wait_for_no_motion()
        pir.wait_for_motion(10)

    ts2 = datetime.now()
    ts = '{:%Y-%m-%d %H:%M:%S}'.format(ts2)
    delta = ts2-ts1
    print('Motion Ended: ' + str(ts) + ' = ', delta)
