# Written by Samuel Estes, Zach Farr, Emily Hattman

import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys
import cv2
import math

import numpy as np

# parse the command line
parser = argparse.ArgumentParser(description="Run AI weight lifting pose estimation DNN on a video/image stream.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.poseNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="csi://0", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="display://0", nargs='?', help="URI of the output stream")
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
#input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

def main():

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

    while True:
        # capture the next image
        img = input.Capture()

        # perform pose estimation (with overlay)
        poses = net.Process(img, overlay=opt.overlay)

        # print the pose results
        print("detected {:d} objects in image".format(len(poses)))

        for pose in poses:
 #           print(pose)
 #           print(pose.Keypoints)
 #           print('Links', pose.Links)
            
            #pointing(pose, display)
            squat_knee_angle(pose)

        # render the image
        output.Render(img)

    # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))


        # print text on screen
        #cv2.putText(img, "I HATE CODING", (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (0, 0, 0), 2, lineType=cv2.LINE_AA)

        # print out performance info
        # poseNet.PrintProfilerTimes()

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break

def pointing(pose, display):
    # find the keypoint index from the list of detected keypoints
    # you can find these keypoint names in the model's JSON file, 
    # or with net.GetKeypointName() / net.GetNumKeypoints()
    print("---------------------") 

    left_wrist_idx = pose.FindKeypoint(9) #9 = left wrist
    left_shoulder_idx = pose.FindKeypoint(5) #5 = left shoulder
    # if the keypoint index is < 0, it means it wasn't found in the image
    if left_wrist_idx < 0 or left_shoulder_idx < 0:
        return
    
    left_wrist = pose.Keypoints[left_wrist_idx]
    left_shoulder = pose.Keypoints[left_shoulder_idx]

    point_x = left_shoulder.x - left_wrist.x
    point_y = left_shoulder.y - left_wrist.y

    print(f"person {pose.ID} is pointing towards ({point_x}, {point_y})")
    display.SetStatus(f"person {pose.ID} is pointing towards ({point_x}, {point_y})")

    #cv2.putText(display, "I HATE CODING", (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (0, 0, 0), 2, lineType=cv2.LINE_AA)

    #Parameters:
    #frame: current running frame of the video.
    #Text: The text string to be inserted.
    #org: bottom-left corner of the text string
    #font: the type of font to be used.
    #color: the colour of the font.
    #thickness: the thickness of the font

    print("---------------------")

def squat_detection(pose, display):
    print("---------------------") 
    left_knee_idx = pose.FindKeypoint(13)
    left_hip_idx = pose.FindKeypoint(11)

    right_knee_idx = pose.FindKeypoint(14)
    right_hip_idx = pose.FindKeypoint(12)

    # if the keypoint index is < 0, it means it wasn't found in the image
    if (left_knee_idx < 0 or left_hip_idx < 0) and (right_knee_idx < 0 or right_hip_idx < 0):
        return
    
    left_knee = pose.Keypoints[left_knee_idx]
    left_hip = pose.Keypoints[left_hip_idx]
    right_knee = pose.Keypoints[right_knee_idx]
    right_hip = pose.Keypoints[right_hip_idx]

    if right_hip.y > right_knee.y or left_hip.y > left_knee.y:
        print(f"BREAK 90!!!!!!!!!")
        display.SetStatus(f"BREAK 90!!!!!!!!!")
    else:
        print(f"GOOD SQUAT :)")
        display.SetStatus(f"GOOD SQUAT :)")
    return;

def squat_knee_angle(pose):
    print("---------------------") 

    # Distance formula = abs sqrt((x2-x1)^2 + (y2-y1)^2)

    # Right upper leg distance
    right_knee_idx = pose.FindKeypoint(14)
    right_hip_idx = pose.FindKeypoint(12)

    if (right_knee_idx < 0 or right_hip_idx < 0):
        return
    
    right_knee = pose.Keypoints[right_knee_idx]
    right_hip = pose.Keypoints[right_hip_idx]

    # right_upper_leg_distance = abs(math.sqrt((right_hip.x - right_knee.x)^2 + (right_hip.y - right_knee.y)^2))
    right_upper_leg_slope = abs((right_hip.y - right_knee.y)/(right_hip.x - right_knee.x))
    print("Right Upper Leg Slope: " + str(right_upper_leg_slope))

    # Right lower leg distance
    right_ankle_idx = pose.FindKeypoint(16)

    if (right_ankle_idx < 0):
        return

    right_ankle = pose.Keypoints[right_ankle_idx]

    # right_lower_leg_distance = abs(math.sqrt((right_ankle.x - right_knee.x)^2 + (right_ankle.y - right_knee.y)^2))
    right_lower_leg_slope = abs((right_ankle.y - right_knee.y)/(right_ankle.x - right_knee.x))
    print("Right Lower Leg Slope: " + str(right_lower_leg_slope))
   
    # Calculate knee angle of right knee 
    right_knee_angle = math.degrees(abs(math.atan((right_upper_leg_slope - right_lower_leg_slope) / (1 + right_upper_leg_slope * right_lower_leg_slope))))
    #if right_knee_angle < 0:
    #    right_knee_angle += 180

    print("Right knee angle = " + str(right_knee_angle))

    # Desired angle is 180-125 = 55 degrees
    print("     Off by " + str(right_knee_angle - (180-125)) + " degrees")

# Calculates the slope of a line based on 2 points
def calcSlope(point1, point2):  # point1 and point2 refers to 2 points in the resnet model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    return (point2.y-point1.y)/(point2.x-point1.x)

# Calculate the distance of a line based on 2 points
def calcDistance(point1, point2):
    return abs(math.sqrt((point1.x-point2.x)^2 + (point1.y-point2.y)^2))

# Calculates the angle in degress of two intersecting lines given the slope
def calcAngle(slope1, slope2): 
    angle = (math.degrees(math.atan((slope1-slope2)/(1 + slope1*slope2))))
    return angle if angle < 0 else angle+180

def getTime():
	# Get current date and time
	dt = datetime.datetime.now()
	# Format datetime string
	x = dt.strftime("[%Y-%m-%d %H:%M:%S]	")
	return str(x)

# Run main
if __name__ == '__main__':
	main()




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