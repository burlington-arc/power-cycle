
import RPi.GPIO as GPIO
import time
import sys
import os
from daemon import daemon

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

    print("Cycling {0} for {1} seconds.".format(requestedPin, duration))
    daemon_context=daemon.DaemonContext()

    daemon_context.open()

    pin=pins[requestedPin];

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
