import RPi.GPIO as GPIO
import time
from datetime import datetime
import logging
from rstoys import realtime
from gpiozero import LED
from ratelimit import limits

# ===================== GPX ============================

import gpxpy
import gpxpy.gpx

# ===================== GPS ============================

import board
import busio
import adafruit_gps
import serial

# Create a serial connection for the GPS connection
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False) 

# Turn on the basic GGA and RMC info
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Update rate
gps.send_command(b"PMTK220,1000")

# ======================== Constants =====================

MOTION_LOGFILE = 'gps.log'
LED_PIN = 21
LOOP_INTERVAL_IN_SECS = 2

# ========================================================

logging.basicConfig(level=logging.INFO, filename=MOTION_LOGFILE)

red_led = LED(LED_PIN)

# ========================================================

def update(elapsed_time, delta_time):
    
    global gps
    global logging

    gps.update()    
    if not gps.has_fix:
        print("Waiting for fix...")
        return

    print("=" * 40) 
    print(
        "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
            gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,  # month!
            gps.timestamp_utc.tm_sec,
        )
    )
    logging.info("Latitude: {0:.6f} degrees".format(gps.latitude))
    logging.info("Longitude: {0:.6f} degrees".format(gps.longitude))
    logging.info("Fix quality: {}".format(gps.fix_quality))
    
    # Some attributes beyond latitude, longitude and timestamp are optional
    # and might not be present.  Check if they're None before trying to use!
    #if gps.satellites is not None:
    #    print("# satellites: {}".format(gps.satellites))
    #if gps.altitude_m is not None:
    #    print("Altitude: {} meters".format(gps.altitude_m))
    if gps.speed_knots is not None:
        logging.info("Speed: {} knots".format(gps.speed_knots))
    if gps.track_angle_deg is not None:
        logging.info("Track angle: {} degrees".format(gps.track_angle_deg))
    #if gps.horizontal_dilution is not None:
    #    print("Horizontal dilution: {}".format(gps.horizontal_dilution))
    #if gps.height_geoid is not None:
    #    print("Height geo ID: {} meters".format(gps.height_geoid))

        
# Visual signal our script started        
red_led.blink(0.2,0.2,3)

# Start loop
realtime.loop(update, LOOP_INTERVAL_IN_SECS)
