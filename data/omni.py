"""
Preprocessing of the OMNI data for comparison with the SWspeed data.

"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# file path
omni_file_path = "E:/research/SW_Speed_Models_Comparison/data/omni_data/omni2_data.txt"
CR_file_path = "E:/research/SW_Speed_Models_Comparison/data/Carrington_Rotation_Data__Oct-Dec__2010-2020_.csv"

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

# Filtering over the period of October-December for the years 2012-2020
df = df[(df['Datetime'].dt.month >= 10) & (df['Datetime'].dt.month <= 12)]
df = df[(df['Datetime'].dt.year >= 2012) & (df['Datetime'].dt.year <= 2020)]

# Resampling to 6 hours
df_resampled = df[df['Datetime'].dt.hour.isin([0, 6, 12, 18])].copy()

# Convert to string format
df_resampled.loc[:, 'Datetime_str'] = df_resampled['Datetime'].dt.strftime('%Y-%m-%d %H:%M')

# Convert to dictionary format
omni_dict = {
    'decimal_day': df_resampled['Datetime_str'].tolist(),
    'sw_speed': df_resampled['Plasma_Speed'].tolist()
}


CR_df = pd.read_csv(CR_file_path)

def OMNI(cr):
    cr_data = CR_df[CR_df['Carrington Rotation Number'] == cr]
    
    start_date = cr_data.iloc[0]['Start Date']
    end_date = cr_data.iloc[0]['End Date']
    #year = start_date.year
    
    # convert to datetime format
    start_date = pd.to_datetime(start_date) # '2013-12-19 06:11'
    end_date = pd.to_datetime(end_date)
    
    current_time = start_date
    omni_time = []
    omni = []
    
    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                omni_date = omni_dict['decimal_day']
                
                for d in range(len(omni_date)):
                    if string_time in omni_date[d]:
                        if float(omni_dict['sw_speed'][d]) > 900:
                            omni_time.append(np.nan)
                            omni.append(np.nan)
                        else:
                            omni_time.append(omni_dict['decimal_day'][d])
                            omni.append(float(omni_dict['sw_speed'][d]))
            
            else:
                omni_time.append(np.nan)
                omni.append(np.nan)
                
            current_time += timedelta(hours=6)
            
        else:   
            current_time += timedelta(hours=1)
            
    return omni_time, omni