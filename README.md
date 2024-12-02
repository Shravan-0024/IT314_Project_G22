# WeatherWise
Welcome to WeatherWise, a platform aimed at providing accurate and reliable weather forecasts for users. Our goal is to make weather information easy to access, helping users to stay informed and aware of up-to-date weather conditions.

## Table of Contents
1. [About our Project](#about-our-project)  
2. [Features](#features)  
3. [Technologies Used](#technologies-used)   
4. [Usage](#usage)  
6. [Acknowledgments](#acknowledgments)  
---

## About our Project
**WeatherWise** is a web-based application for users to access accurate and up-to-date weather forecasts. With WeatherWise, you can easily check the current weather, view 5-day forecasts, and get reliable information for your location or any city worldwide. The platform also allows users to save their favorite locations, manage profile, and receive personalized notifications. Whether you're planning a trip, checking daily conditions, or simply staying informed, WeatherWise makes weather forecasting easy and accessible for everyone.

---

## Features

- 🔐 **User Authentication**: Secure login/signup with email verification for account safety.
- 🧑‍💻 **User Profile**: Personalize your experience with customized user profiles. 
- ✍️ **Edit Profile**: Users can update their profile information, including email and bio.   
- 🌍 **Search Location**: Easily search for weather forecasts by city or region.  
- 💾 **Save Favorite Locations**: Keep your most visited locations saved for quick access.  
- 🌤️ **Weather Prediction for 5 Days**: Get detailed weather forecasts for the next five days.  
- 📍 **Recent Locations List**: Quick access to recently searched locations.  
- 📝 **Feedback Form**: Users can submit feedback to improve the platform, helping us provide a better experience.

---
## Technologies Used

- **Frontend**: HTML, TailWind CSS
- **Backend**: Django Web Framework, MySQL , Tensorflow (for machine learning)
- **Template Engine**: Jinja2 (for rendering dynamic HTML) 
- **API**: WeatherStack (for live weather data), Kickbox 
- **Hosting**: PythonAnywhere 
- **Testing**: Jmeter, PyTest, Selenium
  - Jmeter for Non functional testing
  - Selenium IDE for GUI testing
  - PyTest for Unit testing
- **Documentation**: Draw.io 
  - User stories, use case diagrams
  - State and Activity diagrams
  - Class diagrams
  - Sequence diagrams

---
## Usage 
- The site has already been deployed on Pythonanywhere and can be accessed using the following link : [WeatherWise](https://weatherwise.pythonanywhere.com)
- If you want to run the site on localhost download the repository from this link : [WeatherWise_Localhost](https://github.com/Shravan-0024/IT314_Project_G22.git)

### Prerequisites

1. Django framework installed on your system  
2. MySQL running locally
3. Git installed
4. Python 3.10 installed 

### Steps

1. Clone the repository:  
   ```bash
   $ git clone https://github.com/Shravan-0024/IT314_Project_G22.git

2. Navigate into the project directory:
   ```bash
   $ cd IT314_Project_G22

3. Install the required dependencies:  
   ```bash
   $ pip install -r requirements.txt

4. Set up MySQL:
   - Make sure MySQL is running locally.
   - Update the `DATABASES` configuration in `settings.py` with your MySQL credentials (e.g., username, password, database name).

5. Apply migrations to set up the database: 
   ```bash
   $ cd .\weather_wise\
   $ python manage.py migrate

6. Run the development server:  
   ```bash
   $ python manage.py runserver

7. Open your browser and go to `http://127.0.0.1:8000` i.e localhost, to see the site running locally.


## Acknowledgments
### References used:
- [Django-Course](https://www.youtube.com/playlist?list=PLu71SKxNbfoDOf-6vAcKmazT92uLnWAgy)
- [Tailwind-Tutorial](https://tailwindcss.com/docs/installation)
- [Machine Learning-Guide](https://nessie.ilab.sztaki.hu/~kornai/2020/AdvancedMachineLearning/Ng_MachineLearningYearning.pdf)

### Contributors:
- [@Rathva Karnik - 202201266](https://github.com/Karnik-Rathva)
- [@Sharvil Oza - 202201277](https://github.com/so-19)
- [@Jivani Madhav - 202201285](https://github.com/madhavJivani)
- [@Sumit Vishwakarma - 202201320](https://github.com/Sumit-320)
- [@Shrestha Thakkar - 202201323](https://github.com/SHRESTHAkkar)
- [@Kakadiya ShravanKumar - 202201333](https://github.com/Shravan-0024)
- [@Modi Nisharg - 202201346](https://github.com/Nisharg-Modi)
- [@Kanakad KrushangKumar - 202201350](https://github.com/KrushangKanakad)
- [@Bhavya Shah - 202201366](https://github.com/Bhavya3604)

---
## Raise Issus 

You can raise an issue on the GitHub repository.