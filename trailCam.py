from gpiozero import MotionSensor
import logging
from datetime import datetime
from subprocess import call
import picamera
import time
import os

if not os.path.exists('/home/pi/trailcam_log'):
    os.makedirs('/home/pi/trailcam_log')

if not os.path.exists('/home/pi/videos'):
    os.makedirs('/home/pi/videos')

logfile = "/home/pi/trailcam_log/trailcam_log-"+str(datetime.now().strftime("%Y%m%d-%H%M"))+".csv"
logging.basicConfig(filename=logfile, level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S,')

pir = MotionSensor(17)

print('Starting')
logging.info('Starting')

# Wait an initial duration to allow PIR to settle
time.sleep(10)
ts2 = datetime.now()

while True:
    pir.wait_for_motion()
    ts1 = datetime.now()
    timestamp = '{:%Y%m%d-%H%M%S}'.format(ts1)
    logging.info('Slept for: ' + str(ts1-ts2))
    logging.info('Motion detected starting to capture: '+ str(timestamp)+'.jpg')
    print('Motion detected beginning capture')
    with picamera.PiCamera() as cam:
        cam.resolution=(1024,768)
        cam.annotate_background = picamera.Color('black')

        cam.start_recording('/home/pi/video.h264')
        # End recording after timeout when there is no motion
        while pir.motion_detected:
            cam.annotate_text = "Spy 1 "+datetime.now().strftime('%d-%m-%y %H:%M:%S')
            pir.wait_for_no_motion()
            cam.wait_recording()
            pir.wait_for_motion(10)
            cam.wait_recording()

        print('Motion Ended')
        cam.stop_recording()
    time.sleep(0.5)
    ts2 = datetime.now()
    timestamp = ts2.strftime('%d-%m-%y_%H-%M-%S')
    input_video = "/home/pi/video.h264"

    logging.info('Attempting to save capture')

    if os.path.isdir('mnt/usb/videos'):
        logging.info('Saving to /mnt/usb/videos/')
        output_video = "/mnt/usb/videos/{}.mp4".format(timestamp)
    elif os.path.isdir('mnt/usb1/videos'):
        logging.info('Saving to /mnt/usb1/videos/')
        output_video = "/mnt/usb1/videos/{}.mp4".format(timestamp)
    elif os.path.isdir('mnt/usb2/videos'):
        logging.info('Saving to /mnt/usb2/videos/') 
        output_video = "/mnt/usb2/videos/{}.mp4".format(timestamp)
    else:
        logging.info('Saving to /home/pi/videos/')
        output_video = "/home/pi/videos/{}.mp4".format(timestamp)

    call(["MP4Box", "-add", input_video, output_video])
    print('Motion Ended')
    logging.info('Motion Ended duration: ' + str(ts2-ts1))
