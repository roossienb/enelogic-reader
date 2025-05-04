#######################################################################################
# Filename:     example.py
# Author:       Bart Roossien (Github: roossienb)
# Version:      1.0.0
# Date:         2025-05-01
# Copyright:    (c) 2025 Bart Roossien
# Description:  Example on how to use the enelogic module
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

# Import the enelogic module
import enelogic

# Set these values to your own
#   - Go to the developer center: https://enelogic.com/nl/developers
#   - Add your app (URL can be anything like e.g. enelogic.com)
#   - Obtain appid and appsecret
#   - Go to https://enelogic.com/nl/web#/mijn-account/applicaties
#   - Obtain apikey from this page
appid = "<appid>"
appsecret = "<appsecret>"
username = "<username"
apikey = "<apikey>"

# Fetch data from Enelogic API
# This will download all available data from the Enelogic API and save it to CSV files.
# It will skip days where a csv file already exists.
# Delete files to force a re-download.
enelogic.fetch(username, appid, appsecret, apikey)

# Bundles the data into years
# This creates yearly CSV files for easier processing
print("Bundling data into years...")
enelogic.bundle()