# Written by Samuel Estes, Zach Farr, Emily Hattman

import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys

import numpy as np

sudoPassword = 'scalp431!'
command = 'xandr --output HDMI0 --mode 1280x720'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
command = 'sudo systemctl restart nvargus-daemon'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

poseNet = jetson.inference.poseNet(argv=['--network=resnet18-body', '--input-flip=rotate-180', '--overlay=links,keypoints', '--threshold=0.15']) # custom training model

def main():

    while True:
        try:
			# open streams for camera 0
            camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2 
            display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
            print(getTime() + "Camera 0 started...\n")
            break
        except:
            p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            print(getTime() + "Camera 0 failed to start...restarting")
            time.sleep(3)
            print(getTime() + "Done!\n")

    while display.IsStreaming(): #and display_1.IsStreaming():
        # capture the next image
        img = input.Capture()

        # perform pose estimation (with overlay)
        poses = poseNet.Process(img, overlay=opt.overlay)

        # print the pose results
        print("detected {:d} objects in image".format(len(poses)))

        for pose in poses:
            print(pose)
            print(pose.Keypoints)
            print('Links', pose.Links)
            pointing(pose)

        # render the image
        display.Render(img)

        # update the title bar
        display.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, poseNet.GetNetworkFPS()))

        # print out performance info
       # poseNet.PrintProfilerTimes()

        # exit on input/output EOS
        if not input.IsStreaming() or not display.IsStreaming():
            break

def pointing(pose):
    # find the keypoint index from the list of detected keypoints
    # you can find these keypoint names in the model's JSON file, 
    # or with net.GetKeypointName() / net.GetNumKeypoints()
    left_wrist_idx = pose.FindKeypoint('left_wrist')
    left_shoulder_idx = pose.FindKeypoint('left_shoulder')

    # if the keypoint index is < 0, it means it wasn't found in the image
    if left_wrist_idx < 0 or left_shoulder_idx < 0:
        pass
    
    left_wrist = pose.Keypoints[left_wrist_idx]
    left_shoulder = pose.Keypoints[left_shoulder_idx]

    point_x = left_shoulder.x - left_wrist.x
    point_y = left_shoulder.y - left_wrist.y

    print(f"person {pose.ID} is pointing towards ({point_x}, {point_y})")
    

# Run main
if __name__ == '__main__':
	main()




    topology_supercategory = "person";
    topology_id = 1;
    topology_name = "person";
    topology_keypoints = {
        "nose",
        "left_eye",
        "right_eye",
        "left_ear",
        "right_ear",
        "left_shoulder",
        "right_shoulder",
        "left_elbow",
        "right_elbow",
        "left_wrist",
        "right_wrist",
        "left_hip",
        "right_hip",
        "left_knee",
        "right_knee",
        "left_ankle",
        "right_ankle",
        "neck"
    };

    // original topology
    topology_skeleton = {
        { 16, 14 },
        { 14, 12 },
        { 17, 15 },
        { 15, 13 },
        { 12, 13 },
        { 6, 8 },
        { 7, 9 },
        { 8, 10 },
        { 9, 11 },
        { 2, 3 },
        { 1, 2 },
        { 1, 3 },
        { 2, 4 },
        { 3, 5 },
        { 4, 6 },
        { 5, 7 },
        { 18, 1 },
        { 18, 6 },
        { 18, 7 },
        { 18, 12 },
        { 18, 13 }
    };