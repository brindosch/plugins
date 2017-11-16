#!/usr/bin/python3
#####
# Testing script for plugin pull requests to fullfill the requirements
#####
import os, subprocess, simplejson as json

# Errors/Warnings store
Errors = []
Warnings = []
# root directory of plugin source folders
MDIR = os.environ["TRAVIS_BUILD_DIR"]

# helper methods
def getSubDirs():
	dlist = next(os.walk(MDIR))[1]
	cdlist = []
	for entry in dlist:
		if entry.startswith("service.") or entry.startswith("module."):
			cdlist.append(entry)
	return cdlist

def addError(test,msg):
	global Errors
	Errors.append("TEST: "+test+": "+msg)

def addWarning(test,msg):
	global Warnings
	Warnings.append("TEST: "+test+": "+msg)

def printErrors():
	print("###### TEST FAILED PLEASE FIX ALL ERRORS ######")
	for err in Errors:
		print(err)
	print("###### TEST END ######")
	exit(True)

output = subprocess.check_output(["git", "show", "-s --format=%B"])
print("OUTPUT:"+output)
# Test commit message for []
TC = os.environ["TRAVIS_COMMIT_MESSAGE"]
if "[" not in TC or "]" not in TC:
	addError("COMMIT-HEADER","The commit should contain the plugin id in [] example: [service.kodi] The current commit message is: "+TC)
	# fast abort, we need the id
	printErrors()

# Test if plugin id exists as folder plugin id from commit
prPluginId = (TC.split("["))[1].split("]")[0]
if prPluginId not in getSubDirs():
	addError("PLUGIN-ID","Plugin id of the pull request header("+prPluginId+") is not available as folder name. Keep in mind that the id should start with 'service.' or 'module.'")
	# fast abort, as we need the plugin id to know where to search for meta file
	printErrors()


print("Testing plugin id: "+prPluginId)

# Let's parse the meta data
try:
	with open(MDIR+"/"+prPluginId+"/plugin.json", encoding='utf-8') as data_file:
		parsedMeta = json.loads(data_file.read())
except Exception as e:
	addError("plugin.json","Failed to open or parse the plugin.json file. Please make sure the file exist and is valid json. You can test for valid json with www.jsonlint.com")
	print(e)
	# fast abort
	printErrors()

# Compare plugin id of meta file with id of folder
if parsedMeta["id"] not in getSubDirs():
	addError("plugin.json-id","The id of your plugin.json does not exist as folder name. Please use the same name for id and folder")

# check if id is lowercase
if not parsedMeta["id"].islower():
	addError("plugin.json-id","The id of your plugin.json should be lowercase")

# check if ":" is in id
if any(i in parsedMeta["id"] for i in '":_#*='):
	addError("plugin.json-id","The id of your plugin.json shouldn't contain ':' '_' '#' '*' '=' '\"' character")

if "name" not in parsedMeta:
	addError("plugin.json-name","Please add a name property to your plugin.json. The name is a user friendly display name")

if "description" not in parsedMeta:
	addError("plugin.json-description","Please add a description property to your plugin.json with a brief description what your plugin does")

if "version" not in parsedMeta:
	addError("plugin.json-version","Please add a version property to your plugin.json in format of MAJOR.MINOR.PATCH '1.0.0'")

if parsedMeta["id"].startswith("service.") and "dependencies" not in parsedMeta:
	addWarning("plugin.json-dependencies","It's recommended to add a dependencies property to your plugin.json, at least to define a minimum version of Hyperion.")

if "changelog" not in parsedMeta:
	addError("plugin.json-changelog",'Please add a changelog property to your plugin.json in format of [{"HeaderFirstEntry":"-Info1 -Info2"},{"HeaderSecondEntry":"-Info1 -Info2"}]')

if "provider" not in parsedMeta:
	addError("plugin.json-provider",'Please add a provider property to your plugin.jso. This is usually the Auhtor name/nick')

if "support" not in parsedMeta:
	addError("plugin.json-support",'Please add a support property to your plugin.json. This should be a url that points to a support thread at our forum in format of "https://MyUrl"')
elif not parsedMeta["support"].startswith("https://"):
	addError("plugin.json-support",'The support field should contain a URL in format of "https://MyUrl"')

if "source" not in parsedMeta:
	addError("plugin.json-source",'Please add a source property to your plugin.json. This should be a url that points to the source code of this plugin')
elif not parsedMeta["source"].startswith("https://"):
	addError("plugin.json-source",'The source field should contain a URL in format of "https://MyUrl"')

# LICENCE should be defined
if "licence" not in parsedMeta:
	addError("plugin.json-licence",'Please add a licence property to your plugin.json. Can be MIT or LGPL for example')

# settingsSchema.json scheck
if parsedMeta["id"].startswith("service."):
	if os.path.isfile(MDIR+"/"+parsedMeta["id"]+"/settingsSchema.json"):
		try:
			with open(MDIR+"/"+parsedMeta["id"]+"/settingsSchema.json", encoding='utf-8') as schema_file:
				json.loads(schema_file.read())
		except Exception as e:
			addError("settingsSchema.json","Can't open or parse settingsSchema.json. You can check json validation with www.jsonlint.com")
			print(e)
	else:
		addError("settingsSchema.json",'A service. plugin requires a settingsSchema.json file to provide options to configure.')

# now print all errors or exit gracefully
if Errors:
	printErrors()

print("###### TEST SUCCESSFULLY PASSED ######")
if Warnings:
	print("\n###### WARNINGS ######")
	for warn in Warnings:
		print(warn)
