from xml.dom import minidom
import os 
from datetime import datetime
import glob
import xml.etree.ElementTree as ET

  
def new_xml():
    root = minidom.Document()
    
    xml = root.createElement('exercise')
    xml.setAttribute('type', 'squat')
    root.appendChild(xml)
    
    productChild = root.createElement('date')
    xml.appendChild(productChild)
    text = root.createTextNode(str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    productChild.appendChild(text)

    productChild = root.createElement('total_reps')
    xml.appendChild(productChild)
    productChild.appendChild(root.createTextNode("0"))

    productChild = root.createElement('final_score')
    xml.appendChild(productChild)
    productChild.appendChild(root.createTextNode("0"))

    productChild = root.createElement('final_feedback')
    xml.appendChild(productChild)
    productChild.appendChild(root.createTextNode("None"))

    repChild = root.createElement('rep')
    repChild.setAttribute('number', '1')
    xml.appendChild(repChild)

    productChild = root.createElement('knee_angle_top')
    repChild.appendChild(productChild)
    productChild.appendChild(root.createTextNode("0"))

    productChild = root.createElement('knee_angle_mid')
    repChild.appendChild(productChild)
    productChild.appendChild(root.createTextNode("0"))

    productChild = root.createElement('knee_angle_bottom')
    repChild.appendChild(productChild)
    productChild.appendChild(root.createTextNode("0"))

    productChild = root.createElement('back_angle_bottom')
    repChild.appendChild(productChild)
    productChild.appendChild(root.createTextNode("0"))

    productChild = root.createElement('feedback')
    repChild.appendChild(productChild)
    productChild.appendChild(root.createTextNode("None"))

    xml_str = root.toprettyxml(indent ="\t") 
    
    path_pattern = "data/squat_data_%s.xml"
    #save_path_file = next_path(path_pattern) #used for next_path function
    save_path_file = path_pattern % next_file_number()
    print("New File Added: " + save_path_file)
    
    with open(save_path_file, "w") as f:
        f.write(xml_str) 

    print("Oldest File Removed: " + del_oldest_file())
    #print(next_file())

    return save_path_file

# Adds element tags to store next repetition
def add_new_rep():
    tree = ET.parse(newest_file())
    print(newest_file())
    root = tree.getroot()
    print(root[0])
    ET.SubElement(root[0], 'next_rep')
    #Element.set(‘attrname’, ‘value’) – Modifying element attributes. 
    #Element.SubElement(parent, new_childtag) -creates a new child tag under the parent. 

# Returns the next file number in sequence w/o replacements
def next_file_number():
    # Find newest file ID number
    list_of_files = glob.glob('data/*') # * means all if need specific format then *.csv
    #print(list_of_files)
    latest_file = str(max(list_of_files, key=os.path.getmtime)) #getmtime/getctime
    # Returns newest file ID number + 1
    return int(latest_file[16:len(latest_file)-4])+1

def newest_file():
    # Find newest file
    list_of_files = glob.glob('data/*.xml') # * means all if need specific format then *.csv
    # Newest log
    latest_file = max(list_of_files, key=os.path.getmtime) #getmtime/getctime
    print(latest_file) #-1 = newest, 0 = oldest
    return latest_file

def del_oldest_file():
    list_of_files = os.listdir('data')
    full_path = ["data/{0}".format(x) for x in list_of_files]

    if len(list_of_files) > 10:
        oldest_file = min(full_path, key=os.path.getmtime)
        os.remove(oldest_file)
        return oldest_file

"""     list_of_files = os.listdir('videos')
    full_path = ["videos/{0}".format(x) for x in list_of_files]
    if len(list_of_files) > 15:
        oldest_file = min(full_path, key=os.path.getmtime)
        os.remove(oldest_file)
        return oldest_file """

# O(logn) Returns the file path of the next squat with replacements considered
def next_path(path_pattern):
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """
    i = 1

    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2 # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)

    return path_pattern % b

if __name__ == '__main__':
    #new_xml()
    add_new_rep()
