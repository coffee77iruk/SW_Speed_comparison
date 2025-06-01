"""
Preprocessing of the WSA-ENLIL data for comparison with the SWspeed data.

"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict


# file path
enlil_file_path = "E:/research/SW_Speed_Models_Comparison/data/wsa_enlil_data/"
CR_file_path = "E:/research/SW_Speed_Models_Comparison/data/Carrington_Rotation_Data__Oct-Dec__2010-2020_.csv"
CR_df = pd.read_csv(CR_file_path)

def WSA_Enlil1(cr):
    """
    Preprocessing of the WSA-ENLIL data before the validation period for the years 2012-2020
    e.g., [2101, 2115, 2128, 2141, 2155, 2168, 2182, 2195, 2208, 2222, 2235]

    """

    CR_df['Start Date'] = pd.to_datetime(CR_df['Start Date'])
    CR_df['End Date'] = pd.to_datetime(CR_df['End Date'])

    # Period of given Carrington Rotation
    rotation_period = CR_df[CR_df['Carrington Rotation Number'] == cr]
    start_date = pd.to_datetime(rotation_period.iloc[0]['Start Date'])
    end_date = pd.to_datetime(rotation_period.iloc[0]['End Date'])

    os.chdir(enlil_file_path)
    CR_list = os.listdir()

    # find the file name that contains the Carrington Rotation number
    index = None
    for i in range(len(CR_list)):
        if str(cr) in CR_list[i]:
            index = i
            break

    # load the WSA-ENLIL data
    enlil = np.loadtxt(CR_list[index])
    enlil_deltaday = enlil[:, 0]
    enlil_speed = enlil[:, 15]

    df = pd.read_table(CR_list[index])
    start_date_str = str(df.loc[3])[76:93]
    year = int(start_date_str[:4])
    month = int(start_date_str[5:7])
    day = int(start_date_str[8:10])
    hour = int(start_date_str[12:14])
    minute = int(start_date_str[15:17])
    enlil_start_date = datetime(year, month, day, hour, minute)

    # calculate the WSA-ENLIL date
    enlil_date = []
    for d in enlil_deltaday:
        new_date = enlil_start_date + timedelta(days=d)
        enlil_date.append(new_date)

    time_dict = defaultdict(list)

    for dt in range(len(enlil_date)):
        time_key = enlil_date[dt].replace(minute=0, second=0, microsecond=0)
        time_dict[time_key].append(enlil_date[dt])
        time_dict[time_key].append(enlil_speed[dt])

    unique_dates = []
    unique_speeds = []
    for time_key, data in time_dict.items():
        unique_dates.append(data[0])
        unique_speeds.append(data[1])

    # create a dictionary for the WSA-ENLIL data
    wsa_dict = {}
    wsa_date = []
    wsa_speed = []
    for d in range(len(unique_dates)):
        condition = unique_dates[d].hour == 0 or unique_dates[d].hour == 6 or unique_dates[d].hour == 12 or unique_dates[d].hour == 18
        if condition:
            wsa_date.append(unique_dates[d])
            wsa_speed.append(unique_speeds[d])

    wsa_dict['decimal_day'] = np.array(wsa_date)
    wsa_dict['sw_speed'] = np.array(wsa_speed)

    current_time = start_date
    step = timedelta(hours=1)  # check every hour

    # acceptable time difference
    time_tolerance = timedelta(hours=1)

    # list to store results
    results = {'date': [], 'speed': []}

    while current_time <= end_date:
        # only process the data for 00, 06, 12, 18 hours
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                match_found = False
                for i in range(len(wsa_dict['decimal_day'])):
                    # get the difference in time between wsa_dict['decimal_day'] and current_time
                    time_diff = abs(wsa_dict['decimal_day'][i] - current_time)
                
                    # if time_diff is less than time_tolerance, save the data
                    if time_diff <= time_tolerance:
                        day = str(wsa_dict['decimal_day'][i])
                        results['date'].append(day[:19])
                        results['speed'].append(float(wsa_dict['sw_speed'][i]))
                        match_found = True
                        break

                if not match_found:
                    # if no data are available for that time, save np.nan
                    results['date'].append(np.nan)
                    results['speed'].append(np.nan)
            else:
                results['date'].append(np.nan)
                results['speed'].append(np.nan)

        # if the current time is not in the list, increase by 1 hour
        current_time += step

    return results['date'], results['speed']


def WSA_Enlil2(cr):
    """
    Preprocessing of the WSA-ENLIL data to consider the 3-day propagation delay
    (Jian et al. 2015)
    
    """
    
    # period of given Carrington Rotation
    rotation_period1 = CR_df[CR_df['Carrington Rotation Number'] == (cr - 1)]
    rotation_period2 = CR_df[CR_df['Carrington Rotation Number'] == cr]
    start_date = pd.to_datetime(rotation_period2.iloc[0]['Start Date'])
    start_date1 = pd.to_datetime(rotation_period1.iloc[0]['End Date'])
    start_date2 = pd.to_datetime(rotation_period2.iloc[0]['Start Date']) + timedelta(days=3)
    end_date1 = pd.to_datetime(rotation_period1.iloc[0]['End Date']) + timedelta(days=3)
    end_date2 = pd.to_datetime(rotation_period2.iloc[0]['End Date'])

    os.chdir(enlil_file_path)
    CR_list = os.listdir()
    CR_list.sort()

    # find the file name that contains the Carrington Rotation number
    index1, index2 = None, None
    for i in range(len(CR_list)):
        if str(cr) in CR_list[i]:
            index1, index2 = i - 1, i
            break

    # load the WSA-ENLIL data
    enlil1 = np.loadtxt(CR_list[index1])
    enlil2 = np.loadtxt(CR_list[index2])
    enlil1_deltaday = enlil1[:, 0]
    enlil1_speed = enlil1[:, 15]
    enlil2_deltaday = enlil2[:, 0]
    enlil2_speed = enlil2[:, 15]

    df1 = pd.read_table(CR_list[index1])
    start_date1_str = str(df1.loc[3])[76:93]
    year1 = int(start_date1_str[:4])
    month1 = int(start_date1_str[5:7])
    day1 = int(start_date1_str[8:10])
    hour1 = int(start_date1_str[12:14])
    minute1 = int(start_date1_str[15:17])
    enlil_start1_date = datetime(year1, month1, day1, hour1, minute1)

    df2 = pd.read_table(CR_list[index2])
    start_date2_str = str(df2.loc[3])[76:93]
    year2 = int(start_date2_str[:4])
    month2 = int(start_date2_str[5:7])
    day2 = int(start_date2_str[8:10])
    hour2 = int(start_date2_str[12:14])
    minute2 = int(start_date2_str[15:17])
    enlil_start2_date = datetime(year2, month2, day2, hour2, minute2)

    # calculate the WSA-ENLIL date
    enlil1_date = []
    for d in enlil1_deltaday:
        new_date = enlil_start1_date + timedelta(days=d)
        enlil1_date.append(new_date)

    enlil2_date = []
    for d in enlil2_deltaday:
        new_date = enlil_start2_date + timedelta(days=d)
        enlil2_date.append(new_date)

    time1_dict = defaultdict(list)
    time2_dict = defaultdict(list)

    for dt in range(len(enlil1_date)):
        time_key = enlil1_date[dt].replace(minute=0, second=0, microsecond=0)
        time1_dict[time_key].append(enlil1_date[dt])
        time1_dict[time_key].append(enlil1_speed[dt])
    for dt in range(len(enlil2_date)):
        time_key = enlil2_date[dt].replace(minute=0, second=0, microsecond=0)
        time2_dict[time_key].append(enlil2_date[dt])
        time2_dict[time_key].append(enlil2_speed[dt])

    unique_dates1, unique_speeds1 = [], []
    for time_key, data in time1_dict.items():
        unique_dates1.append(data[0])
        unique_speeds1.append(data[1])
    unique_dates2, unique_speeds2 = [], []
    for time_key, data in time2_dict.items():
        unique_dates2.append(data[0])
        unique_speeds2.append(data[1])

    # create a dictionary for the WSA-ENLIL data
    wsa_dict1 = {}
    wsa_date1, wsa_speed1 = [], []
    for d in range(len(unique_dates1)):
        condition1 = unique_dates1[d].hour == 0 or unique_dates1[d].hour == 6 or unique_dates1[d].hour == 12 or unique_dates1[d].hour == 18
        condition2 = unique_dates1[d] >= start_date1 and unique_dates1[d] <= end_date1
        if condition1 and condition2:
            wsa_date1.append(unique_dates1[d])
            wsa_speed1.append(unique_speeds1[d])

    wsa_dict1['decimal_day'] = np.array(wsa_date1)
    wsa_dict1['sw_speed'] = np.array(wsa_speed1)

    wsa_dict2 = {}
    wsa_date2, wsa_speed2 = [], []
    for d in range(len(unique_dates2)):
        condition1 = unique_dates2[d].hour == 0 or unique_dates2[d].hour == 6 or unique_dates2[d].hour == 12 or unique_dates2[d].hour == 18
        condition2 = unique_dates2[d] >= start_date2 and unique_dates2[d] <= end_date2
        if condition1 and condition2:
            wsa_date2.append(unique_dates2[d])
            wsa_speed2.append(unique_speeds2[d])

    wsa_dict2['decimal_day'] = np.array(wsa_date2)
    wsa_dict2['sw_speed'] = np.array(wsa_speed2)

    # combine the two dictionaries
    combined_decimal_day = np.concatenate([wsa_dict1['decimal_day'], wsa_dict2['decimal_day']])
    combined_sw_speed = np.concatenate([wsa_dict1['sw_speed'], wsa_dict2['sw_speed']])

    # create a new dictionary with the combined data 
    wsa_dict = {
        'decimal_day': combined_decimal_day,
        'sw_speed': combined_sw_speed
    }

    current_time = start_date
    step = timedelta(hours=1)  # check every hour

    # acceptable time difference
    time_tolerance = timedelta(hours=1)

    # list to store results
    results = {'date': [], 'speed': []}

    while current_time <= end_date2:
        # only process the data for 00, 06, 12, 18 hours
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                match_found = False
                for i in range(len(wsa_dict['decimal_day'])):
                    # get the difference in time between wsa_dict['decimal_day'] and current_time
                    time_diff = abs(wsa_dict['decimal_day'][i] - current_time)
                
                    # if time_diff is less than time_tolerance, save the data
                    if time_diff <= time_tolerance:
                        day = str(wsa_dict['decimal_day'][i])
                        results['date'].append(day[:19])
                        results['speed'].append(float(wsa_dict['sw_speed'][i]))
                        match_found = True
                        break

                if not match_found:
                    # if no data are available for that time, save np.nan
                    results['date'].append(np.nan)
                    results['speed'].append(np.nan)
            else:
                results['date'].append(np.nan)
                results['speed'].append(np.nan)

        # if the current time is not in the list, increase by 1 hour
        current_time += step

    return results['date'], results['speed']

def WSA_ENLIL(cr):
    if cr in [2101, 2115, 2128, 2141, 2155, 2168, 2182, 2195, 2208, 2222, 2235]:
        return WSA_Enlil1(cr)
    else:
        return WSA_Enlil2(cr)
    