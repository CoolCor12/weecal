"""
Created on Thu Apr 13 20:24:30 2017
Updated on Sat Apr 29 20:04:50 2017 
Author: Dillon Sienko
Program Title: weather_api
Program Description: calls weather underground api  
"""

from __future__ import print_function
import requests

def weather(state,city):
    """calls weather underground api, returns json containing 
    pertinent info
    """
    # api id
    wid = "db7f2066e9fd88ad"
    
    # city and state
    state = state.lower()
    city = city.replace(" ","_").lower()
    
    # api call
    url = "http://api.wunderground.com/api/"+wid+"/conditions/q/"+state+"/"+city+".json"
    response = requests.get(url)
    weather_json = response.json()
    
    # pull info from json
    full_loc = [weather_json['current_observation']['display_location']['full']]
    local_time = temp_f = [weather_json['current_observation']['local_time_rfc822']]
    weather = temp_f = [weather_json['current_observation']['weather']]
    feelslike_f = temp_f = [weather_json['current_observation']['feelslike_f']]
    temp_f = [weather_json['current_observation']['temp_f']]
    last_up = [weather_json['current_observation']['observation_time']]
    
    # create dictionary
    weather_dict = {'full_loc':full_loc[0], 'local_time':local_time[0], 'weather':weather[0], 'feelslike_f':str(feelslike_f[0]), 'temp_f':str(temp_f[0]),'last_up':last_up[0]}
    
    # return weather dictionary 
    return weather_dict

def weather_icon(state,city):
    
    # call weather
    weather_dict = weather(state,city)
    
    # decide which image to use
    if weather_dict['weather'] == 'Clear':
        file_dict = {'fname':'sun_img.png'} 
    elif weather_dict['weather'] == 'Partly Cloudy' or weather_dict['weather'] == 'Mostly Cloudy':
        file_dict = {'fname':'moon_clouds_img.png'}
    elif weather_dict['weather'] == 'Overcast':
        file_dict = {'fname':'rain_img.svg'}
    elif weather_dict['weather'] == 'Rain':
        file_dict = {'fname':'thunderstorm_img.png'}
    else:
        file_dict = {'fname':'weather_img_1.png'}
      
    # return dictionary including filename
    return file_dict

def print_weather():
    
    # call weather()
    weather_dict = weather()
    
    # print formatted info
    print("Location: "+weather_dict['full_loc'])
    print("Local Time: "+weather_dict['local_time'])
    print("Weather Description: "+weather_dict['weather'])
    print("Temperature(f): "+weather_dict['feelslike_f'])
    print("Feels like: "+weather_dict['temp_f'])
    print(weather_dict['last_up'])