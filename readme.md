# 🛰️ ISS Visualizer

ISS Visualizer is a simple web application that shows the current location of the International Space Station (ISS) on a map. 

## Installation

1. Clone the repository
2. Install python dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. Open `iss_map.html` in your browser.

# How to use

The application will automatically update the ISS location every 1 second. It also saves the ISS location history in a file called `iss_data.json`. You can use this file to plot the ISS path on a map.

# Libraries used

- [folium]() - Python library for creating interactive maps
- [requests]() - Python library for making HTTP requests
- [json]() - Python library for working with JSON files
- [time]() - Python library for working with time
- [os]() - Python library for working with operating system

