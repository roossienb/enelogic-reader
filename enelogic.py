#######################################################################################
# Filename:     enelogic.py
# Author:       Bart Roossien (Github: roossienb)
# Version:      1.0.0
# Date:         2025-05-01
# Copyright:    (c) 2025 Bart Roossien
# Description:  Fetches all data from Enelogic API and saves it to CSV files.
# Attribution:  Based on the original work by @Kleptog:
#               https://gist.github.com/kleptog/572b529b84a1f0c40c3c69edaa18d670
#                    
# License:      This program is free software: you can redistribute it and/or modify it 
#               under the terms of the GNU General Public License as published by the 
#               Free Software Foundation, either version 3 of the License, or (at your option) 
#               any later version.
# 
#               This program is distributed in the hope that it will be useful, but WITHOUT 
#               ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
#               FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
#               details.
#
#               You should have received a copy of the GNU General Public License along with 
#               this program. If not, see <https://www.gnu.org/licenses/>.
#
#########################################################################################

# Go to the developer center: enelogic.com/nl/developers.
# Add your app and choose a desired redirect url (only for OAuth2 purposes, if using WSSE just fill in a URL e.g. enelogic.com)
# Fill in values below

import hashlib
import json
import os
from unittest.main import MAIN_EXAMPLES
import requests
import base64
import datetime
import uuid
import csv

# Generates an X-WSSE authentication header for the given username and password.
#
# Args:
#     username (str): The username for authentication.
#     password (str): The password used to generate the WSSE header.
#
# Returns:
#     dict: A dictionary containing the WSSE authentication header.
#
# Example:
#     header = create_wsse_header("myUser", "myPass")
#     s = requests.Session()
#     s.headers.update(header)
#
def create_wsse_header(username, password):
    # Create a random nonce.
    nonce = uuid.uuid4().hex

    # Get current UTC time
    utc_now = datetime.datetime.now(datetime.timezone.utc)

    # Subtract 30 seconds because Enelogic server is behind in time
    # This triggers the Forbidden error as the time is in the future.
    utc_minus_30s = utc_now - datetime.timedelta(seconds=30)
    created = utc_minus_30s.strftime("%Y-%m-%dT%H:%M:00Z")

    # Create the password digest
    digest = base64.b64encode(hashlib.sha1((nonce + created + password).encode()).digest()).decode()

    # Encode the nonce in base64
    base64nonce = base64.b64encode(nonce.encode("utf-8")).decode("utf-8")

    # Create the WSSE header
    return {
        "X-WSSE": f'UsernameToken Username="{username}", PasswordDigest="{digest}", Nonce="{base64nonce}", Created="{created}"'
    }

# Fetches data from the Enelogic API and saves it to CSV files.
#
# Args:
#     username (str): The username for authentication.
#     appid (str): The application ID for authentication.
#     appsecret (str): The application secret for authentication.
#     apikey (str): The API key for authentication.
#
# Returns:
#     None
#
# Example:
#   fetch("user@example.com", "appid", "appsecret", "apikey"))
#
def fetch(username, appid, appsecret, apikey):
    # Create username and password
    u = appid + "." + username
    p = appsecret + "." + apikey

    # Create a session
    s = requests.Session()
    s.headers.update({'Content-Type': 'application/json'})    

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Get Measuring Points
    s.headers.update(create_wsse_header(u,p))    
    res = s.get("https://enelogic.com/api/measuringpoints/")
    measurepoints = {r['id']: r for r in res.json()}

    # Grab data for each measuring point
    for measurepoint in measurepoints:

        # Find the start and end date for the measuring point
        currentDate = datetime.datetime.strptime(measurepoints[measurepoint]['dayMin'][:10], "%Y-%m-%d")
        endDate = datetime.datetime.strptime(measurepoints[measurepoint]['dayMax'][:10], "%Y-%m-%d")
    
        # Need to grab the data day by day
        while currentDate < endDate:
            # Calculate the next date
            nextDate = currentDate + datetime.timedelta(days=1)

            # Create the filename
            fname = os.path.join("output/" + str(measurepoint) + "." + currentDate.strftime("%Y-%m-%d") + '.csv')

            # Skip if file already exists, to prevent unnecessary requests
            if os.path.exists(fname):
                currentDate = nextDate
                continue

            # Print the filename to the console
            # This is useful for debugging and tracking progress        
            print (fname)

            # Make the request
            s.headers.update(create_wsse_header(u,p))    
            res = s.get("https://enelogic.com/api/measuringpoints/%s/datapoints/%s/%s" % (measurepoint, currentDate.strftime("%Y-%m-%d"), nextDate.strftime("%Y-%m-%d")))
        
            # Convert data to JSON.
            jdata = json.loads(res.content.decode())

            # Check if the response contains data
            if jdata:
                # Write to CSV file
                with open(fname, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=jdata[0].keys())
                    writer.writeheader()
                    writer.writerows(jdata)
        
            # Go to the next date
            currentDate = nextDate

def bundle():
    # Get all files in the output directory
    files = os.listdir("output")

    # Create a dictionary to hold the data
    data = {}

    # Loop through all files
    for file in files:

        # Check if the file is a CSV file
        if file.endswith(".csv"):

            # Get the info from the filename
            measurementId = file.split(".")[0]
            date = file.split(".")[1]
            year = date.split("-")[0]

            # Check if the measurement-year is already in the dictionary
            consolidatedName = measurementId + "." + year

            if consolidatedName not in data:
                data[consolidatedName] = []

            # Read the CSV file and append the data to the dictionary
            with open(os.path.join("output", file), "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data[consolidatedName].append(row)

    # Write the data to CSV files
    for consolidatedName, rows in data.items():
        with open(os.path.join("output", f"{consolidatedName}.csv"), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)