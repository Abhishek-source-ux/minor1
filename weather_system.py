import streamlit as st
import requests
from datetime import datetime

# OpenWeatherMap API Key
API_KEY = "d92a24b13449fe3a0712a374d07b612e"

# Function to fetch current weather
def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# Function to calculate Dew Point
def calculate_dew_point(temp, humidity):
    """
    Calculate the dew point based on temperature and humidity.
    Formula: Td = T - ((100 - RH) / 5)
    Td = Dew Point Temperature
    T = Air Temperature (in Celsius)
    RH = Relative Humidity (%)
    """
    return temp - ((100 - humidity) / 5)

# Main function for the app
def main():
    # Streamlit page configuration
    st.set_page_config(page_title="Weather Forecast", layout="wide")
    
    # Title and Input
    st.title("🌦️ Weather Forecast System")
    st.write("Enter a city name to get the current weather details.")

    # User input for city name
    city = st.text_input("Enter City Name", "London")

    if city:
        # Fetch weather data
        weather_data = get_current_weather(city)

        if weather_data.get("cod") != 200:
            st.error("City not found. Please enter a valid city name.")
        else:
            # Extract data from API response
            temp = weather_data['main']['temp']
            temp_max = weather_data['main']['temp_max']
            temp_min = weather_data['main']['temp_min']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            pressure = weather_data['main']['pressure']
            visibility = weather_data.get('visibility', 10000) / 1000  # Convert to kilometers
            uv_index = "N/A"  # UV index is not available in standard API response
            dew_point = calculate_dew_point(temp, humidity)

            # Display Weather Data
            st.subheader(f"🌍 Current Weather in {city.title()}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🌡️ Temperature", f"{temp} °C")
                st.metric("🌡️ High / Low", f"{temp_max} °C / {temp_min} °C")
                st.metric("💧 Humidity", f"{humidity}%")
                st.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
            with col2:
                st.metric("🌫️ Visibility", f"{visibility} km")
                st.metric("🧭 Pressure", f"{pressure} hPa")
                st.metric("🌡️ Dew Point", f"{dew_point:.2f} °C")
                st.metric("☀️ UV Index", uv_index)

            # Sunrise and Sunset Times
            st.subheader("🌅 Sunrise and Sunset")
            sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%I:%M %p")
            sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%I:%M %p")
            st.write(f"🌞 **Sunrise**: {sunrise}")
            st.write(f"🌜 **Sunset**: {sunset}")

# Run the app
if __name__ == "__main__":
    main()
