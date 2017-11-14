#!/usr/bin/python3
import os, shutil, httplib2, simplejson as json
print("PUBLSH PY CALLED")
# print some stuff
MDIR = os.environ["TRAVIS_BUILD_DIR"]
TC = os.environ["TRAVIS_COMMIT"]
TCM = os.environ["TRAVIS_COMMIT_MESSAGE"]

print("TBD",MDIR)
print("TC",TC)
print("TCM",TCM)
print("now exits with")
exit()
