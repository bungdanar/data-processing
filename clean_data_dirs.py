import os
import shutil


dir_list = ['err_data', 'res_data', 'output']

# Delete dirs
for dir in dir_list:
    if os.path.exists(dir):
        shutil.rmtree(dir)

# Recreate dirs
for dir in dir_list:
    os.makedirs(dir)
