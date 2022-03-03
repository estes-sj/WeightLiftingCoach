import glob
import os

# Find newest file
list_of_files = glob.glob('logs/*.log') # * means all if need specific format then *.csv
print(list_of_files)
latest_file = sorted(list_of_files, key=os.path.getmtime) #getmtime/getctime
# Newest log
print(latest_file[-1]) #-1 = newest, 0 = oldest


# Delete oldest file
list_of_files = os.listdir('logs')

if len(list_of_files) == 25:
    oldest_file = min(list_of_files, key=os.path.getctime)
    os.remove(os.path.abspath(oldest_file))