from flask import Flask, request, jsonify
from flask_cors import CORS
import feedparser
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
weatherstack_api_key = os.getenv("57f23543a8ad8dac5e436eeab73db9ca")  # Weatherstack API key
gdacs_api_url = "https://www.gdacs.org/xml/rss.xml"

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Function to Fetch GDACS Disaster Alerts
def get_gdacs_alerts():
    feed = feedparser.parse(gdacs_api_url)
    alerts = []
    for entry in feed.entries[:5]:  # Fetch latest 5 alerts
        alerts.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary
        })
    return alerts

# Function to Fetch Weather Data from Weatherstack
def get_weather(city):
    url = f"http://api.weatherstack.com/current?access_key={weatherstack_api_key}&query={city}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "current" in data:
            current_weather = data["current"]
            temperature = current_weather["temperature"]
            weather_description = current_weather["weather_descriptions"][0]
            return f"Weather in {city}: {temperature}°C, {weather_description.capitalize()}"
        else:
            return "Unable to fetch weather data. Please check the city name."
    else:
        return "Unable to fetch weather data. Please try again later."

# Chatbot Response Function
def get_bot_response(user_input):
    user_input = user_input.lower()

    if "disaster update" in user_input:
        alerts = get_gdacs_alerts()
        response = "\n".join([f"⚠️ {a['title']} \n🔗 {a['link']}" for a in alerts])
        return response or "No recent disaster alerts."
    
    elif "weather" in user_input:
        # Extract the city name from user input
        city = user_input.split("weather in")[-1].strip()
        if city:
            return get_weather(city)
        else:
            return "Please provide a city name to check the weather."

    else:
        return "I'm here to assist you with disaster safety and updates. Ask about disaster updates or weather."

# Route to Get Disaster Alerts
@app.route('/disaster_alerts', methods=['GET'])
def disaster_alerts():
    alerts = get_gdacs_alerts()
    return jsonify({"alerts": alerts})

# Route for Chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    bot_response = get_bot_response(user_input)
    return jsonify({"response": bot_response})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
