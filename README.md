# traffic_data 

Author: Michael Cole

## About

This project takes a list of start addresses as well as a list of end 
addresses and compiles traffic data over a period of time into a Pandas 
DataFrame. This was born out of a personal use in which I planned to move 
to a new city but wanted to become familiarized with traffic times to and 
from different cities.  

## How-To

Using a test editor, modify these variables:
- **INTERVAL**: Input an integer number of minutes between cycles.
For instance, if you'd like the program to collect data in 20 minutes 
intervals, type `20`.
- **DURATION**: Input an integer number of minutes the program should run. 
If you'd like for it to run for an entire day - or longer - you can input an 
equation using valid Python syntax such as `60 * 24`
*Don't forget order of operations when doing this*
- **START_ADDRESSES**: This is simply a list of start addresses as strings. 
This program uses Google Map's API so anything you would typically type into 
Google Maps should be sufficient.
- **END_ADDRESSES**: *Exactly as the previous variable*
- **GOOGLE_MAPS_API_KEY**: This is a string of your API key. This can be found 
at https://cloud.google.com/maps-platform/

### Sample

Below would create a Pandas DataFrame from every start address to every end 
address. The DataFrame would be updated every 15 minutes for an entire day.

```python
INTERVAL = 15 # Fifteen mins

DURATION = 24 * 60 # One Day

START_ADDRESSES = [
    '123 Address Lane Foo, CA 12345',
    '456 Address Cove Bar, CA 12345',
	 ]

END_ADDRESSES = [
    '1400 Suite 600 Address Street Los Angeles',
    'Statue of Liberty',
    '42 Python Ave SoftwareLand, WA'
	 ]

GOOGLE_MAPS_API_KEY = '4242SUPERSECRETAPIKEY4242'
```

