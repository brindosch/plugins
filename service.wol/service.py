from enum import Enum
from plugin import *
import wakeonlan
import time

# the settings
sendCont = False
macAddresses = ()

def sendPacket(count = 1):
	"""
		Send a magic packet to all listed mac addresses, if count is higher than 1 it will be repeated (1s delay in between)
	"""
	for i in range(count):
		for mac in macAddresses:
			wakeonlan.send_magic_packet(mac)
		
		time.sleep(1)

def getUserSettings():
	""" Get user settings
		Get the user settings and resend magic packets
	"""
	global macAddresses, sendCont
	settings = getSettings()
	macAddresses = settings.get('macAddresses', ())
	sendCont = settings.get('sendContinuous', False)
	sendPacket(3)

def onSettingsChanged():
	""" Settings changed
		Update them!
	"""
	getUserSettings()


# Get the user settings and send first shot
getUserSettings()

# Register callbacks from Hyperion to get notifications during runtime about specific events
registerCallback(ON_SETTINGS_CHANGED, onSettingsChanged)

# use loop to send continuous
while not abort():
	time.sleep(1)
	if sendCont:
		sendPacket()
		
