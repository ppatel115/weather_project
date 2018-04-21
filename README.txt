Weather Forecast -
Script to predict the weather in a city given the forecasts of four exterior weather stations

Usage -
Keep .pkl files in the same directory as weather_forecaster, those files hold the models I created to predict the various parts of the forecast

Windows:
 > py -3 weather_forecaster.py
Linux:
 > python3 weather_forecaster.py


Solution Description:

I chose the city of Gainesville, FL with exterior forecasts from:
	 Chiefland Sky Ranch, Chiefland, FL
	 North Shore Little Lake Kerr, Salt Springs, FL
	 O'Brien, FL
	 Lazy Dogs Ranch, Baldwin, FL

I initially started by gathering historical weather data from the Wunderground API (https://www.wunderground.com/weather/api/d/docs?d=data/history),
 but after gathering it, I realized the response did not actually contain some of the data that it was supposed to, like conditions. As a result, 
I decided to use the 10 day forecast from the Wunderground API (https://www.wunderground.com/weather/api/d/docs?d=data/forecast10day) to build my 
models. In my 10day_forecast Jupyter Notebook, I gathered the relevant data and filled out a .csv which I used to create my models. After creating 
the .csv, I opened the data in another notebook, forecast_model.ipynb, where I used pandas and scikit-learn's LinearRegression to train and test my 
models on the csv data. Finally, I loaded my models and four forecasts of the next day (from whenever the program is run) in weather_forecaster.py, 
and ran my models on the forecast data to produce my output in "output.txt".


Solution Limitations:

The maximum windspeed model is not as accurate as the other models, possibly because windspeed is more variable across distance than other weather 
features. Additionally, I am not sure how accurate the condition model is when the given forecasts disagree on conditions. I believe this is due to 
the small amount of data I used to create it, but it could also be due to how I created the model (Linear regression of dummy variables), because 
this was my first experience with categorical variable modeling. 