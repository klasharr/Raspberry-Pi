import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging
from rstoys import realtime

# https://pypi.org/project/rstoys/

logging.basicConfig(level=logging.INFO, filename='motion.log')

INPUT_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)

every_5_secs = realtime.Interval(5.0)
loop_interval_in_secs = 1.5

def update(elapsed_time, delta_time):
    
    input_state = GPIO.input(INPUT_PIN)
    if input_state == True:
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	message = "Motion detected - " + dt_string
        print(message)
        logging.info(message)

    if every_5_secs.should(delta_time):
        print(".")

realtime.loop(update, loop_interval_in_secs)