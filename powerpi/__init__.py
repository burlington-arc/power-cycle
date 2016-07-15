
import time
import sys
import os
from daemon import daemon
import logging

try:
    import RPi.GPIO as GPIO
except:
    GPIO=None

pins= { 'repeater': 18, 'router': 17 }

def main():
    """Entry point for the application script"""
    requestedPin=sys.argv[1];
    if not requestedPin in pins:
        print("The following powered items are supported")
        for pin in pins:
            print("  " + pin)
        sys.exit(os.EX_USAGE)
    if len(sys.argv)==3:
        duration=int(sys.argv[2])
    else:
        duration=10

    print "Cycling {0} for {1} seconds.".format(requestedPin, duration)
    if GPIO==None:
        print "No GPIO library - this will be a dry run."
        dryRun=True
    else:
        dryRun=False

    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    try:
        fh=logging.FileHandler("/var/log/power-cycle.log")
    except:
        fh=logging.FileHandler("./power-cycle.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    daemon_context=daemon.DaemonContext(
        files_preserve= [ fh.stream ]
    )

    daemon_context.open()

    pin=pins[requestedPin];

    if dryRun:
        logger.info("(Dry-run) Power off {0} for {1} seconds".format(requestedPin, duration))
    else:
        logger.info("Power off {0} for {1}".format(requestedPin, duration))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    if dryRun:
        logger.info("(Dry-run) Power on {0}".format(requestedPin))
    else:
        logger.info("Power on {0}".format(requestedPin))
        GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
