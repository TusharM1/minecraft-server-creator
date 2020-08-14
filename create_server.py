#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import os
import shutil
import subprocess
import sys
import math

print("Minecraft Server Creator v1.4")
print("This script will scrape the mcversion.net website and download a server")
print("It will then setup the server\n")

# Create, Manage, Update
url = "https://mcversions.net"
mcversions = BeautifulSoup(requests.get(url).text, "html.parser")
server_links = dict()
version_categories = ["Stable Releases", "Snapshot Preview"]
version_sections = list(mcversions.find_all("div", class_='versions')[0].children)
for i in range(len(version_categories)):
	version_items = version_sections[i].find_all(class_='item')
	version_items = list(filter(lambda version_item: len(version_item['class']) == 1, version_items))
	server_links[version_categories[i]] = dict(zip([version["id"] for version in version_items], [link.find("a", text="Download")["href"] for link in version_items]))

version = input("Please enter a Minecraft version, \n" + 
				"\"view\" to see all versions, \n" + 
				"\"release\" for the latest release version, or\n" + 
				"\"snapshot\" for the latest snapshot version: ")

while True:
	if version == "release":
		version = list(server_links[version_categories[0]].keys())[0]
		category = version_categories[0]
		break
	if version == "snapshot":
		version = list(server_links[version_categories[1]].keys())[0]
		category = version_categories[1]
		break
	if version == "view":
		columns = 4
		for i in range(len(version_categories)):
			print(version_categories[i] + ": ")
			release = list(server_links[version_categories[i]].keys())
			rows = math.ceil(len(release) / columns)
			for i in range(rows):
				print("\t", end="")
				for j in range(columns):
					if len(release) > i + j * rows:
						print(release[i + j * rows], end="")
						spacing = math.ceil(max((24 - len(release[i + j * rows])) / 8, 1)) * "\t"
						print(spacing, end="")
				print()	
		version = input("Please enter a valid version number, \"release\" for the latest release version, or \"snapshot\" for the latest snapshot version: ")	
		continue		
	if version in server_links.get(version_categories[0]).keys():
		category = version_categories[0]
		break
	if version in server_links.get(version_categories[1]).keys():
		category = version_categories[1]
		break
	version = input("Please enter a valid version number, \"release\" for the latest release version, or \"snapshot\" for the latest snapshot version: ")	

print("Creating server with version: " + version)

download = BeautifulSoup(requests.get(url + server_links[category][version]).text, "html.parser")
mojang_url = download.find_all('a',class_="button")[0]['href']

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
server_directory = application_path + "/" + version

if os.path.exists(server_directory):
	shutil.rmtree(server_directory)

os.makedirs(server_directory)
with open(server_directory + "/server.jar", "wb") as jar:
    jar.write(requests.get(mojang_url).content)

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