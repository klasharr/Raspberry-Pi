# Raspberry Pi Motion Detector

This script will detect motion, log movement and optionally push a notification to your phone in a rate limited way. 

I'm using https://pypi.org/project/rstoys/ 

```
rstoys.realtime
```

to manage the programme loop and https://pushover.net/ as the notification gateway


## Config


Rate Limit the push notifications.

```
CALLS_PER_PERIOD_LIMIT = 1
RATE_LIMIT_PERIOD_SECS = 20
```

See the pushover.net APIs.

```
ENABLE_PUSHOVER_NOTIFICATIONS = False
PUSHOVER_TOKEN = 'XXXXX'
PUSHOVER_USER = 'XXXXX'
PUSHOVER_SOUND = 'siren'
PUSHOVER_MESSAGE = 'Movement detected'
```

GPIO pin set up, the electroncis are very simple.

```
PIR_PIN = 18
LED_PIN = 21
```

Control the programme loop. The interval of 1.5 secs helps with over reporting of the PIR sensor which can log movement my times / second.

```
LOOP_INTERVAL_IN_SECS = 1.5
```

A status . appears in the outout every 5 secs. 

```
EVERY_X_SECS = realtime.Interval(5.0)
```


## Usage

```
python motion.py
```

## Electronics and power

I'll add more details here especially on the PIR sensor set up. 'm powering it from a standard phone power bank. A bit overkill but this is all I have right now.

![motion detector](https://github.com/klasharr/Raspberry-Pi/blob/master/motion_detection/IMG_20200302_065934654.png)
