import json
from requests import get
from datetime import datetime


def dark_sky(key):

    home = ("53.842", "-0.418") #Latitude and longitude for Grovehill Road, Yorkshire
    #Dark = "https://api.darksky.net/forecast/de4380c740eeef05e8779a029a49ef2f/53.842,-0.418"
    Dark = "https://api.darksky.net/forecast/{}/{loc[0]:},{loc[1]:}?".format(key, loc=home)
    weather = get(Dark)
    currentW = json.loads(weather.text)['currently'] #Current weather data

    #Connvert UNIX time stamp to YMDHMS
    currentTime = currentW['time']
    timedate = datetime.fromtimestamp(int(currentTime)).strftime('%Y-%m-%d %H:%M:%S')

    return [timedate, currentW['cloudCover'], currentW['windSpeed'], currentW['temperature'], currentW['humidity'], currentW['icon'], currentW['precipIntensity']]

def dark_sky2(key):

    home = ("53.842", "-0.418") #Latitude and longitude for Grovehill Road, Yorkshire
    Dark = "https://api.darksky.net/forecast/{}/{loc[0]:},{loc[1]:}?".format(key, loc=home)
    weather = get(Dark)
    currentW = json.loads(weather.text)['currently'] #Current weather data
    weather_array = [currentW['cloudCover'], currentW['windSpeed'], currentW['temperature'], currentW['humidity'], currentW['precipIntensity']]
    return weather_array


