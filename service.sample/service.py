#
# This is a sample service plugin for Hyperion, it can be used as a start point for development.
#
# API documentation: https://docs.hyperion-project.org/en/developer/plugins#plugin_development
# Tutorial : https://docs.hyperion-project.org/en/developer/plugins_dev#our_first_plugin
#

# we work with Enum values so import the module
from enum import Enum
# import the plugin modul from Hyperion to get access to the API
from plugin import *
# import time to use time.sleep(1) for the abort loop
import time


# the user settings are declared here as variable, currently None (empty)
settings = None

def getUserSettings():
	""" Get user settings
		Get the user settings. You may want to perform further actions here
	"""
	log("Get settings now...")
	# Write the new settings to our global settings variable declared above
	global settings
	settings = getSettings()
	# print the content to log according to our settingsSchema.json. The fallback values should be the same from the settingsSchema default fields
	log("myMealOption has value: "+settings.get('myMealOption', "Pizza Fallback"))
	log("mySelectionOption has value: "+settings.get('mySelectionOption', "option2"))
	log("myIntegerOption has value: "+str(settings.get('myIntegerOption', 999)))
	log("myNumberOption has value: "+str(settings.get('myNumberOption', 45.5)))
	log("myBooleanOption has value: "+str(settings.get('myBooleanOption', True)))
	log("myFavouriteColorOption has value: "+str(settings.get('myFavouriteColorOption', (255,255,0))))

def onCompStateChanged(comp, state):
	""" Component State Changed
		This function is called whenever a component state has been changed
	"""
	log("The component "+comp+" changed state to: "+str(state))

def onSettingsChanged():
	""" Settings changed
		This function is called whenever the user saved new settings for this plugin
	"""
	log("Settings of this plugin has been changed, grab them!")
	# Get them by calling getUserSettings() (declared above) again!
	getUserSettings()

def onVsibilePriorityChanged(newPrio):
	""" Visible priority changed
		This function is called whenever the visible priority changed 
	"""
	log("New visible priority is: "+str(newPrio))


# Let's print a message to the Hyperion log with different log types
log("Awesome, we start! No LOG_LVL type given means type DEBUG")
log("This message is of type INFO", LOG_INFO)
log("This message is of type WARNING", LOG_WARNING)
log("This message is of type ERROR", LOG_ERROR)
log("This message is of type DEBUG", LOG_DEBUG)


# Get the user settings as they are empty
getUserSettings()


# Register callbacks from Hyperion to get notifications during runtime about specific events
registerCallback(ON_COMP_STATE_CHANGED, onCompStateChanged)
registerCallback(ON_SETTINGS_CHANGED, onSettingsChanged)
registerCallback(ON_VISIBLE_PRIORITY_CHANGED, onVsibilePriorityChanged)

# Let's play around with the API, remove the hashtag "#" to see them in action. You need to restart this plugin to load the changed code
#setColor(255,0,0)
#setColor(0,255,0, 15000, 75)

#setEffect("Candle", -1, 100)
#setEffect("Warm mood blobs", 25000, 125)

#setComponentState(COMP_SMOOTHING, False)

# Keep the plugin running, if Hyperion requests an abort it will end. Limit the abort api call to one each second with time.sleep(1)
while not abort():
	time.sleep(1)

# No code after "while not abort()" loop, when we reach this comment the script should end!
log("So let's stop...")
