import pandas as pd
import lib
import os
import time


if __name__ == '__main__':

    # folders and files for initialization
    logfile_folder = r'C:\Users\dominik\Documents\logfiles'
    logfile_def = 'logfile_definition.csv'
    logfile_device_folders = os.listdir(logfile_folder)
    pressure_bounds = {
        'TS1': {'lp': [2.8, 3.2], 'hp': [14.5, 15.5]},
        'TS2': {'lp': [3.7, 4.1], 'hp': [12.5, 13.5]}
    }
    target_runtime = 300

    while True:
        print('-------------------------------------------------------------------------------------')
        print('Data postprocessing Dauerlauf')
        print('The follwoing commands are available:')
        print('analysis:\t\tGet an output of a short analysis for the devices in the data')
        print('update:\t\t\tUpdate the logfiles (e.g. new CSV files added to the logfile folders')
        print('export:\t\t\tExport the data as one CSV per device with clear header')
        print('exit:\t\t\tExit the application.')
        user_input = input('What should I do?')

        if user_input == 'exit':
            break

        if user_input == 'update':
            user_input = input('Found {} devices. Do you want to update them? [y]/n'.format(len(logfile_device_folders)))
            if user_input != 'n':
                compression_factor = input('By which factor shall the data be reduced?')
                data = {}
                # read the files per device and store it in a dictionary
                for device in logfile_device_folders:
                    print('Updating {}...'.format(device))
                    logfile_folder_path = '/'.join([logfile_folder, device])
                    data_dev = lib.update_data(logfile_folder_path, logfile_def, int(compression_factor))
                    data[device] = data_dev

                # save the data dictionary for later use
                save_flag = lib.data_to_pickle(data, 'data.pickle')
                if save_flag:
                    print('Files updated and saved as data.pickle')
            else:
                print('Update cancelled!')

        if user_input == 'analysis':
            # load data if not yet loaded
            if 'data' not in locals():
                # load the data.pickle
                if os.path.exists('data.pickle'):
                    data = lib.read_data_from_pickle('data.pickle')
                else:
                    print('No file data.pickle found. Please update data!')
                    continue
            lib.run_short_analysis(data, pressure_bounds, target_runtime)
            input('\nPress key to continue...')

        if user_input == 'export':
            compression_factor = input('By which factor shall the data be reduced?')
            compression_factor = int(compression_factor)

            # load data if not yet loaded
            if 'data' not in locals():
                # load the data.pickle
                if os.path.exists('data.pickle'):
                    data = lib.read_data_from_pickle('data.pickle')
                else:
                    print('No file data.pickle found. Please update data!')
                    continue

            for dev in data:
                lib.export_csv(data, compression_factor)
            print('CSV files exported.')

        time.sleep(1)
