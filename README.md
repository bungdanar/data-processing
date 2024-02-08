## Summary

This repository is a collection of scripts for calculating the number of unique errors and average response time from log files in [NodeJs REST Fuzzing](https://github.com/bungdanar/nodejs-rest-fuzzing) 
and [Python REST Fuzzing](https://github.com/bungdanar/python-rest-fuzzing) applications.

## How to run

1.	Install Python version 3.11 or higher.
2.	Clone this repository.
3.	Run command `pip install -r requirements.txt`.
4.	Run command `python clean_data_dirs.py` to create the input directories `err_data` and `res_data`.

## How to count the number of unique errors for each fuzzing tool

1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste one or more `err500.log` files into the `err_data` directory.
3.	Run command `python count_err_per_fuzz_tool.py`.
4.	It will show the number of unique errors for each file log.

## How to count the number of unique aggregate errors for each validation library

This script is used to count the number of unique errors from several `err500.log` files. 
For example, you have performed fuzzing using two different tools and want to know the number of unique errors found by the two fuzzing tools.
1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste one or more `err500.log` files into the `err_data` directory.
3.	Run command `python count_err_per_val_lib.py`.

## How to calculate the average response time for each validation library

1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste one or more `res-time.log` files into the `res_data` directory.
3.	Run command `python count_res_per_val_lib.py`.

## How to count the number of total requests and endpoint coverage for each fuzzing tool

1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste one or more `res-time.log` files into the `res_data` directory.
3.	Run command `python count_req_per_fuzz_tool.py`.
4.	It will show the number of total requests and endpoint coverage for each file log.
