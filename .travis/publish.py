#!/usr/bin/python3
import os, shutil, httplib2, simplejson as json

# define GH_REP repository; GH_USR the github user; GH_REL_TAG The release tag to use; GH_TOK the access token
GH_REP = "plugins"
GH_USR = "brindosch"
GH_REL_TAG = "1.0.0"
GH_TOK = os.environ["GH_TOK"]
# root directory of plugin source folders
MDIR = os.environ["TRAVIS_BUILD_DIR"]
# directory where the zips should be saved
ZIPDIR = os.environ["TRAVIS_BUILD_DIR"]+"/packages"

GH_API = "https://api.github.com"
GH_REPO = GH_API+"/repos/"+GH_USR+"/"+GH_REP
GH_TAGS = GH_REPO+"/releases/tags/"+GH_REL_TAG
GH_ASSETS = GH_REPO+"/releases/assets/"
GH_UPLOAD = "https://uploads.github.com/repos/"+GH_USR+"/"+GH_REP+"/releases/"
AUTHHEAD = {'Authorization': 'token '+GH_TOK}
HEADERS = {'Content-type': 'application/zip'}

TC = os.environ["TRAVIS_COMMIT_MESSAGE"]

# not all commit messages needs to be a upload request, filter them
if "[" not in TC or "]" not in TC:
	print("Aborting script, nothing to do as there where no [] in commit message. Message: "+TC)
	exit()

# add auth header
HEADERS.update(AUTHHEAD)

ZIPPEDFILES = []
GITHUB_FILES = []
REPOINDEX = []
httplib2.debuglevel = 1
http = httplib2.Http()

# get all module. and service. subdirs in MDIR
def getSubDirs():
	dlist = next(os.walk(MDIR))[1]
	cdlist = []
	for entry in dlist:
		if entry.startswith("service.") or entry.startswith("module."):
			cdlist.append(entry)
	return cdlist

# load plugin.json of path
def loadMeta(path):
	global REPOINDEX
	try:
		with open(path+"/plugin.json", encoding='utf-8') as meta_file:
			REPOINDEX.append(json.loads(meta_file.read()))
	except Exception as e:
		print("Failed to open/parse plugin.json of: "+path)
		print(e)
		exit(True)

# zip a directory and push info dict to ZIPPEDFILES
def zipDir(dir):
	global ZIPPEDFILES
	shutil.make_archive(ZIPDIR+"/"+dir, 'zip', MDIR+"/"+dir)
	ZIPPEDFILES.append({"path":ZIPDIR+"/"+dir+".zip","name":dir+".zip"})
	#print("Zipped dir: "+dir+" to "+ZIPDIR+"/"+dir+".zip")

# check if zip file exists on github
def existZip(name):
	for entry in GITHUB_FILES:
		if entry["name"] == name:
			return True, entry["id"]
	return False, ''

# delete a file by id from github
def delete(id):
	response, content = http.request(GH_ASSETS+str(id), 'DELETE', headers=AUTHHEAD)

# upload a file to github
def upload(filePath, fileName):
	GH_ASSET = GH_UPLOAD+TAG_ID+"/assets?name="+fileName
	response, content = http.request(GH_ASSET, 'POST', headers=HEADERS, body=open(filePath, "rb"))
	print(response,content)
	parsed = json.loads(content)
	parsedResp = json.loads(response)
	if 'errors' in parsed:
			errors = parsed["errors"][0]
			if 'code' in errors:
				print("There where errors during upload Code: "+errors["code"]+" FileName: "+fileName)
				exit(True)
	elif parsedResp["status"] != 200:
		print("Failed to upload: "+fileName,"Server Response: "+response)
		exit(True)
    else:
		print("Upload was successfull: "+fileName)

# extract plugin id from commit
pluginid = (TC.split("["))[1].split("]")[0]
print("Starting processing of plugin id: "+pluginid)

# verify commit id is found as folder name
# zip on success (push to ZIPPEDFILES)
if pluginid not in getSubDirs():
	print("The commit plugin id does not exist as folder! -> "+pluginid)
	exit(True)
else:
	zipDir(pluginid)

# get list of github assets and tag id of the specified github tag
response, content = http.request(GH_TAGS, 'GET', headers=AUTHHEAD)
parsed = json.loads(content)
# tag id
TAG_ID = json.dumps(parsed["id"])

# build list of github assets; push to GITHUB_FILES
for entry in parsed["assets"]:
	GITHUB_FILES.append({"name":entry["name"],"id":entry["id"]})

# generate new repository index
for dir in getSubDirs():
	loadMeta(MDIR+"/"+dir)

# save to disk
with open(MDIR+"/repository.json","w+") as f:
	f.write(json.dumps(REPOINDEX))
	f.close()

# append it to ZIPPEDFILES, to upload it just if prev uploads where successfull
ZIPPEDFILES.append({"path":MDIR+"/repository.json","name":"repository.json"})

# upload all entrys in ZIPPEDFILES
for zfile in ZIPPEDFILES:
	exists, id = existZip(zfile["name"])
	if exists:
		# delete asset
		delete(id)
	# upload asset
	upload(zfile["path"],zfile["name"])

# gracefully ended
print("Script ended successfully")
