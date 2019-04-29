#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

python3 /root/VkBots/sorry.py  & 2>> errors
python3 /root/VkBots/__init__.py & 2>> errors
exit 0
