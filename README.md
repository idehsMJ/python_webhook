Hey so this is the webhook which runs REST APIs and connects the Dialogflow to OpenWeather services

get your own OpenWeather API key by signing up here: https://openweathermap.org
run the file by simply typing "python webhook.py" and you should see it running on your local server 
for it to work, run "ngrok {port}" -5000 in this case. 
then take the https URL and paste it in the fullfilment "webhook" section of dialogflow which will connect the service to the bot.
Now test the bot in the top right corner labelled "Try it now".


### IMPORTANT ###
in the current version run the same query twice to get the result 
as for the 8 day forecast, the free api only lets you get data 5 days ahead.
visit the site https://openweathermap.org for their different API calls which forecasts for different time brackets