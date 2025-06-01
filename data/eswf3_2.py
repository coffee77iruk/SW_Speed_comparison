"""
Preprocessing of the ESWF 3.2 data for comparison with the SWspeed data.

"""

import numpy as np
import pandas as pd


# file path
eswf_file_path = "E:/research/SW_Speed_Models_Comparison/data/eswf_data/eswfv3_2.csv"
CR_file_path = "E:/research/SW_Speed_Models_Comparison/data/Carrington_Rotation_Data__Oct-Dec__2010-2020_.csv"
CR_df = pd.read_csv(CR_file_path)
eswf3_2_df = pd.read_csv(eswf_file_path, parse_dates=[0])

CR_df['Start Date'] = pd.to_datetime(CR_df['Start Date'])
CR_df['End Date'] = pd.to_datetime(CR_df['End Date'])
eswf3_2_df['timestamp'] = pd.to_datetime(eswf3_2_df['timestamp'])

def ESWF3_2(cr):
    # find the start and end date for the given rotation number
    rotation_period = CR_df[CR_df['Carrington Rotation Number'] == cr]
    
    start_date = pd.to_datetime(rotation_period.iloc[0]['Start Date'])
    end_date = pd.to_datetime(rotation_period.iloc[0]['End Date'])
    
    # set the current time
    current_time = start_date
    eswf_time = []
    eswf = []

    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                eswf3_2_time = eswf3_2_df['timestamp']

                Bool = True
                for d in range(len(eswf3_2_time)):
                    if string_time in str(eswf3_2_time[d]):
                        eswf_time.append(eswf3_2_df['timestamp'].iloc[d].strftime('%Y-%m-%d %H:%M:%S'))
                        eswf_speed = eswf3_2_df['v[km/s]'].iloc[d]
                        eswf.append(float(eswf_speed.round(3)))
                        Bool = False
                if Bool:
                    eswf_time.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))
                    eswf.append(np.nan)
            else:
                eswf_time.append(np.nan)
                eswf.append(np.nan)
            
            current_time += pd.Timedelta(hours=6)
        else:
            current_time += pd.Timedelta(hours=1)    
        
    return eswf_time, eswf
