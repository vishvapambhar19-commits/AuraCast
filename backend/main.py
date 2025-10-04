import os
import requests
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
import random

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# --- API Endpoints ---

@app.route('/api/air_data')
def get_air_data():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # --- NEW LOGIC ---
    # 1. Try AirNow first (best for North America)
    aq_data, aq_source = get_airnow_data(lat, lon)
    
    # 2. If AirNow fails, fallback to OpenAQ
    if not aq_data:
        aq_data, aq_source = get_openaq_data(lat, lon)
        
    # 3. If OpenAQ fails, fallback to WAQI
    if not aq_data:
        aq_data, aq_source = get_waqi_data(lat, lon)

    # 4. If all real sources fail, use simulated data
    if not aq_data:
        aq_data, aq_source = get_simulated_aq_data(), "(Simulated)"
    
    # Fetch Weather Data (this part remains the same)
    weather_data, weather_source = get_openmeteo_data(lat, lon)
    if not weather_data:
        weather_data, weather_source = get_simulated_weather_data(), "(Simulated)"
    
    # Combine and return
    return jsonify({
        "aq": {**aq_data, "source": aq_source},
        "weather": {**weather_data, "source": weather_source}
    })
def get_some_other_data():
    # ... function code ...
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not configured on server"}), 500
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status() # Raises an exception for bad status codes
        result = response.json()
        text_response = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No insight received.")
        return jsonify({"text": text_response})
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Could not fetch AI insights right now."}), 503

# --- Data Fetching Helper Functions ---

def get_openaq_data(lat, lon):
    try:
        url = f"https://api.openaq.org/v2/latest?coordinates={lat},{lon}&radius=50000&order_by=distance"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            measurements = data["results"][0]["measurements"]
            return {
                "pm25": next((m['value'] for m in measurements if m['parameter'] == 'pm25'), None),
                "pm10": next((m['value'] for m in measurements if m['parameter'] == 'pm10'), None),
                "o3": next((m['value'] for m in measurements if m['parameter'] == 'o3'), None),
            }, "(OpenAQ)"
    except Exception as e:
        print(f"OpenAQ Error: {e}")
    return None, None

def get_airnow_data(lat, lon):
    api_key = os.getenv("AIRNOW_API_KEY")
    if not api_key:
        print("AirNow API Key not found")
        return None, None
    
    try:
        # AirNow API endpoint for current conditions by coordinates
        url = f"https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude={lat}&longitude={lon}&distance=100&API_KEY={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data:
            # Find PM2.5 and Ozone data from the response
            pm25_data = next((item for item in data if item['ParameterName'] == 'PM2.5'), None)
            o3_data = next((item for item in data if item['ParameterName'] == 'O3'), None)
            
            return {
                "pm25": pm25_data['AQI'] if pm25_data else None, # AirNow often provides AQI directly
                "o3": o3_data['AQI'] if o3_data else None,
            }, "(AirNow)"
            
    except Exception as e:
        print(f"AirNow Error: {e}")
    return None, None

def get_waqi_data(lat, lon):
    # NOTE: Using a demo token. For production, get your own from https://aqicn.org/data-platform/token/
    token = "demo" 
    try:
        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            iaqi = data["data"].get("iaqi", {})
            return {
                "pm25": iaqi.get("pm25", {}).get("v"),
                "pm10": iaqi.get("pm10", {}).get("v"),
                "o3": iaqi.get("o3", {}).get("v"),
            }, "(AQICN)"
    except Exception as e:
        print(f"WAQI Error: {e}")
    return None, None

# Replace the old get_openmeteo_data with this one
def get_openmeteo_data(lat, lon):
    try:
        # UPDATED: Added relative_humidity_2m to the hourly request
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,rain,wind_speed_10m,relative_humidity_2m&forecast_days=1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("hourly"):
            return data["hourly"], "(Open-Meteo)"
    except Exception as e:
        print(f"Open-Meteo Error: {e}")
    return None, None

# --- Simulated Data Functions ---

def get_simulated_aq_data():
    return {
        "pm25": 25.4 + (random.random() - 0.5) * 10,
        "pm10": 45.8 + (random.random() - 0.5) * 15,
        "o3": 55.2 + (random.random() - 0.5) * 20,
    }

def get_simulated_weather_data():
    return {
        "temperature_2m": 28 + (random.random() - 0.5) * 5,
        "wind_speed_10m": 10 + (random.random() - 0.5) * 5,
        "relative_humidity_2m": 60 + (random.random() - 0.5) * 20,
    }

# --- Serve Frontend Files ---

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)
@app.route('/api/gemini_insight', methods=['POST'])
def get_gemini_insight():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not configured on server"}), 500
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status() # Raises an exception for bad status codes
        result = response.json()
        text_response = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No insight received.")
        return jsonify({"text": text_response})
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": "Could not fetch AI insights right now."}), 503
@app.route('/api/predict_aq')
def predict_aq():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # 1. Get baseline AQI with multiple fallbacks to ensure we always have a value
    current_aq, _ = get_airnow_data(lat, lon)
    if not current_aq:
        current_aq, _ = get_openaq_data(lat, lon)
    if not current_aq:
        current_aq, _ = get_waqi_data(lat, lon)
    
    # Safely get the pm25 value from whatever source was successful
    baseline_aqi = current_aq.get('pm25') if current_aq else None
    
    # If ALL real sources fail, set a default baseline to prevent a crash
    if baseline_aqi is None:
        baseline_aqi = 50 

    # 2. Get the 24-hour weather forecast
    weather_forecast, _ = get_openmeteo_data(lat, lon)
    if not weather_forecast:
        return jsonify({"error": "Could not retrieve weather forecast"}), 500

    # 3. Apply rules to generate a predicted AQI forecast
    predictions = []
    last_aqi = float(baseline_aqi)

    for i in range(24):
        wind_speed = weather_forecast['wind_speed_10m'][i]
        rain = weather_forecast['rain'][i]
        
        if wind_speed > 20: last_aqi *= 0.90
        elif wind_speed > 10: last_aqi *= 0.97
        if rain > 0.5: last_aqi *= 0.85
        elif wind_speed < 5 and rain == 0: last_aqi *= 1.02
            
        last_aqi = max(10, last_aqi)
        predictions.append(round(last_aqi, 2))

    # Return the full forecast package
    return jsonify({
        "labels": weather_forecast['time'],
        "aqi_data": predictions,
        "temp_data": weather_forecast['temperature_2m'],
        "wind_data": weather_forecast['wind_speed_10m']
    })
if __name__ == '__main__':
    app.run(debug=True)