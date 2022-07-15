import pandas as pd
import lib


if __name__ == '__main__':
    logfile_folder_TS1 = r'/logfiles/TS1'
    logfile_folder_TS2 = r'/logfiles/TS2'
    logfile_def = 'logfile_definition.csv'

    user_input = input('Do you want to update the data log? y/[n]')
    if user_input == 'y':
    # TODO: Liste erstellen, die die DataFrames beinhaltet --> leichter zu verarbeiten
        data_TS1 = lib.update_data(logfile_folder_TS1, logfile_def)
        data_TS1.to_pickle('data_TS1.pkl')

        data_TS2 = lib.update_data(logfile_folder_TS2, logfile_def)
        data_TS2.to_pickle('data_TS2.pkl')
        print('Files updated and saved as data_**.pkl')

    else:
        print('Skipping update and reading data**.pkl instead.')
        data_TS1 = pd.read_pickle('data_TS1.pkl')
        data_TS2 = pd.read_pickle('data_TS2.pkl')

