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
import angle_calculations
import numpy as np

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

def main():

    while True:
        try:
			# open streams for camera 0
            #camera = jetson.utils.videoSource("csi://0", argv=["--input-flip=rotate-180"])      # '/dev/video0' for V4L2 
            camera = jetson.utils.videoSource('csi://0', argv=["--input-flip=rotate-180"])      # '/dev/video0' for V4L2 
            #display = jetson.utils.videoOutput('display://0') # 'my_video.mp4' for file
            display = jetson.utils.videoOutput('videos/demo.mp4') # 'my_video.mp4' for file
            print(getTime() + "Camera 0 started...\n")
            break
        except:
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            print(getTime() + "Camera 0 failed to start...restarting")
            time.sleep(3)
            print(getTime() + "Done!\n")

    top_score = 0.0
    while display.IsStreaming(): #and display_1.IsStreaming():
        # capture the next image
        img = camera.Capture()
  
        # perform pose estimation (with overlay)
        poses = net.Process(img, overlay=opt.overlay)

        # print the pose results
        print("detected {:d} objects in image".format(len(poses)))

        for pose in poses:
 #           print(pose)
 #           print(pose.Keypoints)
 #           print('Links', pose.Links)
            
            #pointing(pose, display)
            #angle_calculations.squat_right_knee_angle(pose)
            
            #squat_right_score(pose)

            last_scores = squat_right_score(pose)
            if last_scores != None:
                if last_scores[0] > top_score:
                    top_score = last_scores[0]
                    print("Current Score: {:.3f}%".format(top_score))

        # render the image
        display.Render(img)

        # update the title bar
        display.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

        # print text on screen
        #cv2.putText(img, "I HATE CODING", (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (0, 0, 0), 2, lineType=cv2.LINE_AA)

        # print out performance info
        # poseNet.PrintProfilerTimes()

        # exit on input/output EOS
        if not camera.IsStreaming() or not display.IsStreaming():
            break
    
    # Add try-catch if needed
    print("###############################")
    angle_calculations.squat_scoring(last_scores[1], last_scores[2])
    print("BEST SCORE = {:.3f}%".format(top_score))
    print("###############################") 
# Calculate percent correctness for right-side-view of sqat
def squat_right_score(pose):
    right_knee_angle = angle_calculations.squat_right_knee_angle(pose)
    back_angle = angle_calculations.squat_right_back_angle(pose)
    if (right_knee_angle != None and back_angle != None):
        return angle_calculations.squat_scoring(right_knee_angle, back_angle)
    return

# Calculate percent correctness for left-side-view of sqat
def squat_left_score(pose):
    left_knee_angle = angle_calculations.squat_left_knee_angle(pose)
    back_angle = angle_calculations.squat_left_back_angle(pose)
    return 1

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
  #  test = angle_calculations.test()
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