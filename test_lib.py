import lib

logfile_path = r'logfiles'
logfile_def = 'logfile_definition.csv'

data = lib.update_data(logfile_folder=logfile_path, logfile_def=logfile_def)
header = lib.read_logfile_header_def(logfile_def)
