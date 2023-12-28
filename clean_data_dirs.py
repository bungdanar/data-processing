import os
import shutil


dir_list = ['aggr_err_data', 'err_data', 'res_data']

# Delete dirs
for dir in dir_list:
    if os.path.exists(dir):
        shutil.rmtree(dir)

# Recreate dirs
for dir in dir_list:
    os.makedirs(dir)
