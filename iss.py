#!/usr/bin/python3
import requests
import json
import folium
import time
import os
from folium.plugins import AntPath
import sys

# Create a folium map centered on the initial ISS location

# Load music argument from command line
MUSIC = False
if len(sys.argv) > 1:
    MUSIC = True


OVERRIDE = False # Set to True to override the iss_data.json file

if MUSIC:
    # Play music while script is running
    music_path = os.path.join(os.path.expanduser('.'), 'audio.mp3')

    # Play music in background silently 
    os.system("afplay " + music_path + " &")
    os.system("osascript -e 'set volume output volume 100'")




m = folium.Map(location=[0, 0], zoom_start=3, tiles='CartoDB positron')

marker = folium.Marker(
    location=[0, 0],
    icon=folium.Icon(icon='rocket', prefix='fa')
    ).add_to(m)

# Save the map as an HTML file and open it in the web browser
filename = 'iss_map.html'
filepath = os.path.join(os.path.expanduser('.'), filename)
m.save(filepath)
os.system("osascript -e 'tell application \"Safari\" to set the URL of the front document to \"" + filepath + "\"'")

# Load ISS positional data from file, if available
iss_data_path = os.path.join(os.path.expanduser('.'), 'iss_data.json')

if os.path.exists(iss_data_path):
    with open(iss_data_path, 'r') as f:
        iss_data = json.load(f)
        print(iss_data)
        if OVERRIDE:
            iss_data = []



        if(iss_data is None):
            iss_data = []
else: 
    print('iss_data.json not found')
    iss_data = []


# Continuously update the ISS location every second
while True:
    # Obtain ISS location and altitude data from NASA API
    response = requests.get('http://api.open-notify.org/iss-now.json')
    data = json.loads(response.text)
    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    #altitude = int(data['iss_position']['altitude'])

    print(latitude, longitude)

    # Add current ISS position to data list
    
    iss_data.append({'latitude': latitude, 'longitude': longitude})

    # Save the data list to a file called output.json
    
    json_str = json.dumps(iss_data)

    
    if OVERRIDE is False:
        with open(iss_data_path, 'w') as f:
            f.write(json_str)
            print('Saved iss_data to iss_data.json')
        
    

    

    
    # Update the map with the new ISS location
    m.location = [latitude, longitude]

    # Update the marker with the new ISS location
    
    marker.location = [latitude, longitude]

    

    # Draw dots for each ISS location in the data list
    if iss_data:
        for point in iss_data:
            folium.CircleMarker(
                 location=[point['latitude'], point['longitude']],
                 radius=3,
                 color='red',
                 fill=True,
                 fill_color='red',
                 fill_opacity=1
            ).add_to(m)
    
    # Draw an arc between the current and previous ISS locations
    if len(iss_data) > 2:
        folium.PolyLine(
            locations=[[latitude, longitude], [iss_data[-2]['latitude'], iss_data[-2]['longitude']]],
            color='red',
            weight=1,
            opacity=1
            ).add_to(m)
        
    # Draw an arrow indicating the direction of travel using AntPath
    if len(iss_data) > 2:
        AntPath(
            locations=[[latitude, longitude], [iss_data[-2]['latitude'], iss_data[-2]['longitude']], [iss_data[-3]['latitude'], iss_data[-3]['longitude']]],
            dash_array=[1, 10],
            delay=1000,
            weight=10,
            color='black',
            pulse_color='white',
            reverse=True,
            ).add_to(m)
        
    # Draw head of arrow in the direction of travel of the ISS using a circle marker
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=5,
        color='black',
        fill=True,
        fill_color='black',
        fill_opacity=1
        ).add_to(m)
    
    #marker.tooltip = 'ISS Altitude: {} kilometers'.format(altitude)

    # Save the updated map as an HTML file
    m.save(filepath)

    # Wait for one second before the next update
    time.sleep(1)

    # Reload the map page in the web browser
    os.system("osascript -e 'tell application \"Safari\" to set the URL of the front document to \"" + filepath + "\"'")
