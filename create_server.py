from bs4 import BeautifulSoup
import requests
import os
import shutil
import subprocess
import sys

print("Minecraft Server Creator v1.0")
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
		print("Release: ")
		for current_version in server_links[version_categories[0]].keys():
			print("\t%s" % current_version)
		print("Snapshot: ")
		for current_version in server_links[version_categories[1]].keys():
			print("\t%s" % current_version)
		continue		
	if version in server_links.get(version_categories[0]).keys():
		category = version_categories[0]
		break
	if version in server_links.get(version_categories[1]).keys():
		category = version_categories[1]
		break
	# TODO change this input text	
	version = input("Invalid input: ")

# Directory Name,
	# Directory already exists, override or update?
# Sign EULA, maybe

if os.path.exists(version):
	shutil.rmtree(version)
	# print("Directory " + version + " already exists. ")
	# while True:
	# 	print("Enter \"reinstall\" to delete and recreate the server. All files will be deleted")
	# 	print("Enter \"create\" to create another server of the same version")	
	# 	recreate = input()

os.makedirs(version)
with open(version + "/server.jar", "wb") as jar:
    jar.write(requests.get(server_links[category][version]).content)

eula = open(version + "/eula.txt", "w")
eula.write("eula=true")
eula.close()

subprocess.Popen("cd " + version + "; java -Xmx1G -Xms1G -jar server.jar", stdout=sys.stdout, shell=True).communicate()