import numpy as np
import os
import requests
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger('custom_logger')

class WeatherScaler:
    def __init__(self):
        # Initialize feature ranges
        self.feature_ranges = {
            'temperature': (19, 110),  # still in Fahrenheit for model compatibility
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
        self.num_features = 4  # Number of features per input
        self.output_days = 5  # Number of output days

        # API endpoint for predictions
        self.api_url = "https://6660-2409-4041-2d3e-4ef4-2a-e62-c7fd-c217.ngrok-free.app/predict"

    def predict(self, input_data):
        logger.debug(f"Input data: {input_data}")
        try:
            # Make API call
            response = requests.post(
                self.api_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps({"inputs": input_data})
            )

            # Check if request was successful
            response.raise_for_status()

            # Parse API response
            api_response = response.json()
            logger.debug(f"Raw API response: {api_response}")

            # Extract predictions
            if "predictions" not in api_response:
                raise ValueError("API response does not contain 'predictions' key")

            api_predictions = api_response["predictions"]
            predictions = []

            for day_pred in api_predictions:
                # Extract information from each prediction
                prediction_entry = {
                    'date': day_pred['date'],  # Directly use 'date' from API
                    'day': day_pred['day'],    # Directly use 'day' from API
                    'scaled_values': day_pred['scaled_values'],  # Use scaled values
                    'original_values': {       # Extract and round original values
                        k: round(v, 2) for k, v in day_pred['original_values'].items()
                    }
                }

                predictions.append(prediction_entry)

            logger.debug(f"Processed predictions: {predictions}")
            return predictions

        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except (KeyError, ValueError) as parsing_error:
            logger.error(f"Error parsing API response: {parsing_error}")
            raise


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