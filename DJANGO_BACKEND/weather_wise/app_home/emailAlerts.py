from datetime import datetime
from .models import Notify
import requests
from .pipeline import WeatherPipeline
from .utils import send_notification_email

YOUR_ACCESS_KEY = '6d01b78a047e5aa7f1b705ad7cdbfde7'

def get_weather_forecast(city):

    url = "http://api.weatherstack.com/current"
    querystring = {"access_key": YOUR_ACCESS_KEY, "query": city}
    response = requests.get(url, params=querystring)

    if response.status_code == 200:
        data = response.json()

        if 'error' in data:
            error_message = f"Failed to get data for {city}. Please try again later."
            return None

        # Extract weather details
        weather_info = {
            'temperature': float(data['current']['temperature']),
            'humidity': float(data['current']['humidity']),
            'wind_speed': float(data['current']['wind_speed']),
            'precipitation': float(data['current']['precip']),
        }

        # Use the extracted data for prediction
        input_data =[weather_info['temperature'], weather_info['humidity'],
                    weather_info['wind_speed'], weather_info['precipitation']]
        
        predictions = None  # Initialize predictions to handle errors
        try:
            # Load the prediction pipeline
            pipeline = WeatherPipeline()
            predictions = pipeline.predict(input_data)
            error_message = 'none'
            return predictions
        except Exception as e:
            error_message = "An error occurred during prediction. Please try again later."
            predictions = None
            return predictions
    else:
        error_message = f"API call failed with status code {response.status_code}. Please try again later."
        return None
    
# Default thresholds for all City's for alerts (will change in future versions)
THRESHOLDS = {
    "temperature": {"min": -5, "max": 45},  # in Degrees Celsius
    "humidity": {"min": 20, "max": 90},      # in Percentage
    "wind_speed": {"max": 30},              # in km/h
    "precipitation": {"max": 50},            # in mm
}

def check_weather_alerts():

    users = Notify.objects.filter(get_notifications=True)

    for user_notify in users:
        preferred_location = user_notify.preferred_location
        user_email = user_notify.user.email

        # Get 5-day forecast for the preferred location
        Predictions = get_weather_forecast(preferred_location) 

        if not Predictions:
            print(f"Could not fetch forecast for {preferred_location}.")
            continue

        alerts = []
        for predictions in Predictions["predictions"]:
            if (
                predictions["original_values"]["temperature"] < THRESHOLDS["temperature"]["min"]
                or predictions["original_values"]["temperature"] > THRESHOLDS["temperature"]["max"]
                or predictions["original_values"]["humidity"] < THRESHOLDS["humidity"]["min"]
                or predictions["original_values"]["humidity"] > THRESHOLDS["humidity"]["max"]
                or predictions["original_values"]["wind_speed"] > THRESHOLDS["wind_speed"]["max"]
                or predictions["original_values"]["precipitation"] > THRESHOLDS["precipitation"]["max"]
            ):
                alerts.append(predictions)

        # If there are alerts, send an email to the user
        if alerts:
            subject = "Weather Alert for Your Preferred Location"
            message = f"""
            Dear {user_notify.user.username},

            There are weather alerts for your preferred location, {preferred_location}, in the next 5 days:
            """
        
            for alert in alerts:
                message += f"""
                Date: {alert['date']}
                """
                
                # Temperature Alert
                if alert['original_values']['temperature'] < THRESHOLDS['temperature']['min']:
                    message += f"- Low Temperature Alert: {alert['temperature']}°C \n"
                elif alert['original_values']['temperature'] > THRESHOLDS['temperature']['max']:
                    message += f"- High Temperature Alert: {alert['temperature']}°C \n"
                
                # Humidity Alert
                if alert['original_values']['humidity'] < THRESHOLDS['humidity']['min']:
                    message += f"- Low Humidity Alert: {alert['humidity']}%\n"
                elif alert['original_values']['humidity'] > THRESHOLDS['humidity']['max']:
                    message += f"- High Humidity Alert: {alert['humidity']}%\n"
                
                # Wind Speed Alert
                if alert['original_values']['wind_speed'] > THRESHOLDS['wind_speed']['max']:
                    message += f"- High Wind Speed Alert: {alert['wind_speed']} km/h\n"
                
                # Precipitation Alert
                if alert['original_values']['precipitation'] > THRESHOLDS['precipitation']['max']:
                    message += f"- High Precipitation Alert: {alert['precipitation']} mm\n"
            
            # Closing message
            message += "\nStay safe and take necessary precautions.\n\n- WeatherWise Team"

            # Send email
            if send_notification_email(subject, message, [user_email]):
                print(f"Alert sent to {user_email}.")
            else:
                print(f"Failed to send alert to {user_email}.")

