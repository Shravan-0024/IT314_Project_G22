import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle


class WeatherScaler:
    def __init__(self):
        self.feature_ranges = {
            'temperature': (30, 100),
            'humidity': (0, 100),
            'wind_speed': (0, 50),
            'precipitation': (0, 10)
        }

    def transform(self, data):
        """Transform data to scaled format"""
        scaled_data = []
        for value, (min_val, max_val) in zip(data, self.feature_ranges.values()):
            scaled_value = (value - min_val) / (max_val - min_val)
            scaled_value = max(0, min(1, scaled_value))  # Clip values to [0,1]
            scaled_data.append(scaled_value)
        return np.array(scaled_data)

    def inverse_transform(self, scaled_data):
        """Transform scaled data back to original format"""
        unscaled_data = []
        for scaled_value, (min_val, max_val) in zip(scaled_data, self.feature_ranges.values()):
            unscaled_value = scaled_value * (max_val - min_val) + min_val
            unscaled_data.append(unscaled_value)
        return np.array(unscaled_data)


class WeatherPipeline:
    def __init__(self, model_path, sequence_length=1):
        """
        Initialize the pipeline with a pre-trained model
        Args:
            model_path: Path to the pickle file containing the trained model
            sequence_length: Length of input sequence expected by the model
        """
        self.sequence_length = sequence_length
        self.num_features = 4  # temperature, humidity, wind_speed, precipitation
        self.output_days = 5  # number of days to predict

        # Load the pre-trained model
        try:
            # First try loading as a regular keras model
            self.model = keras.models.load_model(model_path)
        except:
            try:
                # If that fails, try loading from pickle with custom objects
                with open(model_path, 'rb') as file:
                    self.model = pickle.load(file)
            except:
                # If both fail, try loading with specific keras configuration
                custom_objects = {}
                with keras.utils.custom_object_scope(custom_objects):
                    self.model = keras.models.load_model(model_path)

        # Initialize the scaler
        self.scaler = WeatherScaler()

    def prepare_input(self, input_data):
        """
        Prepare input data for prediction
        Args:
            input_data: List or numpy array of current weather values
                       [temperature, humidity, wind_speed, precipitation]
        """
        if len(input_data) != self.num_features:
            raise ValueError(f"Input data must contain {self.num_features} features")

        # Scale the input data
        scaled_data = self.scaler.transform(input_data)

        # Reshape for model input (adding batch dimension if needed)
        if self.sequence_length > 1:
            # For LSTM-type models that expect sequences
            model_input = scaled_data.reshape(1, self.sequence_length, self.num_features)
        else:
            # For models that expect single time step
            model_input = scaled_data.reshape(1, -1)

        return model_input

    def predict(self, input_data):
        """
        Make predictions for the next 5 days
        Args:
            input_data: List or numpy array of current weather values
        Returns:
            dict: Predictions for each day with both scaled and original values
        """
        # Prepare input
        model_input = self.prepare_input(input_data)

        # Make prediction
        try:
            scaled_predictions = self.model.predict(model_input)
        except AttributeError:
            # If predict method doesn't exist, try _call_
            scaled_predictions = self.model(model_input)

        # Reshape predictions if needed
        if len(scaled_predictions.shape) == 3:
            # If model outputs 3D array (batch, timesteps, features)
            scaled_predictions = scaled_predictions.reshape(self.output_days, self.num_features)
        elif len(scaled_predictions.shape) == 2:
            # If model outputs 2D array (batch, features*timesteps)
            scaled_predictions = scaled_predictions.reshape(self.output_days, self.num_features)

        # Convert scaled predictions back to original values
        original_predictions = np.array([
            self.scaler.inverse_transform(day_pred)
            for day_pred in scaled_predictions
        ])

        # Format predictions
        predictions = []
        feature_names = ['temperature', 'humidity', 'wind_speed', 'precipitation']

        for day in range(self.output_days):
            day_pred = {
                'day': day + 1,
                'scaled_values': {
                    name: float(scaled_predictions[day][i])
                    for i, name in enumerate(feature_names)
                },
                'original_values': {
                    name: float(original_predictions[day][i])
                    for i, name in enumerate(feature_names)
                }
            }
            predictions.append(day_pred)

        return predictions


def format_prediction_output(predictions):
    """Format predictions for display"""
    output = "Weather Predictions for Next 5 Days:\n"
    for pred in predictions:
        output += f"\nDay {pred['day']}:\n"
        output += f"  Temperature: {pred['original_values']['temperature']:.2f}°F\n"
        output += f"  Humidity: {pred['original_values']['humidity']:.2f}%\n"
        output += f"  Wind Speed: {pred['original_values']['wind_speed']:.2f} mph\n"
        output += f"  Precipitation: {pred['original_values']['precipitation']:.2f} inches\n"
    return output


# Example usage
if __name__ == "__main__":
    try:
        # Initialize pipeline with your model
        pipeline = WeatherPipeline('weather_prediction_model.pkl')

        # Example input data [temperature, humidity, wind_speed, precipitation]
        current_weather = [75.0, 45.0, 10.0, 0.0]

        # Make prediction
        predictions = pipeline.predict(current_weather)

        # Display results
        print(format_prediction_output(predictions))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nPlease ensure you have the following packages installed with compatible versions:")
        print("pip install tensorflow==2.13.0")
        print("pip install keras==2.13.1")
        print("pip install numpy")
        print("\nIf the error persists, you may need to save your model in a different format:")
        print("1. Load your model in the original environment")
        print("2. Save it using model.save('weather_model.h5') or tf.saved_model.save()")