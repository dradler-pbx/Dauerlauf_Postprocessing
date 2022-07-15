import pandas as pd
import numpy as np
import os
import csv
import pickle


def update_data(logfile_folder: str, logfile_def: str):

    # read the files in the filepath
    filelist = os.listdir(logfile_folder)
    dataframe_list = []

    # loop through the files in the folder and append them as DataFrames to the list
    for file in filelist:
        filepath = '/'.join([logfile_folder, file])
        data = pd.read_csv(filepath, sep=';')
        dataframe_list.append(data)

    # create a single DataFrame from the list
    data = pd.concat(dataframe_list, axis=0, ignore_index=True)

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
