import numpy as np
import pickle
import os
from datetime import datetime, timedelta
from django.conf import settings



class WeatherScaler:
    def __init__(self):
        # Initialize feature ranges
        self.feature_ranges = {
            'temperature': (19, 110),#still in Fahrenheit for model compatibility
            'humidity': (20, 90),
            'wind_speed': (0, 50),
            'precipitation': (0, 20)
        }

    def transform(self, data):
        """
        Scale the input data to a range of 0 to 1 based on feature ranges.
        """
        scaled_data = []
        for value, (min_val, max_val) in zip(data, self.feature_ranges.values()):
            scaled_value = (value - min_val) / (max_val - min_val)
            scaled_value = max(0, min(1, scaled_value))  # Ensure scaled values are between 0 and 1
            scaled_data.append(scaled_value)
        return np.array(scaled_data)
    

    def inverse_transform(self, scaled_data):
        """
        Convert scaled data back to the original range.
        """
        unscaled_data = []
        for scaled_value, (min_val, max_val) in zip(scaled_data, self.feature_ranges.values()):
            unscaled_value = scaled_value * (max_val - min_val) + min_val
            if min_val == 0 and max_val == 20:  # Handle precipitation specifically
                unscaled_value = max(0, unscaled_value)
            unscaled_data.append(unscaled_value)
        return np.array(unscaled_data)
    

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

class WeatherPipeline:
    def __init__(self, sequence_length=1):
        self.sequence_length = sequence_length  # Input sequence length for the model
        self.num_features = 4                   # Number of features per input
        self.output_days = 5                    # Number of output days

        # Locate the model file using Django's BASE_DIR
        model_path = os.path.join(settings.BASE_DIR, 'final4_weather_prediction_model.pkl')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        # Load the model
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        # Initialize the scaler
        self.scaler = WeatherScaler()


    def prepare_input(self, input_data):
        """
        Prepare input data for the model by scaling and reshaping it.
        """
        if len(input_data) != self.num_features:
            raise ValueError(f"Input data must contain {self.num_features} features")

        # Scale the input data
        scaled_data = self.scaler.transform(input_data)

        # Reshape data for model input
        model_input = scaled_data.reshape(1, self.sequence_length, self.num_features)
        return model_input

    
    def predict(self, input_data):
        """
        Generate predictions using the trained model.
        """
        # Prepare the input data
        model_input = self.prepare_input(input_data)
        # Get predictions from the model
        scaled_predictions = self.model.predict(model_input)
        # Reshape predictions for multiple output days
        scaled_predictions = scaled_predictions.reshape(self.output_days, self.num_features)
        # Convert predictions back to the original scale
        original_predictions = np.array([
            self.scaler.inverse_transform(day_pred)
            for day_pred in scaled_predictions
        ])
        # Prepare predictions in a structured format
        predictions = []
        feature_names = ['temperature', 'humidity', 'wind_speed', 'precipitation']
        start_date = datetime.now() + timedelta(days=1)
        for day in range(self.output_days):
            current_date = start_date + timedelta(days=day)
            original_values = {}
            for i, name in enumerate(feature_names):
                value = float(original_predictions[day][i])
                if name == 'temperature':
                    value = fahrenheit_to_celsius(value)
                original_values[name] = round(value, 2)
            
            day_pred = {
                'date': current_date.strftime('%Y-%m-%d'),
                'day': current_date.strftime('%A'),
                'scaled_values': {
                    name: float(scaled_predictions[day][i])
                    for i, name in enumerate(feature_names)
                },
                'original_values': original_values
            }
            predictions.append(day_pred)
        return predictions
        
        

def format_prediction_output(predictions):
    """
    Format predictions into a user-friendly string.
    """
    output = "Weather Predictions for the Next 5 Days:\n"
    for pred in predictions:
        output += f"\nDay {pred['day']}:\n"
        output += f"  Temperature: {pred['original_values']['temperature']:.2f}°F\n"
        output += f"  Humidity: {pred['original_values']['humidity']:.2f}%\n"
        output += f"  Wind Speed: {pred['original_values']['wind_speed']:.2f} mph\n"
        output += f"  Precipitation: {pred['original_values']['precipitation']:.2f} inches\n"
    return output


if __name__ == "__main__":
    # Example usage of the pipeline
    pipeline = WeatherPipeline()

    # Example input: [temperature, humidity, wind_speed, precipitation]
    current_weather = [75.0, 45.0, 10.0, 0.0]
    predictions = pipeline.predict(current_weather)
