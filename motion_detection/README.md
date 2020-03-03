# Raspberry Pi Motion Detector

This script will detect motion, log movement and optionally push a notification to your phone in a rate limited way. 

I'm using https://pypi.org/project/rstoys/ 

```
rstoys.realtime
```

to manage the programme loop and https://pushover.net/ as the notification gateway


## Config


Rate limit the push notifications.

```
CALLS_PER_PERIOD_LIMIT = 1
RATE_LIMIT_PERIOD_SECS = 20
```

Turn off Pushover notifications, handy for debugging and set up.

```
ENABLE_PUSHOVER_NOTIFICATIONS = False
```

See the https://pushover.net/api/client for details. For private use you just need to buy the Pushover [App](https://pushover.net/) once and if you rate limit, that should give you ample notifications to play with.

```
PUSHOVER_TOKEN = 'XXXXX'
PUSHOVER_USER = 'XXXXX'
PUSHOVER_SOUND = 'siren'
PUSHOVER_MESSAGE = 'Movement detected'
```

GPIO pin set up, the electronics are very simple.

```
PIR_PIN = 18
LED_PIN = 21
```

This controls programme loop cycle. The interval of 1.5 secs helps with over reporting of the PIR sensor which can log movement many times / second.

```
LOOP_INTERVAL_IN_SECS = 1.5
```

A status . appears in the outout every 5 secs. 

```
EVERY_X_SECS = realtime.Interval(5.0)
```


## Usage

I've set this script to run at boot on my Pi Zero and it gives three blinks on start up. It can send notifications to your phone, or just log in to your PI via SSH and tail -f log.

```
python motion.py
```

## Electronics and power

I'll add more details here especially on the PIR sensor set up. It's powered from a standard phone power bank, a bit overkill but this is all I have right now. Likely a small battery pack and voltage regulator would do it too.

![motion detector](https://github.com/klasharr/Raspberry-Pi/blob/master/motion_detection/IMG_20200302_065934654.png)
