# DE4_SIoT
Fourth Year Project for Sensing and IoT Module.
Download the app and data_collection folders to a local directory on your Raspberry Pi/computer. Make sure you have python3 and pip3 installed on your machine, and install libraries for Dark Sky API, gspread for Google Sheets and Dash. All linked below where documentation and instructions for library install can be found.

# Setting up Data Collection 
Use a microcontroller such as a Raspberry Pi to execute the data_collect.py file from your terminal. 
Before you do this you will need to set up your credentials for GDOCS and Dark Sky API.

Copy this text and save as a .json file in the format:

{
  "darksky_key": "YOUR_KEY"
}

Where YOUR_KEY is the key from Dark Sky API (set up at https://darksky.net/dev)

Follow steps to set up GDOCS OAuth 2.0 credentials here: https://gspread.readthedocs.io/en/latest/oauth2.html

Go into the data_collect.py file and set variables GDOCS_OAUTH_JSON to your google authorisation credentials, GDOCS_SPREADSHEET_NAME to the name of your Google Sheets and FREQUENCY_SECONDS to the delay you want your data to be sampled. NB Dark Sky API has a limit of 1000 calls per day for free users.
Set up your DHT11 sensor (details here: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/connecting-to-googles-docs-python3) and set PIN = the GPIO pin on the Pi that you are using in line: dhtDevice = adafruit_dht.DHT11(board.PIN) 

You should be ready to go! The names of your backup DHT11 sensor file is 'data_log1.csv' and for your weather is 'data_log2.csv' - change these in data_collect.py you want to define your back-ups as something different.

# Setting up App
Once you have your results, create a large spreadhseet on Google Sheets of your results (importing .csv files if you want). Arrange the data you want your app to use on one worksheet, and export it to a .csv called 'data_new.csv'. 
Then, ensuring 'API.py and app.py' are in the same directory, navigate to that directory in your terminal using $ cd and type in command:
$ python3 app.py

This is powered by Dash from Plot.ly, and their full documentation and tutorials can be found here: https://dash.plot.ly/getting-started

You will then get a message saying the app is running on http://XXXX:XXX
Copy that link and paste to your web browser to access the app.
