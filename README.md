# Trail Camera
Trigger camera recoring while there is a movement identified by the PIR sensor.

## prerequisites
enabled camera in raspi-config
python3 python3-gpiozero python3-picamera gpac

## using nonstadart user
make sure user is in groups: video gpio

## run after boot
 add to /etc/rc.local before exit 0:
 /usr/bin/python3 /home/<...>/trailCam.py &


Original code taken from: https://peaknature.co.uk/blog/how-to-build-a-raspberry-pi-trail-cam--part-2-software-setup
