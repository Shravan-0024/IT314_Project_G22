import numpy as np
from sklearn.preprocessing import StandardScaler


class WeatherScaler:
    def __init__(self):
        # Domain-specific ranges and expected values
        self.feature_ranges = {
            'temperature': (0, 100),  # Typical temperature range
            'humidity': (0, 100),  # Humidity percentage
            'wind_speed': (0, 50),  # Typical wind speed range
            'precipitation': (0, 10)  # Typical precipitation range
        }

    def transform(self, data):
        """
        Custom scaling that respects domain-specific ranges

        Args:
            data (list or np.array): [temperature, humidity, wind_speed, precipitation]

        Returns:
            np.array: Scaled values between 0 and 1
        """
        scaled_data = []
        for value, (min_val, max_val) in zip(data, self.feature_ranges.values()):
            scaled_value = (value - min_val) / (max_val - min_val)
            scaled_value = max(0, min(1, scaled_value))  # Clip between 0 and 1
            scaled_data.append(scaled_value)

        return np.array(scaled_data).reshape(1, -1)


scaler = WeatherScaler()
raw_data = [40, 3, 8, 0]
scaled_data = scaler.transform(raw_data)
print(scaled_data)