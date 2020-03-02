import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging
from rstoys import realtime
from gpiozero import LED
import httplib, urllib
from ratelimit import limits

# =====================================================

MOTION_LOGFILE = 'motion.log'

CALLS_PER_PERIOD_LIMIT = 1
RATE_LIMIT_PERIOD_SECS = 20

ENABLE_PUSHOVER_NOTIFICATIONS = False
PUSHOVER_TOKEN = 'XXXXX'
PUSHOVER_USER = 'XXXXX'
PUSHOVER_SOUND = 'siren'
PUSHOVER_MESSAGE = 'Movement detected'

PIR_PIN = 18
LED_PIN = 21

EVERY_X_SECS = realtime.Interval(5.0)
LOOP_INTERVAL_IN_SECS = 1.5

# =====================================================

logging.basicConfig(level=logging.INFO, filename=MOTION_LOGFILE)

red_led = LED(LED_PIN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)


@limits(calls=CALLS_PER_PERIOD_LIMIT, period=RATE_LIMIT_PERIOD_SECS)
def send_pushover_message():
    
    if not ENABLE_PUSHOVER_NOTIFICATIONS: 
        print('Pushover message would have been sent')
        return

    try:
        conn = httplib.HTTPSConnection("api.pushover.net:443", timeout=3)
        conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "sound": PUSHOVER_SOUND,
            "message": PUSHOVER_MESSAGE,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        response = conn.getresponse()
        
        print('Pushover message sent')
    except Exception as e:
        print('Pushover message failed: ' + str(e))

def update(elapsed_time, delta_time):

    red_led.off()
    input_state = GPIO.input(PIR_PIN)
    
    if input_state == True:
        now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	message = "Motion detected - " + dt_string
        print(message)
        logging.info(message)
        try: 
            send_pushover_message()
        except Exception as e:
            print(str(e))
        
        red_led.on()

    if EVERY_X_SECS.should(delta_time):
        print(".")
        
# Visual signal our script started        
red_led.blink(0.2,0.2,3)

realtime.loop(update, LOOP_INTERVAL_IN_SECS)
