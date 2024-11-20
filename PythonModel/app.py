from flask import Flask, request, jsonify
import numpy as np
import pickle
import os

# Define the WeatherScaler class
class WeatherScaler:
    def _init_(self):
        self.feature_ranges = {
            'temperature': (30, 100),
            'humidity': (0, 100),
            'wind_speed': (0, 50),
            'precipitation': (0, 10)  # Ensure this matches the precipitation range
        }

    def transform(self, data):
        scaled_data = []
        for value, (min_val, max_val) in zip(data, self.feature_ranges.values()):
            scaled_value = (value - min_val) / (max_val - min_val)
            scaled_value = max(0, min(1, scaled_value))
            scaled_data.append(scaled_value)
        return np.array(scaled_data)

    def inverse_transform(self, scaled_data):
        unscaled_data = []
        for scaled_value, (min_val, max_val) in zip(scaled_data, self.feature_ranges.values()):
            unscaled_value = scaled_value * (max_val - min_val) + min_val
            # Clip precipitation to ensure it is non-negative
            if (min_val, max_val) == self.feature_ranges['precipitation']:
                unscaled_value = max(0, unscaled_value)
            unscaled_data.append(unscaled_value)
        return np.array(unscaled_data)


# Define the WeatherPipeline class
class WeatherPipeline:
    def _init_(self, sequence_length=1):
        self.sequence_length = sequence_length
        self.num_features = 4
        self.output_days = 5

        # Load the pre-trained model
        model_path = os.path.join(os.getcwd(), 'final4_weather_prediction_model.pkl')
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

        self.scaler = WeatherScaler()

    def prepare_input(self, input_data):
        if len(input_data) != self.num_features:
            raise ValueError(f"Input data must contain {self.num_features} features")

        scaled_data = self.scaler.transform(input_data)
        model_input = scaled_data.reshape(1, self.sequence_length, self.num_features)
        return model_input

    def predict(self, input_data):
        model_input = self.prepare_input(input_data)
        scaled_predictions = self.model.predict(model_input)
        scaled_predictions = scaled_predictions.reshape(self.output_days, self.num_features)

        original_predictions = np.array([
            self.scaler.inverse_transform(day_pred)
            for day_pred in scaled_predictions
        ])

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


# Flask app initialization
app = Flask(_name_)
pipeline = WeatherPipeline()

# Add a home route
@app.route('/')
def home():
    return "Welcome to the Weather Prediction API! Use the /predict endpoint to make predictions."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Expecting JSON input: {"inputs": [temperature, humidity, wind_speed, precipitation]}
        input_data = request.json.get('inputs')
        if not input_data:
            return jsonify({'error': 'No input data provided. Expected JSON: {"inputs": [...]}'}), 400
        
        # Perform prediction using the pipeline
        predictions = pipeline.predict(input_data)
        
        # Format the predictions for a readable response
        response = {
            'predictions': predictions
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if _name_ == "_main_":
    app.run(debug=True)