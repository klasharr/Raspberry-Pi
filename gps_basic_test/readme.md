## Getting GPS basics working

Scope: GPS works and is logging. 

### Hardware

- Raspberry PI 3B
- Adafruit GPS HAT https://www.adafruit.com/product/2324

### Docs

- https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi/ 
- https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-python-uart-usage 
- https://wiki.dragino.com/index.php?title=Getting_GPS_to_work_on_Raspberry_Pi_3_Model_B
- https://gpsd.gitlab.io/gpsd/client-howto.html
- https://wiki.openstreetmap.org/wiki/GPX 

### Libs

- https://pypi.org/project/rstoys/ - used for the control loop currently. I'll use mapping and route features in later projects
- https://pypi.org/project/gpxpy/#description - this looks useful for reading / writing GPX files
