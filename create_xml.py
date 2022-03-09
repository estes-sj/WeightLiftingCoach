from xml.dom import minidom
import os 
from datetime import datetime
import glob
  
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
def add_new_rep(rep_count):
    file_path = newest_file()
    file = minidom.parse(file_path)
    
    repChild = file.createElement('rep')
    repChild.setAttribute('number', str(rep_count))
    file.firstChild.appendChild(repChild)

    productChild = file.createElement('knee_angle_top')
    repChild.appendChild(productChild)
    productChild.appendChild(file.createTextNode("0"))

    productChild = file.createElement('knee_angle_mid')
    repChild.appendChild(productChild)
    productChild.appendChild(file.createTextNode("0"))

    productChild = file.createElement('knee_angle_bottom')
    repChild.appendChild(productChild)
    productChild.appendChild(file.createTextNode("0"))

    productChild = file.createElement('back_angle_bottom')
    repChild.appendChild(productChild)
    productChild.appendChild(file.createTextNode("0"))

    productChild = file.createElement('feedback')
    repChild.appendChild(productChild)
    productChild.appendChild(file.createTextNode("None"))

    xml_str = file.toprettyxml(indent ="\t") 

    # writing the changes in "file" object to 
    # the "test.xml" file
    with open(file_path, "w" ) as fs: 
  
        fs.write( file.toxml() )
        fs.close() 

def modify_value(save_data_path, element, rep, value):
    file = minidom.parse(save_data_path)
    # modifying the value of a tag(here "age")
    file.getElementsByTagName( element )[ rep-1 ].childNodes[ 0 ].nodeValue = str(value)
    # writing the changes in "file" object to 
    # the save_data_path file
    with open(save_data_path, "w" ) as fs: 
        fs.write( file.toxml() )
        fs.close() 
    return

# Returns the next file number in sequence w/o replacements
def next_file_number():
    # Find newest file ID number
    list_of_files = glob.glob('data/*') # * means all if need specific format then *.csv
    #print(list_of_files)
    latest_file = str(max(list_of_files, key=os.path.getmtime)) #getmtime/getctime
    # Returns newest file ID number + 1
    return int(latest_file[16:len(latest_file)-4])+1

# Find newest data file
def newest_file():
    # Find newest file
    list_of_files = glob.glob('data/*.xml') # * means all if need specific format then *.csv
    # Newest log
    latest_file = max(list_of_files, key=os.path.getmtime) #getmtime/getctime
    print(latest_file) #-1 = newest, 0 = oldest
    return latest_file

def newest_video():
    # Find newest video
    list_of_files = glob.glob('videos/*') # * means all if need specific format then *.csv
    # Newest video
    latest_file = max(list_of_files, key=os.path.getmtime) #getmtime/getctime
    print(latest_file) #-1 = newest, 0 = oldest
    return latest_file

# Returns the 6 most recent data xml files 
def previous_lift_files():
    # Find newest file
    list_of_files = glob.glob('data/*.xml') # * means all if need specific format then *.csv
    latest_file = sorted(list_of_files, key=os.path.getmtime, reverse=True) #getmtime/getctime
    return latest_file[0:7] # 0 = newest because reversed list

def del_oldest_file():
    oldest_data = None
    oldest_video = None

    # Delete oldest XML data
    list_of_data = os.listdir('data')
    full_path = ["data/{0}".format(x) for x in list_of_data]
    if len(list_of_data) > 20:
        oldest_data = min(full_path, key=os.path.getmtime)
        os.remove(oldest_data)

    # Delete oldest video
    list_of_videos = os.listdir('videos')
    full_path = ["videos/{0}".format(x) for x in list_of_videos]
    if len(list_of_videos) > 30:
        oldest_video = min(full_path, key=os.path.getmtime)
        os.remove(oldest_video)

    if oldest_data != None and oldest_video != None:
        oldest_files = [oldest_data, oldest_video]
        return oldest_files
    elif oldest_data != None:
        return oldest_data
    elif oldest_video != None:
        return oldest_video
    else:
        return

# New method to obtain final results as an array
def getFinalResults():
    latest_file = newest_file()
    file = minidom.parse(latest_file)
    final_score = file.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue
    final_feedback = file.getElementsByTagName( "final_feedback" )[ 0 ].childNodes[ 0 ].nodeValue
    final_results = [final_score, final_feedback]
    return final_results


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
    # Testing
    
    #new_xml()
    #add_new_rep(2)
    #add_new_rep(3)
    #add_new_rep(4)
    #add_new_rep(5)
    #modify_value(newest_file(), "knee_angle_top", 4, 9)
    #previous_lift_files()
    getFinalResults()