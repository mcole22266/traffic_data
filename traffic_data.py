# traffic_data.py - Program to collect data from various start addresses to 
#                   various end addresses.  Designed to run on designated 
#                   intervals for a designated amount of time
#
# Author: Michael Cole
# =============================================================================

# Boiler Plate and User-Specified Variables ===================================
from datetime import datetime
import time
import pandas as pd
import googlemaps

# In Minutes
INTERVAL = # Integer number of minutes between cycles in which travel data 
           # should be collected
DURATION = # Integer number of minutes until this program terminates 

START_ADDRESSES = [
        # Insert start addresses as strings separated by commas
        ]
END_ADDRESSES = [
        # Insert end addresses as strings separated by commas 
        ]
GOOGLE_MAPS_API_KEY = # String. Visit: https://cloud.google.com/maps-platform/  

# Variables and Functions =====================================================
#              !!! MODIFY BELOW THIS LINE AT YOUR OWN RISK !!! 
# _____________________________________________________________________________
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_duration(start_address, end_address):
    '''Returns 'duration_in_traffic' from Google API'''
    results = gmaps.directions(start_address, end_address, 
                               mode='driving', departure_time=datetime.now())
    # try/except to cover circumstances in which Google API doesn't deliver.
    try:
        results = results[0]['legs'][0]['duration_in_traffic']['text']
    except:
        results = None
    return results


def get_info(reverse=False):
    '''Returns timestamp (datetime.now().ctime()) and a dataframe which can 
    later be appended in a list of dataframes for concatenation.
    Param:
        reverse=False : Set True to evaluate trip from work to home
    '''
    now = datetime.now().ctime()
    df = pd.DataFrame(index=START_ADDRESSES, columns=END_ADDRESSES)
    if not reverse:
        print()
        print('Home to work ==========')
    if reverse:
        print()
        print('Work to home ==========')
    for home in df.index:
        for work in df.columns:
            if not reverse:
                duration = get_duration(home, work)
                df[work][home] = duration
                print(f'{home} to {work}: {duration}')
            if reverse:
                duration = get_duration(work, home)
                df[work][home] = duration
                print(f'{work} to {home}: {duration}')
    print()
    print('----- done -----')
    return now, df

def read_csv(filename='traffic_data_forward.csv', reverse=False):
    '''Reads csv into pandas dataframe while preserving the multi-indexing.
    Param:
        filename='traffic_data_forward.csv'
        reverse=False : Set to true in order to read the reverse csv file
    '''
    if reverse:
        filename='traffic_data_reverse.csv'
    df = pd.read_csv(filename, index_col=[0,1])
    return df

def save_dataframe(dataframe, filename='traffic_data_forward', 
             reverse=False, csv=True, html=True):
    '''Writes the given dataframe to a csv file and html.
    Param:
        dataframe : The dataframe that will be written to csv
        filename='traffic_data_forward.csv'
        reverse=False : Set to True if given dataframe is reversed so the csv 
                        file will be saved correctly
        csv=True : Set False to avoid saving csv file
        html=True : Set False to avoid saving html file
    '''
    if reverse:
        filename='traffic_data_reverse'
    if csv:
        dataframe.to_csv(filename+'.csv')
        print(f'----- Dataframe saved as {filename}.csv -----')
    if html:
        dataframe.to_html(filename+'.html')
        print(f'----- Dataframe saved as {filename}.html -----')

def timer_complete(max_seconds):
    '''Loops until a timer is complete.  Then returns True'''
    start_time = time.time()
    elapsed_time = start_time - time.time()
    while elapsed_time < max_seconds:
        print('Checking elapsed time')
        time.sleep(60) # check every minute
        elapsed_time = time.time() - start_time
    return True

def elapsed_time_complete(max_seconds, start_time):
    '''Returns whether or not the elapsed time has exceeded the limit'''
    elapsed = time.time() - start_time
    return elapsed > max_seconds

# Scripting ===================================================================
def run_program():
    '''Wrapper function that calls all necessary previous functions.'''
    interval_seconds = INTERVAL * 60   # convert to seconds
    duration_seconds = DURATION * 60   # convert to seconds
    start_time = time.time()

    # Will break when timer completes:
    while not elapsed_time_complete(duration_seconds, start_time):
        forward_data_dict = {}   # Create an empty dictionary
        timestamp, dataframe = get_info()  # Read data into tuple
        forward_data_dict[timestamp] = dataframe   # Insert tuple into data 
                                                   # dictionary
        forward_dataframe = pd.concat(forward_data_dict)  # Concat dict into 
                                                          # dataframe -
                                                          # (multi-index) 
        # Repeat for backward data ----
        backward_data_dict = {}   # Create an empty dictionary
        timestamp, dataframe = get_info(reverse=True)  # Read data into
                                                       # tuple
        backward_data_dict[timestamp] = dataframe   # Insert tuple into 
                                                    # data dictionary
        backward_dataframe = pd.concat(backward_data_dict)   # Concat dict 
                                             # into dataframe (multi-index) 

        # Forward: Try to read in old data - if first time, this is skipped
                 # then write to csv and html
        try:
            old_forward_dataframe = read_csv()
            forward_dataframe = old_forward_dataframe.append(forward_dataframe)
        except:
            pass
        save_dataframe(forward_dataframe)

        # Backward: Repeat with reverse
        try:
            old_backward_dataframe = read_csv(reverse=True)
            backward_dataframe = old_backward_dataframe.append(backward_dataframe)
        except:
            pass
        save_dataframe(backward_dataframe, reverse=True)
        while not timer_complete(interval_seconds):
            pass

    print('===== Done Collecting Data =====')

# Main Guard ==================================================================
if __name__ == '__main__':
    run_program()
