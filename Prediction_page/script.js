let recentLocations = JSON.parse(localStorage.getItem("recentLocations")) || [];

function getWeather() {
  const city = document.getElementById("city").value;
  if (!city.trim()) {
    alert("Please enter a valid city name.");
    return;
  }

  document.getElementById("get-weather-btn").disabled = true;
  document.getElementById("city").disabled = true;
  document.getElementById("weather-info").classList.remove("hidden");

  const weatherData = {
    forecast: [
      { date: '2024-11-16', temp: 22, humidity: 50, precipitation: 5, windSpeed: 10, condition: 'Sunny' },
      { date: '2024-11-17', temp: 20, humidity: 60, precipitation: 10, windSpeed: 12, condition: 'Partly Cloudy' },
      { date: '2024-11-18', temp: 18, humidity: 70, precipitation: 15, windSpeed: 15, condition: 'Cloudy' },
      { date: '2024-11-19', temp: 17, humidity: 80, precipitation: 25, windSpeed: 18, condition: 'Rainy' },
      { date: '2024-11-20', temp: 16, humidity: 65, precipitation: 5, windSpeed: 8, condition: 'Showers' }
    ]
  };

  displayWeatherInfo(weatherData.forecast);

  
  recentLocations.unshift({ city, weatherData });
  if (recentLocations.length > 3) {
    recentLocations.pop();
  }

  localStorage.setItem("recentLocations", JSON.stringify(recentLocations));
  

  displayRecentLocations();

  setTimeout(() => {
    document.getElementById("get-weather-btn").disabled = false;
    document.getElementById("city").disabled = false;
  }, 1000);
}

function displayWeatherInfo(forecast) {
  const forecastContainer = document.getElementById("forecast");
  forecastContainer.innerHTML = '';

  forecast.forEach(day => {
    const dayCard = document.createElement("div");
    dayCard.classList.add("card", "fade-in");

    const iconSrc = getWeatherIcon(day.condition);

    dayCard.innerHTML = `
      <div class="card-title">${new Date(day.date).toLocaleDateString()}</div>
      <div class="weather-image-container">
        <img src="${iconSrc}" alt="${day.condition}" class="weather-icon">
      </div>
      <div class="card-content">Temp: ${day.temp}°C</div>
      <div class="card-content">Wind Speed: ${day.windSpeed} km/h</div>
      <div class="card-content">${day.condition}</div>
      <div class="weather-info">
        <span>Humidity: ${day.humidity}%</span>
        <span>Precip: ${day.precipitation}mm</span>
      </div>
    `;

    forecastContainer.appendChild(dayCard);
  });
}

function displayRecentLocations() {
  const recentLocationsContainer = document.getElementById("recent-locations");
  recentLocationsContainer.innerHTML = '';

  recentLocations.forEach(location => {
    const locationCard = document.createElement("div");
    locationCard.classList.add("recent-location");

    locationCard.innerHTML = `
      <p>${location.city}</p>
      <button class="btn" onclick="getWeatherForRecentLocation('${location.city}')">View Weather</button>
    `;
    recentLocationsContainer.appendChild(locationCard);
  });
}

function getWeatherForRecentLocation(city) {
  document.getElementById("city").value = city;
  getWeather(); 
}

function getWeatherIcon(condition) {
  switch (condition) {
    case 'Sunny':
      return 'https://cdn-icons-png.flaticon.com/512/869/869869.png'; // Sunny icon
    case 'Partly Cloudy':
      return 'https://cdn-icons-png.flaticon.com/512/1163/1163642.png'; // Partly Cloudy icon
    case 'Cloudy':
      return 'https://cdn-icons-png.flaticon.com/512/1163/1163659.png'; // Cloudy icon
    case 'Rainy':
      return 'https://cdn-icons-png.flaticon.com/512/1163/1163653.png'; // Rainy icon
    case 'Showers':
      return 'https://cdn-icons-png.flaticon.com/512/1163/1163657.png'; // Showers icon
    default:
      return 'https://cdn-icons-png.flaticon.com/512/869/869869.png'; // Default icon (sunny)
  }
}

document.getElementById("get-weather-btn").addEventListener("click", getWeather);

window.onload = displayRecentLocations;