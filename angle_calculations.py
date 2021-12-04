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

def test():
    return 1;

def squat_right_knee_angle(pose, display):
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
    right_upper_leg_slope = abs(calcSlope(right_knee, right_hip))
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