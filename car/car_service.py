#!/usr/bin/env python3

from time import sleep
from server.Station import Station

conf = """
nano ~/.bashrc

set tabsize 4
set constantshow
set autoindent
# set linenumbers
# set nohelp
# set tabstospaces
# set boldtext

runnig on /etc/systemd/system/
"""
s = Station('server/joystick/index.html', 'server/joystick/logic.js', 'server/joystick/look.css')
s.start()

while True:
	sleep(1)
	print(conf)
