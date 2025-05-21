from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse

app = Flask(__name__)
API_KEY = "_YOUR_API_KEY_HERE_"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    parameters = req.get('queryResult').get('parameters')
    address = parameters.get('address', {})
    city = address.get('city') if address else None
    date_time = parameters.get('date-time')

    print("Received request:", req)
    print("Parameters:", parameters)
    print("City:", city)
    print("Date-time:", date_time)

    if not city:
        print("City is None, request:", req) 
        return jsonify({
            'fulfillmentText': 'Please specify a city.',
            'outputContexts': []
        })

    # converts into local time (gmt+5)
    current_time = datetime.now(timezone.utc) + timedelta(hours=5)
    current_date = current_time.date()

    if not date_time:
        # current or the default weather option. triggered when date is not captuyred
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = round(data['main']['temp'])
            description = data['weather'][0]['description']
            fulfillment_text = f"The weather in {city} today is {temp}°C with {description}."
        else:
            fulfillment_text = f"Sorry, I couldn't find weather data for {city}."
    else:
        # Forecast module for 5 days due to freee API restrictions 
        try:
            if isinstance(date_time, str):
                requested_date = parse(date_time).date()
            else:
                requested_date = parse(date_time.get('startDateTime')).date()
            
            if requested_date < current_date:
                fulfillment_text = f"Historical weather data for {city} on {requested_date} is not available with the free API."
            elif requested_date == current_date:
                # todays date
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    temp = round(data['main']['temp'])
                    description = data['weather'][0]['description']
                    fulfillment_text = f"The weather in {city} today is {temp}°C with {description}."
                else:
                    fulfillment_text = f"Sorry, I couldn't find weather data for {city}."
            else:
                # Future date, use forecast
                url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    # Find forecast for requested date
                    for forecast in data['list']:
                        forecast_date = datetime.fromtimestamp(forecast['dt'], tz=timezone.utc).date()
                        if forecast_date == requested_date:
                            temp = round(forecast['main']['temp'])
                            description = forecast['weather'][0]['description']
                            fulfillment_text = f"The weather in {city} on {requested_date} is expected to be {temp}°C with {description}."
                            break
                    else:
                        fulfillment_text = f"No forecast available for {city} on {requested_date}."
                else:
                    fulfillment_text = f"Sorry, I couldn't find forecast data for {city}."
        except Exception as e:
            print("Error parsing date-time:", str(e))
            fulfillment_text = "Sorry, I couldn't understand the date you provided."

    return jsonify({
        'fulfillmentText': fulfillment_text,
        'outputContexts': []  # supposed to clear context but doesnt work, i tried eliminating the problem by calling it after every query but that crashed the funtion alltogether
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)





