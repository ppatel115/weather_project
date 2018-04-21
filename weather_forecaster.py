import urllib.request
import json
from time import sleep
from sklearn.externals import joblib


# models take in sw, se, nw, ne

high = joblib.load('high.pkl')
low = joblib.load('low.pkl')

maxwind = joblib.load('maxwind.pkl') 


# conditions models

chance_of_rain = joblib.load('chance_of_rain.pkl') 
mostly_cloudy = joblib.load('mostly_cloudy.pkl') 
partly_cloudy = joblib.load('partly_cloudy.pkl') 
thunderstorm = joblib.load('Thunderstorm.pkl')
clear = joblib.load('clear.pkl')


# my four stations, outside of target (Gainesville, FL)
sw_weather = 'KFLCHIEF2'
se_weather = 'KFLSALTS2'
nw_weather = 'KFLOBRIE3'
ne_weather = 'KFLJACKS112'
gainesville_weather = 'KFLGAINE83'

sw_forecastlink = 'http://api.wunderground.com/api/b7c207a3511cd200/forecast/q/pws:' + sw_weather + '.json'
se_forecastlink = 'http://api.wunderground.com/api/b7c207a3511cd200/forecast/q/pws:' + se_weather + '.json'
nw_forecastlink = 'http://api.wunderground.com/api/b7c207a3511cd200/forecast/q/pws:' + nw_weather + '.json'
ne_forecastlink = 'http://api.wunderground.com/api/b7c207a3511cd200/forecast/q/pws:' + ne_weather + '.json'
gainesville_forecastlink = 'http://api.wunderground.com/api/b7c207a3511cd200/forecast/q/pws:' + gainesville_weather + '.json'

f = urllib.request.urlopen(gainesville_forecastlink)
json_string = f.read()
gainesville_forecast = json.loads(json_string)
sleep(7)

f = urllib.request.urlopen(se_forecastlink)
json_string = f.read()
se_forecast = json.loads(json_string)
sleep(7)

f = urllib.request.urlopen(sw_forecastlink)
json_string = f.read()
sw_forecast = json.loads(json_string)
sleep(7)

f = urllib.request.urlopen(nw_forecastlink)
json_string = f.read()
nw_forecast = json.loads(json_string)
sleep(7)

f = urllib.request.urlopen(ne_forecastlink)
json_string = f.read()
ne_forecast = json.loads(json_string)
sleep(7)


highs = [int(sw_forecast['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit']),
         int(se_forecast['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit']), 
         int(nw_forecast['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit']), 
         int(ne_forecast['forecast']['simpleforecast']['forecastday'][1]['high']['fahrenheit'])]


lows = [int(sw_forecast['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit']),
         int(se_forecast['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit']), 
         int(nw_forecast['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit']), 
         int(ne_forecast['forecast']['simpleforecast']['forecastday'][1]['low']['fahrenheit'])]

winds = [int(sw_forecast['forecast']['simpleforecast']['forecastday'][1]['maxwind']['mph']),
         int(se_forecast['forecast']['simpleforecast']['forecastday'][1]['maxwind']['mph']), 
         int(nw_forecast['forecast']['simpleforecast']['forecastday'][1]['maxwind']['mph']), 
         int(ne_forecast['forecast']['simpleforecast']['forecastday'][1]['maxwind']['mph'])]

conditions = [sw_forecast['forecast']['simpleforecast']['forecastday'][1]['conditions'],
	         se_forecast['forecast']['simpleforecast']['forecastday'][1]['conditions'], 
	         nw_forecast['forecast']['simpleforecast']['forecastday'][1]['conditions'], 
	         ne_forecast['forecast']['simpleforecast']['forecastday'][1]['conditions']]


# Forming 'dummies' of conditions to feed to condition models
sw_clear, sw_rain, sw_mostly, sw_partly, sw_thunderstorm = 0, 0, 0, 0, 0
se_clear, se_rain, se_mostly, se_partly, se_thunderstorm = 0, 0, 0, 0, 0
ne_clear, ne_rain, ne_mostly, ne_partly, ne_thunderstorm = 0, 0, 0, 0, 0
nw_clear, nw_rain, nw_mostly, nw_partly, nw_thunderstorm = 0, 0, 0, 0, 0



for i in range (0,4):
    if (conditions[i] == 'Clear'):
        if (i == 0):
            sw_clear = 1
        elif (i == 1):
            se_clear = 1
        elif (i == 2):
            ne_clear = 1
        elif (i == 3):
            nw_clear = 1
    elif (conditions[i] == 'Chance of Rain'):
        if (i == 0):
            sw_rain = 1
        elif (i == 1):
            se_rain = 1
        elif (i == 2):
            ne_rain = 1
        elif (i == 3):
            nw_rain = 1
    elif (conditions[i] == 'Mostly Cloudy'):
        if (i == 0):
            sw_mostly = 1
        elif (i == 1):
            se_mostly = 1
        elif (i == 2):
            ne_mostly = 1
        elif (i == 3):
            nw_mostly = 1
    elif (conditions[i] == 'Partly Cloudy'):
        if (i == 0):
            sw_partly = 1
        elif (i == 1):
            se_partly = 1
        elif (i == 2):
            ne_partly = 1
        elif (i == 3):
            nw_partly = 1
    elif (conditions[i] == 'Thunderstorm'):
        if (i == 0):
            sw_thunderstorm = 1
        elif (i == 1):
            se_thunderstorm = 1
        elif (i == 2):
            ne_thunderstorm = 1
        elif (i == 3):
            nw_thunderstorm = 1
            

       
clearweather = clear.predict([[sw_clear,se_clear,ne_clear,nw_clear]])[0]
chanceofrain = chance_of_rain.predict([[sw_rain,se_rain,ne_rain,nw_rain]])[0]
mostlycloudy = mostly_cloudy.predict([[sw_mostly,se_mostly,ne_mostly,nw_mostly]])[0]
partlycloudy = partly_cloudy.predict([[sw_partly,se_partly,ne_partly,nw_partly]])[0]
thunderstormchance = thunderstorm.predict([[sw_thunderstorm,se_thunderstorm,ne_thunderstorm,nw_thunderstorm]])[0]

condition_chances = [clearweather, chanceofrain, mostlycloudy, partlycloudy, thunderstormchance]

predicted_condition = 'Clear'

max = 0.1
index = 0

for i in range(0,5) :
	if condition_chances[i] > max:
		max = condition_chances[i]
		index = i

if index == 0:
	predicted_condition = 'Clear'
elif index == 1:
	predicted_condition = 'Chance of Rain'
elif index == 2:
	predicted_condition = 'Mostly Cloudy'
elif index == 3:
	predicted_condition = 'Partly Cloudy'
elif index == 4:
	predicted_condition = 'Thunderstorm'


# Predictions other than condition
predicted_high = high.predict([highs])[0]
predicted_low = low.predict([lows])[0]
predicted_wspeed = maxwind.predict([winds])[0]


f = open('output.txt','w')
f.write('City: Gainesville, FL' + '\n')

f.write('Predicted High Temperature: ' + str(predicted_high) +'\n')
f.write('Predicted Low Temperature: ' + str(predicted_low) +'\n')
f.write('Predicted Max Wind Speed: ' + str(predicted_wspeed) +'\n')
f.write('Predicted Conditions: ' + predicted_condition +'\n')
f.close()