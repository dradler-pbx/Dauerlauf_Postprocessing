import pandas as pd
import lib
import os
import time


if __name__ == '__main__':

    # folders and files for initialization
    logfile_folder = './logfiles'
    logfile_def = 'logfile_definition.csv'
    logfile_device_folders = os.listdir(logfile_folder)

    while True:
        print('-------------------------------------------------------------------------------------')
        print('Data postprocessing Dauerlauf')
        print('The follwoing commands are available:')
        print('analysis:\t\t\tGet an output of a short analysis for the devices in the data')
        print('update:\t\t\t\tUpdate the logfiles (e.g. new CSV files added to the logfile folders')
        print('export:\t\t\tExport the data as one CSV per device with clear header')
        print('exit:\t\t\t\tExit the application.')
        user_input = input('What should I do?')

        if user_input == 'exit':
            break

        if user_input == 'update':
            user_input = input('Found {} devices. Do you want to update them? [y]/n'.format(len(logfile_device_folders)))
            if user_input != 'n':
                data = {}
                # read the files per device and store it in a dictionary
                for device in logfile_device_folders:
                    logfile_folder_path = '/'.join([logfile_folder, device])
                    data_dev = lib.update_data(logfile_folder_path, logfile_def)
                    data[device] = data_dev

                # save the data dictionary for later use
                save_flag = lib.data_to_pickle(data, 'data.pickle')
                if save_flag:
                    print('Files updated and saved as data.pickle')
            else:
                print('Update cancelled!')

        if user_input == 'analysis':
            continue

        if user_input == 'export':
            # load data if not yet loaded
            if 'data' not in locals():
                # load the data.pickle
                if os.path.exists('data.pickle'):
                    data = lib.read_data_from_pickle('data.pickle')
                else:
                    print('No file data.pickle found. Please update data!')
                    continue

            for dev in data:
                df = data[dev]
                df.to_csv(dev+'.csv')
            print('CSV files exported.')

        time.sleep(1)
