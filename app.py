from flask import Flask, request, jsonify, render_template
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="weather_app")

API_URL = "https://api.open-meteo.com/v1/forecast"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Необходимо указать город"}), 400

    location = geolocator.geocode(city)
    if not location:
        return jsonify({"error": "Город не найден"}), 404

    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "hourly": "temperature_2m"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    return jsonify({
        "hourly": {
            "time": data["hourly"]["time"],
            "temperature_2m": data["hourly"]["temperature_2m"]
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
