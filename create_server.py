from bs4 import BeautifulSoup
import requests
import os
import shutil
import subprocess
import sys
import math

print("Minecraft Server Creator v1.2")
print("This script will scrape the mcversion.net website and download a server")
print("It will then setup the server\n")

# Create, Manage, Update	

mcversions = BeautifulSoup(requests.get("https://mcversions.net/").text, "html.parser")
server_links = dict()
version_categories = ["Stable Releases", "Snapshot Previews"]
for i in range(len(version_categories)):
	category = mcversions.find_all(class_="list-group")[i]
	server_links[version_categories[i]] = dict(zip([version["id"] for version in category.find_all("li")], [link["href"] for link in category.find_all("a", text="Server Jar")]))

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
		print("Release: ")
		release = list(server_links[version_categories[0]].keys())
		rows = math.ceil(len(release) / columns)
		for i in range(rows):
			print("\t", end="")
			for j in range(columns):
				if len(release) > i + j * rows:
					print(release[i + j * rows], end="")
					spacing = math.ceil(max((24 - len(release[i + j * rows])) / 8, 1)) * "\t"
					print(spacing, end="")
			print()	
		print("Snapshot: ")
		snapshot = list(server_links[version_categories[1]].keys())
		rows = math.ceil(len(snapshot) / columns)
		for i in range(rows):
			print("\t", end="")
			for j in range(columns):
				if len(snapshot) > i + j * rows:
					print(snapshot[i + j * rows], end="")
					spacing = math.ceil(max((24 - len(snapshot[i + j * rows])) / 8, 1)) * "\t"
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

if os.path.exists(version):
	shutil.rmtree(version)

os.makedirs(version)
with open(version + "/server.jar", "wb") as jar:
    jar.write(requests.get(server_links[category][version]).content)

eula = open(version + "/eula.txt", "w")
eula.write("eula=true")
eula.close()

if os.name == "nt":
	run = open(version + "/run.bat", "w")
	run.write("java -Xmx1G -Xms1G -jar server.jar nogui")
	run.close()
	subprocess.Popen("cd " + version + "; run.bat", stdout=sys.stdout, shell=True).communicate()
else:
	run = open(version + "/run.sh", "w")
	run.write("java -Xmx1G -Xms1G -jar server.jar nogui")
	run.close()
	os.chmod(version + "/run.sh", os.stat(version + "/run.sh").st_mode | 0o111)
	subprocess.Popen("cd " + version + "; ./run.sh", stdout=sys.stdout, shell=True).communicate()