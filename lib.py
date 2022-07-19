import pandas as pd
import os
import csv
import pickle
import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt


def update_data(logfile_folder: str, logfile_def: str, compression_factor: int):

    # read the files in the filepath
    filelist = sorted(os.listdir(logfile_folder))
    dataframe_list = []

    # loop through the files in the folder and append them as DataFrames to the list
    for file in tqdm(filelist):
        filepath = '/'.join([logfile_folder, file])
        data = pd.read_csv(filepath, sep=';')
        dataframe_list.append(data)

    # create a single DataFrame from the list
    data = pd.concat(dataframe_list, axis=0, ignore_index=True)

    # only take every n entry
    data = data.iloc[::compression_factor, :]

    # exchange the header with clear name header
    data.columns = exchange_header(file_header=data.columns, logfile_def=logfile_def)

    # convert timestamp to datetime
    data['timestamp_UNIXms'] = pd.to_datetime(data['timestamp_UNIXms'], unit='ms')

    # replace 'T' and 'F' with True and False
    data.replace({'T': True, 'F': False}, inplace=True)

    # aggregate by 10 values in mean
    # data = data.groupby(np.arange(len(data)//10).mean())

    return data


def exchange_header(file_header, logfile_def):
    # read the clear name header as a dictionary
    header_dict = read_logfile_header_def(logfile_def)
    new_header = []

    # loop through the file header and create a new header list
    for h in file_header:
        new_header.append(header_dict[h])
    return new_header


def read_logfile_header_def(logfile_def: str):
    with open(logfile_def, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header_dict = {rows[0]: rows[1] for rows in reader}
    return header_dict


def data_to_pickle(data: dict, filename: str):
    with open(filename, 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
    return True


def read_data_from_pickle(filename: str):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data


def run_short_analysis(data: dict, pressure_bounds: dict, target_runtime: float):
    resultlist = []
    for dev in data:
        resultlist.append(_calc_compressor_runtime(data[dev], pressure_bounds[dev], target_runtime))

    df = pd.DataFrame(resultlist)
    df.index = data.keys()
    df = df.transpose()
    print(df)
    _plot_discharge_temp(data)


def _calc_compressor_runtime(data, pressure_bounds: dict, target_runtime: float):
    result_dict = {}

    # calulate new column with timedelta
    data['timedelta'] = data['timestamp_UNIXms'].diff()

    # get the first and last timestamp
    first_timestamp = data['timestamp_UNIXms'].iloc[0]
    result_dict['first timestamp'] = first_timestamp
    last_timestamp = data['timestamp_UNIXms'].iloc[-1]
    result_dict['last_timestamp'] = last_timestamp

    # get data, where the compressor is running
    data = data[data['cpr_CAN_speed'] > 500]

    # exclude data with timestamp difference of more than 1s (e.g. non-consecutive logifles)
    data = data[data['timedelta'] <= datetime.timedelta(seconds=1)]

    # get total runtime
    total_runtime = data['timedelta'].sum()
    result_dict['total_runtime_hours'] = total_runtime.total_seconds()/3600

    # exclude data, where the extended pressure bounds are not met
    # low pressure
    data = data[data['cpr_p_i_r'] > pressure_bounds['lp'][0]-0.1]
    data = data[data['cpr_p_i_r'] < pressure_bounds['lp'][1]+0.1]
    # high pressure
    data = data[data['cond_p_o_r'] > pressure_bounds['hp'][0]-0.3]
    data = data[data['cond_p_o_r'] < pressure_bounds['hp'][1]+0.3]
    runtime_extended_bounds = data['timedelta'].sum()
    result_dict['runtime_within_extended_bounds_hours'] = runtime_extended_bounds.total_seconds()/3600

    # exclude data, where the pressure bounds are not met
    # low pressure
    data = data[data['cpr_p_i_r'] > pressure_bounds['lp'][0]]
    data = data[data['cpr_p_i_r'] < pressure_bounds['lp'][1]]
    # high pressure
    data = data[data['cond_p_o_r'] > pressure_bounds['hp'][0]]
    data = data[data['cond_p_o_r'] < pressure_bounds['hp'][1]]

    # get runtime within bounds
    runtime_bounds = data['timedelta'].sum()
    result_dict['runtime_within_bounds_hours'] = runtime_bounds.total_seconds()/3600

    # get runtime within extended bounds
    result_dict['runtime_share_in_extended_bounds'] = runtime_extended_bounds/total_runtime
    result_dict['runtime_share_in_bounds'] = runtime_bounds/total_runtime

    # calculate remaining runtime
    target_runtime_delta = datetime.timedelta(hours=target_runtime)
    remaining_runtime_delta = target_runtime_delta - runtime_bounds
    target_timestamp = last_timestamp + remaining_runtime_delta

    result_dict['Reaching {} hours'.format(target_runtime)] = target_timestamp

    return result_dict


def _plot_discharge_temp(data):
    for dev in data:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        df = data[dev]
        df = df[df['cpr_T_o_r'] < 1300]

        ax1.plot(df['timestamp_UNIXms'], df['cpr_T_o_r'])
        ax1.set_ylabel('discharge temperature')
        ax1.set_title(dev)
        ax2.plot(df['timestamp_UNIXms'], df['cpr_CAN_speed'])
        ax2.set_ylabel('CPR speed')
        plt.show()


def export_csv(data, compression_factor: int):
    for dev in data:
        df = data[dev]
        df = df.iloc[::compression_factor, :]
        df.to_csv(dev + '.csv')
