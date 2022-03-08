# Written by Samuel Estes, Zach Farr, Emily Hattman

import cv2
import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys
import math
import angle_calculations
import numpy as np
import create_xml
import atexit

sudoPassword = 'scalp431!'
command = 'xrandr --output HDMI-0 --mode 1920x1080'
#command = 'xrandr --output HDMI-0 --mode 1280x720'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
command = 'sudo systemctl restart nvargus-daemon'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

# python3 pose_image_calculation.py form_pictures/squat6.png form_pictures/squat6_results.png > logs/log_squat6.log
# python3 fancyGui.py > logs/log_demo.log
# parse the command line
parser = argparse.ArgumentParser(description="Run AI weight lifting pose estimation DNN on a video/image stream.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.poseNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="resnet18-body", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="links,keypoints", help="pose overlay flags (e.g. --overlay=links,keypoints)\nvalid combinations are:  'links', 'keypoints', 'boxes', 'none'")
parser.add_argument("--threshold", type=float, default=0.15, help="minimum detection threshold to use") 

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the pose estimation model
net = jetson.inference.poseNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# Flags to keep track of squat position during rep
TOP_SQUAT_FLAG = False
MID_SQUAT_FLAG = False
BOT_SQUAT_FLAG = False
top_knee_angle = 10
mid_knee_angle = 30
bot_knee_angle = 55
# Store data path once created in main()
global save_data_path

# Initialize reps variable and reset each time program is ran
reps = 1

def main():
    global save_data_path
    while True:
        try:
			# open streams for camera 0
            camera = jetson.utils.videoSource('videos/IMG_2826.avi', argv=["--input-width=1280 --input-height=720"])      # '/dev/video0' for V4L2 
            #camera = jetson.utils.videoSource("csi://0", argv=["--input-flip=rotate-180"])      # '/dev/video0' for V4L2 
            #display = jetson.utils.videoOutput('display://0') # 'my_video.mp4' for file
            display = jetson.utils.videoOutput('videos/IMG_2826_RESULTS.mp4', argv=["--output-width=1280 --output-height=720"]) # 'my_video.mp4' for file
            print(getTime() + "Camera 0 started...\n")
            break
        except:
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            print(getTime() + "Camera 0 failed to start...restarting")
            time.sleep(3)
            print(getTime() + "Done!\n")

    # Generate new xml file and save path
    save_data_path = create_xml.new_xml()
    top_score = 0.0
    while display.IsStreaming(): #and display_1.IsStreaming():
        # capture the next image
        img = camera.Capture()
        # perform pose estimation (with overlay)
        poses = net.Process(img, overlay=opt.overlay)
        # print the pose results
        print("detected {:d} objects in image".format(len(poses)))

        for pose in poses:
 
 #           Print captured pose information
 #           print(pose)
 #           print(pose.Keypoints)
 #           print('Links', pose.Links)
            verify_squat(pose)
            last_scores = squat_right_score(pose)
            if last_scores != None:
                if last_scores[0] > top_score:
                    top_score = last_scores[0]
                    final_scores = last_scores
                    print("Current Score: {:.3f}%".format(top_score))

        # render the image
        display.Render(img)

        # update the title bar
        display.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

        # print out performance info
        # poseNet.PrintProfilerTimes()

        # exit on input/output EOS
        if not camera.IsStreaming() or not display.IsStreaming():
            break
    
    # Add try-catch if needed
    print("###############################")
    angle_calculations.squat_scoring(final_scores[1], final_scores[2])
    print("BEST REP SCORE = {:.3f}%".format(top_score))
    print("###############################") 
# Calculate percent correctness for right-side-view of sqat
def squat_right_score(pose):
    right_knee_angle = angle_calculations.squat_right_knee_angle(pose)
    #post knee angle to xml
    back_angle = angle_calculations.squat_right_back_angle(pose)
    #post back angle to xml

    #if bottom of squat, calculate score
    if (right_knee_angle != None and back_angle != None):
        return angle_calculations.squat_scoring(right_knee_angle, back_angle)
    return

def verify_squat(pose):
    if TOP_SQUAT_FLAG == False:
        #if false, check angle against desired and set to true if close
        angle = angle_calculations.squat_right_knee_angle(pose, top_knee_angle)
        angle_difference = angle - top_knee_angle
        # if within +- 5 degrees of desired angle, set to true
        if (angle_difference < 5 and angle_difference > -5):
            TOP_SQUAT_FLAG = True
            # Print Top Squat angle to XML
            create_xml.modify_value(save_data_path, "knee_angle_top", reps, angle)
    # Check for mid-point knee angle
    if (TOP_SQUAT_FLAG == True) and (MID_SQUAT_FLAG == False):
        angle = angle_calculations.squat_right_knee_angle(pose, mid_knee_angle)
        angle_difference = angle - mid_knee_angle
        if (angle_difference < 5 and angle_difference > -5):
            MID_SQUAT_FLAG = True
            # Print Mid Squat angle to XML
            create_xml.modify_value(save_data_path, "knee_angle_mid", reps, angle)
    # Check for bottom point knee angle and score
    if (TOP_SQUAT_FLAG == True) and (MID_SQUAT_FLAG == True) and (BOT_SQUAT_FLAG == False):
        angle = angle_calculations.squat_right_knee_angle(pose, bot_knee_angle)
        angle_difference = angle - bot_knee_angle
        if (angle_difference < 5 and angle_difference > -5):
            BOT_SQUAT_FLAG = True
            # Score the bottom squat position
            squat_right_score(pose)
            # Print Bot Squat angle and score
            create_xml.modify_value(save_data_path, "knee_angle_bot", reps, angle)
    # Check for return to top point, increment rep and continue
    if (TOP_SQUAT_FLAG == True) and (MID_SQUAT_FLAG == True) and (BOT_SQUAT_FLAG == True):
        angle = angle_calculations.squat_right_knee_angle(pose, top_knee_angle)
        angle_difference = angle - mid_knee_angle
        if (angle_difference < 5 and angle_difference > -5):
            MID_SQUAT_FLAG = False
            BOT_SQUAT_FLAG = False
            reps += 1
            # Create Next Rep Data on XML
            create_xml.add_new_rep(reps)
            # Print Top Squat angle to XML

def getTime():
	# Get current date and time
	dt = datetime.datetime.now()
	# Format datetime string
	x = dt.strftime("[%Y-%m-%d %H:%M:%S]	")
	return str(x)

# Exit Handler
def exit_handler():
    # Print final score to XML
    # Print rep number to XML
    print ("Workout Completed!")

# Run main
if __name__ == '__main__':
	main()
# When completed, run exit handler
atexit.register(exit_handler)
 



    # topology_supercategory = "person";
    # topology_id = 1;
    # topology_name = "person";
    # topology_keypoints = {
    #0     "nose",
    #1     "left_eye",
    #2     "right_eye",
    #3     "left_ear",
    #4     "right_ear",
    #5     "left_shoulder",
    #6     "right_shoulder",
    #7     "left_elbow",
    #8     "right_elbow",
    #9     "left_wrist",
    #10     "right_wrist",
    #11     "left_hip",
    #12     "right_hip",
    #13     "left_knee",
    #14     "right_knee",
    #15     "left_ankle",
    #16     "right_ankle",
    #17     "neck"
    # };

    # // original topology
    # topology_skeleton = {
    #     { 16, 14 },
    #     { 14, 12 },
    #     { 17, 15 },
    #     { 15, 13 },
    #     { 12, 13 },
    #     { 6, 8 },
    #     { 7, 9 },
    #     { 8, 10 },
    #     { 9, 11 },
    #     { 2, 3 },
    #     { 1, 2 },
    #     { 1, 3 },
    #     { 2, 4 },
    #     { 3, 5 },
    #     { 4, 6 },
    #     { 5, 7 },
    #     { 18, 1 },
    #     { 18, 6 },
    #     { 18, 7 },
    #     { 18, 12 },
    #     { 18, 13 }
    # };