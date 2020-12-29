#!/usr/bin/env python3

import requests
import json
import os
import shutil
import subprocess
import sys
import math

print("Minecraft Server Creator v2.0")
print("This script will scrape the launchermeta.mojang.com website and download a server")
print("It will then setup the server\n")

# Create, Manage, Update
response = json.loads(requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").text)
release = dict()
snapshot = dict()
for entry in response["versions"]:
	if entry["type"] == "release":
		release[entry["id"]] = entry["url"]
	elif entry["type"] == "snapshot":
		snapshot[entry["id"]] = entry["url"]

version = input("Please enter a Minecraft version, \n" + 
				"\"view\" to see all versions, \n" + 
				"\"release\" for the latest release version, or\n" + 
				"\"snapshot\" for the latest snapshot version: ")

while True:
	if version == "release":
		version = response["latest"]["release"]
		version_url = release[version]
		break
	if version == "snapshot":
		version = response["latest"]["snapshot"]
		version_url = snapshot[version]
		break
	if version == "view":
		print("Release:")
		count = 0
		for entry in release.keys():
			if count < 4:
				print(entry + "\t", end="")
				count += 1
			else:
				print(entry)
				count = 0
		print("\n")
		print("Snapshot:")
		count = 0
		for entry in snapshot.keys():
			if count < 4:
				print(entry + "\t\t", end="")
				count += 1
			else:
				print(entry)
				count = 0
		print("\n")			
	elif version in release.keys():
		version_url = release[version]
		break
	elif version in snapshot.keys():
		version_url = snapshot[version]
		break
	version = input("Please enter a valid version number, \"release\" for the latest release version, or \"snapshot\" for the latest snapshot version: ")	

print("Creating server with version: " + version)

response = json.loads(requests.get(version_url).text)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
server_directory = application_path + "/" + version

if os.path.exists(server_directory):
	shutil.rmtree(server_directory)

os.makedirs(server_directory)
with open(server_directory + "/server.jar", "wb") as jar:
    jar.write(requests.get(response["downloads"]["server"]["url"]).content)

eula = open(server_directory + "/eula.txt", "w")
eula.write("eula=true")
eula.close()

if os.name == "nt":
	run = open(server_directory + "/run.bat", "w")
	run.write("java -Xmx1G -Xms1G -jar server.jar nogui")
	run.close()
	subprocess.Popen("cd \"" + server_directory + "\"; run.bat", stdout=sys.stdout, shell=True).communicate()
else:
	run = open(server_directory + "/run.sh", "w")
	run.write("java -Xmx1G -Xms1G -jar server.jar nogui")
	run.close()
	os.chmod(server_directory + "/run.sh", os.stat(server_directory + "/run.sh").st_mode | 0o111)
	subprocess.Popen("cd \"" + server_directory + "\"; ./run.sh", stdout=sys.stdout, shell=True).communicate()
