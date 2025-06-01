"""
Preprocessing of the DL model data for comparison with the SWspeed data.

"""

import numpy as np
import pandas as pd


# file path
dlmodel_data_file_path = "E:/research/SW_Speed_Models_Comparison/data/model_result/model_prediction.npy"
dlmodel_time_file_path = "E:/research/SW_Speed_Models_Comparison/data/model_result/target_time.npy"
CR_file_path = "E:/research/SW_Speed_Models_Comparison/data/Carrington_Rotation_Data__Oct-Dec__2010-2020_.csv"

# read file
model_prediction = np.load(dlmodel_data_file_path)
model_prediction = model_prediction[:, -1] * 1000   # denormalization
model_prediction = model_prediction.astype(float)

model_time = np.load(dlmodel_time_file_path, allow_pickle=True)[:, -1]
model_time = pd.to_datetime(model_time, format='%Y-%m-%d-%H-%M').tz_localize(None)

CR_df = pd.read_csv(CR_file_path)

#CR_df['Start Date'] = pd.to_datetime(CR_df['Start Date'])
#CR_df['End Date'] = pd.to_datetime(CR_df['End Date'])

# Convert to dictionary format
model_dict = {
    'decimal_day': [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in model_time], 
    'sw_speed': list(model_prediction)
}

def DL_Model(cr):
    cr_data = CR_df[CR_df['Carrington Rotation Number'] == cr]

    start_date = cr_data.iloc[0]['Start Date']
    end_date = cr_data.iloc[0]['End Date']

    # convert to datetime format
    start_date = pd.to_datetime(start_date) # '2013-12-19 06:11'
    end_date = pd.to_datetime(end_date)

    current_time = start_date
    model_time = []
    model = []
    
    while current_time <= end_date:
        if current_time.hour in [0, 6, 12, 18]:
            if current_time.month in [10, 11, 12]:
                string_time = str(current_time)[:-6]
                model_date = model_dict['decimal_day']

                Bool = True
                for d in range(len(model_date)):
                    if string_time in str(model_date[d]):
                        model_time.append(model_dict['decimal_day'][d])
                        model.append(float(model_dict['sw_speed'][d]))
                        Bool = False
                if Bool:
                    model_time.append(np.nan)
                    model.append(np.nan)
            else:
                model_time.append(np.nan)
                model.append(np.nan)

            current_time += pd.Timedelta(hours=6)
        else:
            current_time += pd.Timedelta(hours=1)
        
    return model_time, model
