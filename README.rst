Repeater Power-Cycle Controller
===============================

This is a short utility to power-cycle the BARC repeater and router through
a digital output on the Digipeater's Raspberry Pi.

----

The Yaesu Fusion repeater is known to occasionally lock up and require a reboot.
In order to facilitate this remotely, we have a optoisolated relay board that
is attached to the Raspberry Pi that runs the digipeater's beacons.  There are
two relays connected in a normally-closed mode, driven by the Pi's digital
outputs.  The repeater is connected to GPIO17 and the internet router is
connected to GPIO18.  This allows us to set a cron job that resets the router
or repeater occasionally, or potentially send a command through the APRS system.
The repeater could also be reset through a remote login.  Resetting the router
through a remote login makes less sense.  If we're able to login, then by
definition, the router is working.  Nonetheless, it still could be reset.

This package contains the control script to do the actual power cycling.  It is
typically called by running an Ansible playbook remotely, although it could be
run through an interactive login if necessary.  In the usual case, the Ansible
playbook will initiate an orderly shutdown of the Raspberry Pi that controls the
Fusion repeater, prior to shutting down the repeater (the Pi is powered from the
repeater, so we'd like to avoid power-cycling the Pi without warning).
