# Ellie Peatman SIoT Coursework Data Logging Main Script 2019

import sys
import time
from datetime import datetime
import json
from requests import get

import board
import adafruit_dht
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from API import dark_sky, login_open_sheet

# Google Docs oauth2 json stored locally on pi
GDOCS_OAUTH_JSON       = 'dht1-263510-9481bf4b3a96.json'
GDOCS_SPREADSHEET_NAME = 'DHT1'
# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 180

dhtDevice = adafruit_dht.DHT11(board.D4)

print('Logging sensor measurements to\
 {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')

# Attempt to get sensor reading.
temp = dhtDevice.temperature
humidity = dhtDevice.humidity

while True:
    # Login if necessary.
    
    scope =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GDOCS_OAUTH_JSON, scope)
    gc = gspread.authorize(credentials)
    doc = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Gnt-XvSGycmflCDV7WV4rwy2Nqqg3EuPgkBHT24yoE4/edit#gid=0')
    
    with open('Weather_Credentials.json') as f:
        weatherCreds = json.load(f)

    if humidity is not None or temp is not None:
        print('Temperature: {0:0.1f} C, Humidity:    {0:0.1f} %'.format(temp, humidity))
    else:
        print('Check sensor wiring')
    time.sleep(3)


    # Appending data with timestamp
    try:
        tnow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tdata = tnow + "," + str(temp) + "," + str(humidity) + "/n"
        
        weatherdata = dark_sky(weatherCreds['darksky_key'])
        print('Weather data found')
        
        with open ("/home/pi/data_log1.csv", "a") as file:
            file.write(tdata)
        print('Sensor data added to csv')
        
        with open ("/home/pi/data_log2.csv", "a") as file:
            file.write(weatherdata)
        print('Weather data added to csv')
        
        if doc is None:
            doc = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        doc.worksheet('Weather').append_row(weatherdata)
        print('Sensor data added to GDoc')
        doc.worksheet('Weather').append_row(weatherdata)
        print('Weather data added to GDoc')

    except:
        print('No weather data found')

    # Wait 3 minutes before continuing
    print('Data logged to {0}'.format(GDOCS_SPREADSHEET_NAME))
    time.sleep(FREQUENCY_SECONDS)

