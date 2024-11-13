


function getWeatherPrediction() {
    const location = document.getElementById("location").value;
    const forecastContainer = document.getElementById("forecast-container");
    const locationName = document.getElementById("location-name");
    const forecast = document.getElementById("forecast");

    if (location.trim() === "") {
        alert("Please enter a location.");
        return;
    }

 
    const mockForecast = [
        { day: "Monday", high: "30°C", low: "20°C", condition: "Sunny" },
        { day: "Tuesday", high: "28°C", low: "18°C", condition: "Partly Cloudy" },
        { day: "Wednesday", high: "26°C", low: "17°C", condition: "Rainy" },
        { day: "Thursday", high: "25°C", low: "16°C", condition: "Cloudy" },
        { day: "Friday", high: "29°C", low: "19°C", condition: "Sunny" },
        { day: "Saturday", high: "32°C", low: "21°C", condition: "Sunny" },
        { day: "Sunday", high: "31°C", low: "20°C", condition: "Windy" },
    ];

   
    const conditionIcons = {
        "Sunny": "./images/sun.png",
        "Partly Cloudy": "./images/partly-cloudy.png",
        "Rainy": "./images/rainy-day.png",
        "Cloudy": "./images/cloudy.png",
        "Windy": "./images/cloud.png",
    };

   
    locationName.textContent = location;

   
    forecast.innerHTML = "";

   
    mockForecast.forEach((day) => {
        const dayDiv = document.createElement("div");
        dayDiv.classList.add("forecast-day");
        
        
        const iconSrc = conditionIcons[day.condition] || "path/to/default-icon.png";
        
        dayDiv.innerHTML = `
            <h3>${day.day}</h3>
            <p>High: ${day.high}</p>
            <p>Low: ${day.low}</p>
            <p class="text-img">${day.condition} <img src="${iconSrc}" alt="${day.condition} icon" class="condition-icon"></p>
        `;
        
        forecast.appendChild(dayDiv);
    });

    
    forecastContainer.style.display = "block";
}
