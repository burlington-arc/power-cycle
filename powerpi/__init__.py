
import argparse
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
    # Create and configure the argument parser
    argp=argparse.ArgumentParser(description="Power-cycle equipment")
    argp.add_argument("device", nargs=1, choices=pins.keys(),
        help="name of device to power-cycle")
    argp.add_argument("duration", type=int,nargs="?", default=10,
        help="power-cycle duration in seconds");
    argp.add_argument("--dry-run", dest="dryRun", action="store_true",
        help="Dry-run: don't actually power-cycle, but record in the logs")
    argp.add_argument("--comment", help="Comment to be recorded in the log",
        dest="comment", default= None)

    # Run the argument parser
    args=argp.parse_args()

    # If args is not satisfied, print the usage.

    # Run the script.
    requestedPin=args.device[0]
    duration=args.duration
    dryRun=args.dryRun

    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    try:
        fh=logging.FileHandler("/var/log/power-cycle.log")
    except:
        if dryRun:
            fh=logging.FileHandler("./power-cycle.log")
        else:
            print "Unable to write to log file '/var/log/power-cycle.log'."
            print "  ...usually this is fixed if you run with 'sudo'."
            sys.exit(-1)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    print "Cycling {0} for {1} seconds.".format(requestedPin, duration)
    if GPIO==None:
        print "No GPIO library - this will be a dry run."
        dryRun=True

    if args.comment:
        logger.info("{0} is being power-cycled:  Comment is {1}".format(
            requestedPin, args.comment
        ))

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
