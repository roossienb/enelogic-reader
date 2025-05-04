# Enelogic Reader

The Enelogic Reader is a simple tool for interacting with the Enelogic API. It uses the `requests` library to retrieve data and stores it in daily CSV files for easy access. For analysis, the data is consolidated into a single CSV file per year per measurement.

## Features
- Fetch data from the Enelogic API.
- Store data in daily CSV files.
- Consolidate data into yearly CSV files for analysis.
- Avoid redundant API calls by skipping already downloaded data.

## Prerequisites
- Python 3.0 or higher.
- An Enelogic API key, app ID, and app secret.

## Setup and Usage
1. **Install Python**  
   Ensure you have Python 3.0 or higher installed on your system.

2. **Obtain Enelogic API Credentials**  
   - Visit the [Enelogic Developer Center](https://enelogic.com/nl/developers).
   - Add your app (the URL can be any value, e.g., `enelogic.com`).
   - Obtain your `appid` and `appsecret`.
   - Go to [My Account > Applicaties](https://enelogic.com/nl/web#/mijn-account/applicaties) to retrieve your `apikey`.

3. **Configure the Script**  
   Open `example.py` in your preferred text editor and fill in the following variables:
   - `appid`
   - `appsecret`
   - `apikey`
   - `username`

4. **Run the Script**  
   Execute the script using the following command:
   `python example.py`

5. **Access the Data**  
   The retrieved data will be stored in the `output` folder located in the same directory as the script.

## Notes
- The script skips downloading data for days that have already been processed, ensuring efficient API usage.
- To re-download all data, delete the `output` folder before running the script again.

## License
This project is licensed under the [GNU General Public License v3.0](LICENSE).