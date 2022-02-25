squat_dict = {
  "brand": "",
  "electric": "",
  "year": "",
  "colors": ["red", "white", "blue"]
}

#back_angle_bottom, knee_angle_bottom, back_angle_middle, knee_angle_middle, back_angle_top, knee_angle_top, final score


import glob
import os

# Find newest file
list_of_files = glob.glob('/path/to/folder/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)


# Delete oldest file
list_of_files = os.listdir('log')
full_path = ["log/{0}".format(x) for x in list_of_files]

if len(list_of_files) == 25:
    oldest_file = min(full_path, key=os.path.getctime)
    os.remove(oldest_file)