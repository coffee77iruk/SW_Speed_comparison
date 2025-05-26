"""
Preprocessing of the persistence OMNI data for comparison with the SWspeed data.

We prepare the these persistence data. 
(1) Persistence (3 days)
(2) Persistence (4 days)
(3) Persistence (5 days)
(4) Persistence (27 days)

"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# file path
omni_file_path = "E:/Research/SWspeed/omni_data/omni2_data.txt"
CR_file_path = 'E:/Research/SWspeed/Carrington_Rotation_Data__Oct-Dec__2010-2020_.csv'

# read file
with open(omni_file_path, 'r') as file:
    lines = file.readlines()

header_lines = []
data_lines = []

header_ended = False
for line in lines:
    if 'YEAR' in line:
        header_ended = True
    if not header_ended:
        header_lines.append(line)
    else:
        data_lines.append(line)

# Preprocessing
data = []
for line in data_lines[1:]:  # skipe the first line ('YEAR DOY HR')
    parts = line.split()
    year, doy, hr, _, plasma_speed = parts
    year, doy, hr = int(year), int(doy), int(hr)
    plasma_speed = float(plasma_speed)
    date = datetime(year, 1, 1) + timedelta(days=doy-1, hours=hr)
    data.append([date, plasma_speed])

df = pd.DataFrame(data, columns=['Datetime', 'Plasma_Speed'])

df['Persistence_3days']= df['Plasma_Speed'].shift(24*3)
df['Persistence_4days']= df['Plasma_Speed'].shift(24*4)
df['Persistence_5days']= df['Plasma_Speed'].shift(24*5)
df['Persistence_27days']= df['Plasma_Speed'].shift(24*27)

# Filtering over the period of October-December for the years 2012-2020
df = df[(df['Datetime'].dt.month >= 10) & (df['Datetime'].dt.month <= 12)]
df = df[(df['Datetime'].dt.year >= 2012) & (df['Datetime'].dt.year <= 2020)]

# Resampling to 6 hours
df_resampled = df[df['Datetime'].dt.hour.isin([0, 6, 12, 18])].copy()

# Convert to string format
df_resampled.loc[:, 'Datetime_str'] = df_resampled['Datetime'].dt.strftime('%Y-%m-%d %H:%M')

# Convert to dictionary format
persistence_3days_dict = {
    'decimal_day': df_resampled['Datetime_str'].tolist(),
    'Persistence_3days': df_resampled['Persistence_3days'].tolist()
}

persistence_4days_dict = {
    'decimal_day': df_resampled['Datetime_str'].tolist(),
    'Persistence_4days': df_resampled['Persistence_4days'].tolist()
}

persistence_5days_dict = {
    'decimal_day': df_resampled['Datetime_str'].tolist(),
    'Persistence_5days': df_resampled['Persistence_5days'].tolist()
}

persistence_27days_dict = {
    'decimal_day': df_resampled['Datetime_str'].tolist(),
    'Persistence_27days': df_resampled['Persistence_27days'].tolist()
}

CR_df = pd.read_csv(CR_file_path)


def Persistence_3days(cr):
    cr_data = CR_df[CR_df['Carrington Rotation Number'] == cr]
    
    start_date = cr_data.iloc[0]['Start Date']
    end_date = cr_data.iloc[0]['End Date']
    #year = start_date.year
    
    # convert to datetime format
    start_date = pd.to_datetime(start_date) # '2013-12-19 06:11'
    end_date = pd.to_datetime(end_date)
    
    current_time = start_date
    persistence_time = []
    persistence = []
    
    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                omni_date = persistence_3days_dict['decimal_day']
                
                for d in range(len(omni_date)):
                    if string_time in omni_date[d]:
                        if float(persistence_3days_dict['Persistence_3days'][d]) > 900:
                            persistence_time.append(np.nan)
                            persistence.append(np.nan)
                        else:
                            persistence_time.append(persistence_3days_dict['decimal_day'][d])
                            persistence.append(float(persistence_3days_dict['Persistence_3days'][d]))
            
            else:
                persistence_time.append(np.nan)
                persistence.append(np.nan)
                
            current_time += timedelta(hours=6)
            
        else:   
            current_time += timedelta(hours=1)
            
    return persistence_time, persistence

def Persistence_4days(cr):
    cr_data = CR_df[CR_df['Carrington Rotation Number'] == cr]
    
    start_date = cr_data.iloc[0]['Start Date']
    end_date = cr_data.iloc[0]['End Date']
    #year = start_date.year
    
    # convert to datetime format
    start_date = pd.to_datetime(start_date) # '2013-12-19 06:11'
    end_date = pd.to_datetime(end_date)
    
    current_time = start_date
    persistence_time = []
    persistence = []
    
    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                omni_date = persistence_4days_dict['decimal_day']
                
                for d in range(len(omni_date)):
                    if string_time in omni_date[d]:
                        if float(persistence_4days_dict['Persistence_4days'][d]) > 900:
                            persistence_time.append(np.nan)
                            persistence.append(np.nan)
                        else:
                            persistence_time.append(persistence_4days_dict['decimal_day'][d])
                            persistence.append(float(persistence_4days_dict['Persistence_4days'][d]))
            
            else:
                persistence_time.append(np.nan)
                persistence.append(np.nan)
                
            current_time += timedelta(hours=6)
            
        else:   
            current_time += timedelta(hours=1)
            
    return persistence_time, persistence

def Persistence_5days(cr):
    cr_data = CR_df[CR_df['Carrington Rotation Number'] == cr]
    
    start_date = cr_data.iloc[0]['Start Date']
    end_date = cr_data.iloc[0]['End Date']
    #year = start_date.year
    
    # convert to datetime format
    start_date = pd.to_datetime(start_date) # '2013-12-19 06:11'
    end_date = pd.to_datetime(end_date)
    
    current_time = start_date
    persistence_time = []
    persistence = []
    
    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                omni_date = persistence_5days_dict['decimal_day']
                
                for d in range(len(omni_date)):
                    if string_time in omni_date[d]:
                        if float(persistence_5days_dict['Persistence_5days'][d]) > 900:
                            persistence_time.append(np.nan)
                            persistence.append(np.nan)
                        else:
                            persistence_time.append(persistence_5days_dict['decimal_day'][d])
                            persistence.append(float(persistence_5days_dict['Persistence_5days'][d]))
            
            else:
                persistence_time.append(np.nan)
                persistence.append(np.nan)
                
            current_time += timedelta(hours=6)
            
        else:   
            current_time += timedelta(hours=1)
            
    return persistence_time, persistence

def Persistence_27days(cr):
    cr_data = CR_df[CR_df['Carrington Rotation Number'] == cr]
    
    start_date = cr_data.iloc[0]['Start Date']
    end_date = cr_data.iloc[0]['End Date']
    #year = start_date.year
    
    # convert to datetime format
    start_date = pd.to_datetime(start_date) # '2013-12-19 06:11'
    end_date = pd.to_datetime(end_date)
    
    current_time = start_date
    persistence_time = []
    persistence = []
    
    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                omni_date = persistence_27days_dict['decimal_day']
                
                for d in range(len(omni_date)):
                    if string_time in omni_date[d]:
                        if float(persistence_27days_dict['Persistence_27days'][d]) > 900:
                            persistence_time.append(np.nan)
                            persistence.append(np.nan)
                        else:
                            persistence_time.append(persistence_27days_dict['decimal_day'][d])
                            persistence.append(float(persistence_27days_dict['Persistence_27days'][d]))
            
            else:
                persistence_time.append(np.nan)
                persistence.append(np.nan)
                
            current_time += timedelta(hours=6)
            
        else:   
            current_time += timedelta(hours=1)
            
    return persistence_time, persistence
