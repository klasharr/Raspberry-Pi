import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging
from rstoys import realtime
from gpiozero import LED
import httplib, urllib
from ratelimit import limits

logging.basicConfig(level=logging.INFO, filename='motion.log')

INPUT_PIN = 18
red_led = LED(21)

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)

every_5_secs = realtime.Interval(5.0)
loop_interval_in_secs = 1.5

@limits(calls=1, period=15)
def send_message():
    try:
        conn = httplib.HTTPSConnection("api.pushover.net:443", timeout=3)
        conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": "XXXXX",
            "user": "XXXXXX",
            "sound": "siren",
            "message": 'movement',
        }), { "Content-type": "application/x-www-form-urlencoded" })
        response = conn.getresponse()
        print('Ppushover message sent')
    except Exception as e:
        print('Pushover message failed: ' + str(e))

def update(elapsed_time, delta_time):

    red_led.off()

    input_state = GPIO.input(INPUT_PIN)
    if input_state == True:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        message = "Motion detected - " + dt_string
        print(message)
        logging.info(message)
        send_message()
        red_led.on()

    if every_5_secs.should(delta_time):
        print(".")

red_led.blink(0.2,0.2,3)

realtime.loop(update, loop_interval_in_secs)
