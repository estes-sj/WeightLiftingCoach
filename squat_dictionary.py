import glob
import os

# Find newest file
list_of_files = glob.glob('logs/*.log') # * means all if need specific format then *.csv
print(list_of_files)
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


""" # Delete oldest file
list_of_files = os.listdir('log')
full_path = ["log/{0}".format(x) for x in list_of_files]

if len(list_of_files) == 25:
    oldest_file = min(full_path, key=os.path.getctime)
    os.remove(oldest_file) """