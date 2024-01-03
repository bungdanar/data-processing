## Summary

This repository is a collection of scripts for calculating the number of unique errors and average response time from log files in [NodeJs REST Fuzzing](https://github.com/bungdanar/nodejs-rest-fuzzing) 
and [Python REST Fuzzing](https://github.com/bungdanar/python-rest-fuzzing) applications.

## How to run

1.	Install Python version 3.11 or higher.
2.	Clone this repository.
3.	Run command `pip install -r requirements.txt`.
4.	Run command `python clean_data_dirs.py` to create the input directories `err_data`, `aggr_err_data`, and `res_data`.

## How to count the number of unique errors

1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste the `err500.log` and `res-time.log` files into the `err_data` directory. Please note that the file names must still be `err500.log` and `res-time.log`.
3.	Run command `python count_err.py`.

## How to count the number of unique aggregate errors

This script is used to count the number of unique errors from several `err500.log` files. 
For example, you have performed fuzzing using two different tools and want to know the number of unique errors found by the two fuzzing tools.
1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste one or more `err500.log` files into the `aggr_err_data` directory. Please note that there are no special requirements regarding naming the `err500.log` file.
3.	Run command `python count_aggr_err.py`.

## How to calculate the average response time

1.	Run command `python clean_data_dirs.py` again (if necessary) to get clean input directories.
2.	Copy and paste one or more `res-time.log` files into the `res_data` directory. Please note that there are no special requirements regarding naming the `res-time.log` file.
3.	Run command `python count_avg_res.py`.
