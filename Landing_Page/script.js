const apiKey = 'YOUR_API_KEY';

function toggleLogin() {
  alert('Login/Signup functionality coming soon.');
}

function getWeather() {
  const location = document.getElementById('location').textContent || 'Gandhinagar,IN';
  fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${apiKey}&units=metric`)
    .then(response => response.json())
    .then(data => {
      document.querySelector('.temp').textContent = `${Math.round(data.main.temp)}°`;
      document.querySelector('.details div:nth-child(1)').innerHTML = `<img src="icons/humidity.png" alt="Humidity"> ${data.main.humidity}%`;
      document.querySelector('.details div:nth-child(2)').innerHTML = `<img src="icons/sunrise.png" alt="Sunrise"> ${formatTime(data.sys.sunrise)}`;
      document.querySelector('.details div:nth-child(3)').innerHTML = `<img src="icons/sunset.png" alt="Sunset"> ${formatTime(data.sys.sunset)}`;
      document.getElementById('location').textContent = `${data.name}, ${data.sys.country}`;
    })
    .catch(error => {
      alert('Location not found');
    });
}

function formatTime(unixTime) {
  const date = new Date(unixTime * 1000);
  const hours = date.getHours();
  const minutes = "0" + date.getMinutes();
  const ampm = hours >= 12 ? 'pm' : 'am';
  return `${hours % 12 || 12}:${minutes.substr(-2)} ${ampm}`;
}

document.addEventListener('DOMContentLoaded', () => {
  getWeather();
});
