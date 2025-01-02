import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Your OpenWeatherMap API key
API_KEY = "c672af5b302955d55fd3291d2c5b596a"

# Function to fetch weather data
def get_weather():
    city = city_entry.get().strip()  # Trim whitespace
    if not city:
        result_label.config(text="Please enter a city name.", foreground="red")
        return
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        if data.get("cod") != 200:
            result_label.config(text=f"Error: {data.get('message', 'Unknown error')}", foreground="red")
            return
        
        # Extract and format weather data
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Fetch and display the weather icon
        icon_response = requests.get(icon_url)
        icon_response.raise_for_status()
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo  # Keep a reference to avoid garbage collection
        
        # Update weather details
        result_label.config(
            text=f"{city_name}\n{temp}°C\n{weather.capitalize()}",
            foreground="black"
        )
    except requests.exceptions.RequestException as e:
        result_label.config(text="Error fetching data. Check your internet connection.", foreground="red")
    except Exception as e:
        result_label.config(text=f"Unexpected error: {str(e)}", foreground="red")

# Create the GUI
app = tk.Tk()
app.title("Live Weather App")
app.geometry("300x400")

# Input field for city name
city_entry = ttk.Entry(app, width=20, font=("Arial", 14))
city_entry.pack(pady=10)
city_entry.insert(0, "Enter city")

# Search button
search_button = ttk.Button(app, text="Get Weather", command=get_weather)
search_button.pack(pady=10)

# Label to display results
result_label = ttk.Label(app, text="", font=("Arial", 16), anchor="center", wraplength=280)
result_label.pack(pady=20)

# Label to display weather icon
icon_label = ttk.Label(app)
icon_label.pack(pady=10)

# Run the app
app.mainloop()
