#!/usr/local/bin/python3.6

from configparser import ConfigParser
from uszipcode import SearchEngine
import subprocess
import argparse
import requests
import logging
import json
import time
import os
import re

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="enable verbose logging", action="store_true")
    parser.add_argument("-t", "--toggle-fc-type", help="toggle between short and long forecast", action="store_true")
    parser.add_argument("-n", "--notify-5day-fc", help="send 5 day forecast to send-notfiy", action="store_true")
    args = parser.parse_args()
    return args

def conf_creator():
    os.makedirs(conf_path)
    if not os.path.exists(conf_file):
        cp.add_section('weather')
        cp.set('weather', 'use_geoloc', 'true')
        cp.set('weather', 'zipcode', '10001')
        cp.set('weather', 'cache_ageout', '900')
        cp.set('weather', 'forecast_type', 'short')
        with open(conf_file, 'w') as configfile:
            cp.write(configfile)
        logging.debug("WRITING: " + conf_file)

def debug_config():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("---START CONFIG---")
    logging.debug("conf_file: " + conf_file)
    logging.debug("cache_file: " + cache_file)
    logging.debug("zipcode: " + zipcode)
    logging.debug("cache_ageout: " + cache_ageout)
    logging.debug("forecat_type: " + fc_type)
    if use_geoloc:
        logging.debug("use_geoloc: true")
    else:
        logging.debug("use_geoloc: false")
    logging.debug("---END CONFIG---")

def conf_parser(config_file):
    cp.read(config_file)
    return cp._sections["weather"]

def fc_location(zipcode, use_geoloc):
    if use_geoloc:
        logging.debug("use_geoloc: true")
        location = requests.get('https://ipinfo.io/json')
        json = location.json()
        location = json['loc']
    else:
        logging.debug("use_geoloc: true")
        search = SearchEngine()
        zip = search.by_zipcode(zipcode).to_dict()
        latlong = zip['lat'],zip['lng']
        location = ("{0[0]},{0[1]}").format(latlong)
    return fc_get_url(location)

def fc_get_url(location):
    logging.debug("WEATHER.GOV ENTRY URL: https://api.weather.gov/points/%s" % location)    
    fc_url = ("https://api.weather.gov/points/{0}").format(location)
    response = fc_url_response(fc_url)
    json = response.json()
    fc_url = json["properties"]["forecast"]
    loc = json["properties"]["relativeLocation"]["properties"]["city"] + ", " + json["properties"]["relativeLocation"]["properties"]["state"]
    logging.debug("WEATHER.GOV FORECAST URL: " + fc_url)    
    logging.debug("WEATHER.GOV FORECAST LOCATION: " + loc)    
    return [fc_url, loc];

def fc_url_response(fc_url):
    logging.debug("TESTING URL : " + fc_url)
    response = requests.get(fc_url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.debug(e)
        return False
    else:
        return response

def fc_type_toggle(fc_type):
    logging.debug("TOGGLE FORECAST TYPE: " + fc_type )
    if fc_type == "short":
        cp.set('weather', 'forecast_type', 'long')
    elif fc_type == "long":
        cp.set('weather', 'forecast_type', 'short')
    with open(conf_file, 'w') as conf:
        cp.write(conf)

def fc_refresh(cache_ageout):
    current_time = int(time.time())
    cache_mod = int(os.stat(cache_file).st_mtime)
    conf_mod = int(os.stat(conf_file).st_mtime)
    logging.debug("CURRENT TIME: " + str(current_time))
    logging.debug("CONF AGE: " + str(current_time - conf_mod))
    logging.debug("CACHE AGE: " + str(current_time - cache_mod))
    if (current_time - conf_mod) == "0":
        logging.debug("Confile file is NEW! REFRESHING")
        logging.debug(conf + "is 0")
    elif (current_time - conf_mod) < (current_time - cache_mod):
        logging.debug("Conf file is newer than Cache file!! REFRESHING ")
    elif (current_time - cache_mod) > int(cache_ageout):
        logging.debug("Cache file is older than " + cache_ageout + "!! REFRESHING ")
    elif (current_time - cache_mod) < int(cache_ageout):
        logging.debug("Cache file is newer than " + cache_ageout + " EXITING")
        return False
    return True

def fc_get_icon(icon, isDaytime):
    icon = re.findall(r"\/icons\/.*\/.*\/([^,\?]*)", icon)[0]
    if isDaytime:
        icons = { "skc": "", "few": "", "sct": "", "bkn": "", "ovc": "", "wind_skc": "", "wind_few": "", "wind_sct": "", "wind_bkn": "", "wind_ovc": "", "snow": "", "rain_snow": "", "rain_sleet": "", "snow_sleet": "", "fzra": "", "rain_fzra": "", "snow_fzra": "", "sleet": "", "rain": "", "rain_showers": "", "rain_showers_hi": "", "tsra": "", "tsra_sct": "", "tsra_hi": "", "tornado": "", "hurricane": "", "tropical_storm": "", "dust": "", "smoke": "", "haze": "", "hot": "", "cold": "", "blizzard": "", "fog": "" }
    else:
        icons = { "skc": "", "few": "", "sct": "", "bkn": "", "ovc": "", "wind_skc": "", "wind_few": "", "wind_sct": "", "wind_bkn": "", "wind_ovc": "", "snow": "", "rain_snow": "", "rain_sleet": "", "snow_sleet": "", "fzra": "", "rain_fzra": "", "snow_fzra": "", "sleet": "", "rain": "", "rain_showers": "", "rain_showers_hi": "", "tsra": "", "tsra_sct": "", "tsra_hi": "", "tornado": "", "hurricane": "", "tropical_storm": "", "dust": "", "smoke": "", "haze": "", "hot": "", "cold": "", "blizzard": "", "fog": "" }
    return icons.get(icon, "?")

def fc_get_windicon(windSpeed, windDir):
    windSpeed = re.match(r"^(\d+)", windSpeed)
    speedIcons = { "0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "12": "" }
    dirIcons = { ("N", "NNE", "NNW"): "", "NE": "", ("E", "ENE", "ESE"): "", "SE": "", ("S", "SSE", "SSW"): "", "SW": "", ("W", "WSW", "WNW"): "", "NW": "" }
    windSpeed = speedIcons.get(windSpeed.group(0))
    windDir = next(v for k, v in dirIcons.items() if windDir in k)
    opts = windDir,windSpeed
    icon = "{0[0]} {0[1]}".format(opts)
    return icon

def fc_get_json(fc_url, fc_type):
    if args.notify_5day_fc:
        fc = requests.get(fc_url)
    else:
        fc = requests.get(fc_url + "/hourly")
    return fc.json()

def fc_format(fcjson):
    isDaytime = fcjson["properties"]["periods"][0]["isDaytime"]
    temp = str(fcjson["properties"]["periods"][0]["temperature"]) + "°F"
    windSpeed = fcjson["properties"]["periods"][0]["windSpeed"]
    windDir = fcjson["properties"]["periods"][0]["windDirection"]
    windIcon = fc_get_windicon(windSpeed, windDir)
    desc = fcjson["properties"]["periods"][0]["shortForecast"]
    icon = fc_get_icon(fcjson["properties"]["periods"][0]["icon"], isDaytime)
    if fc_type == "short":
        options = icon,temp
        message = "{0[0]} {0[1]}".format(options)
    if fc_type == "long":
        options = icon,temp,windIcon,desc
        message = "{0[0]} {0[1]} {0[2]} {0[3]}".format(options)
    return message

def fc_write_cache(message):
    logging.debug("Writing cache..")
    with open(cache_file, 'w') as cache:
        cache.write(message)

def fc_5day(fcjson, loc):
    isDaytime = fcjson["properties"]["periods"][0]["isDaytime"]
    upcoming = fcjson["properties"]["periods"][0]["name"]
    temp = str(fcjson["properties"]["periods"][0]["temperature"]) + "°F"
    detailedForecast = fcjson["properties"]["periods"][0]["detailedForecast"]
    icon = fc_get_icon(fcjson["properties"]["periods"][0]["icon"], isDaytime)
    options = loc,upcoming, temp, icon, detailedForecast
    forecast = "{0[0]}\n\n{0[1]} - {0[2]} {0[3]}\n{0[4]}".format(options)
    subprocess.Popen(['notify-send', "-t", "100000", forecast])

cp = ConfigParser()
args = arg_parser()

## config and cache files
conf_path = os.environ.get("HOME") + "/.config/polybar/scripts/"
conf_file = conf_path + "py_scripts.conf"
cache_file = conf_path + "py_weather.cache"

## set varibles from config
config = conf_parser(conf_file)
use_geoloc = cp.getboolean('weather', 'use_geoloc')
fc_type = config['forecast_type']
cache_ageout = config['cache_ageout']
zipcode = config['zipcode']

while True:
    if args.verbose:
        debug_config()
    if not os.path.exists(conf_path):
        conf_creator()
    if args.notify_5day_fc:
        fc_url,loc = fc_location(zipcode, use_geoloc)
        fcjson = fc_get_json(fc_url, fc_type)
        fc_5day(fcjson, loc)
        break
    if args.toggle_fc_type:
        fc_type_toggle(fc_type)
    if fc_refresh(cache_ageout):
        fc_url,loc = fc_location(zipcode, use_geoloc)
        fcjson = fc_get_json(fc_url, fc_type)
        forecast = fc_format(fcjson)
        fc_write_cache(forecast)
    with open(cache_file, 'r') as cache:
        logging.debug("Reading cache..")
        message = cache.read()
    print(message)
    break
