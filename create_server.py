#!/usr/bin/env python3

import requests
import json
import os
import shutil
import subprocess
import sys

# Introduction and download/load JSON file containing server versions
print("Minecraft Server Creator v2.1")
print("This script will download the server file from the official mojang.com website and set it up.")
print("You can also specify the version or view the available versions by specifying it as a command line argument.")
response = json.loads(requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").text)

# Read option from command line or from stdin
if len(sys.argv) - 1 == 1:
    version = sys.argv[1].lower()
else:
    version = input("Please enter a Minecraft version, \n" +
                    "\"view\" to see all versions, \n" +
                    "\"release\" for the latest release version, \n" +
                    "\"snapshot\" for the latest snapshot version, or\n" +
                    "\"quit\" to quit: ").lower()
if version == "quit" or version == "exit" or version == "q":
    sys.exit(0)

# Sort the JSON data into two maps: release versions and snapshot versions
# Each map will have a key of the version and value of the url to download the server
release = dict()
snapshot = dict()
for entry in response["versions"]:
    if entry["type"] == "release":
        release[entry["id"]] = entry["url"]
    elif entry["type"] == "snapshot":
        snapshot[entry["id"]] = entry["url"]

# Loop only if the input is invalid
try:
    while True:
        if version == "release" or version == "latest":
            version = response["latest"]["release"]
            version_url = release[version]
            break
        if version == "snapshot":
            version = response["latest"]["snapshot"]
            version_url = snapshot[version]
            break
        if version == "view":
            print("Snapshot:")
            keys = list(snapshot.keys())
            keys.reverse()
            for a, b, c in zip(keys[::3], keys[1::3], keys[2::3]):
                print('{:<25}{:<25}{:<}'.format(a, b, c))
            if len(keys) % 3 == 1:
                print(keys[-1])
            elif len(keys) % 3 == 2:
                print('{:<20}{:<}'.format(keys[-1], keys[-2]))
            print("\n")
            print("Release:")
            keys = list(release.keys())
            keys.reverse()
            for a, b, c in zip(keys[::3], keys[1::3], keys[2::3]):
                print('{:<20}{:<20}{:<}'.format(a, b, c))
            if len(keys) % 3 == 1:
                print(keys[-1])
            elif len(keys) % 3 == 2:
                print('{:<20}{:<}'.format(keys[-1], keys[-2]))
            print("\n")
        elif version in release.keys():
            version_url = release[version]
            break
        elif version in snapshot.keys():
            version_url = snapshot[version]
            break
        version = input("Please enter a Minecraft version, \n" +
                        "\"view\" to see all versions, \n" +
                        "\"release\" for the latest release version, \n" +
                        "\"snapshot\" for the latest snapshot version, or\n" +
                        "\"quit\" to quit: ").lower()
        if version == "quit" or version == "exit" or version == "q":
            sys.exit(0)
except:
    print()
    sys.exit(0)

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
    try:
        subprocess.Popen("run.bat", cwd=server_directory, stdout=sys.stdout, shell=True).communicate()
    except:
        print("\nThe server was exited unexpectedly.")
else:
    run = open(server_directory + "/run.sh", "w")
    run.write("java -Xmx1G -Xms1G -jar server.jar nogui")
    run.close()
    os.chmod(server_directory + "/run.sh", os.stat(server_directory + "/run.sh").st_mode | 0o111)
    try:
        subprocess.Popen("./run.sh", cwd=server_directory, stdout=sys.stdout, shell=True).communicate()
    except:
        print("\nThe server was exited unexpectedly.")
