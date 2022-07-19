import lib
import numpy as np

pressure_bounds = {
    'TS1': {'lp': [2.8, 3.2], 'hp': [14.5, 15.5]},
    'TS2': {'lp': [3.7, 4.1], 'hp': [12.5, 13.5]}
}
target_runtime = 300

logfile_folder = r'test_files/TS1'
df = lib.update_data(logfile_folder, 'logfile_definition.csv', 1)

df['timedelta'] = df['timestamp_UNIXms'].diff()

df_filtered1 = df[df['cpr_CAN_speed'] > 500]
df_filtered2 = df[df['cpr_CAN_speed'].shift(1) > 500]

df_filtered_comb = df[(df['cpr_CAN_speed'] > 500) & (df['cpr_CAN_speed'].shift(-1) > 500)]
