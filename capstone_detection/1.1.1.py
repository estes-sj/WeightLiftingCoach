#Authors: Samuel Estes and Trevor Weygandt
#Resources: https://rawgit.com/dusty-nv/jetson-inference/dev/docs/html/python/jetson.inference.html#detectNet

from ctypes import alignment
import threading
import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys

import numpy as np
import Jetson.GPIO as GPIO

sudoPassword = 'Rah2022'
command = 'xrandr --output HDMI-0 --mode 1920x1080'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
command = 'sudo systemctl restart nvargus-daemon'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

#
# object detection setup
#IDs(Cup = 1, Net = 2, Beads = 3, Pole = 4, Marshmallow = 5)
#
net = jetson.inference.detectNet(argv=['--model=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/ssd-mobilenet.onnx', 
'--labels=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/labels.txt', '--input-blob=input_0', '--output-cvg=scores', 
'--output-bbox=boxes']) # custom training model

# Pin Definitions
# Outputs
PIN_LEFT = 17		# white
PIN_RIGHT = 27		# grey
PIN_LAUNCH = 22		# purple
PIN_ARM = 10		# blue
PIN_CONTROL = 9		# green
# Input
PIN_RESPONSE = 11	# yellow

# Flags
# 0 = Center, 1 = Left of Center, 2 = Right of Center
ALIGNMENT = 0x0

# State Machine
IDLE_TREE = 0x0
ALIGN_TREE = 0x1
IDLE_NET = 0x2
ALIGN_NET = 0x3


# Alignment Coordinates
TREE_COORD = 0
NET_COORD = 0

# Alignment Flags
LOADED = 1
ALIGNED = 0
DETECT_TREE = 0
DETECT_NET = 0
RESPONSE = 0


# Setup GPIO Pins
def GPIOsetup():
	GPIO.setmode(GPIO.BCM)

	# Outputs
	GPIO.setup(PIN_LEFT, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_RIGHT, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_LAUNCH, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_ARM, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_CONTROL, GPIO.OUT, initial=GPIO.LOW)

	# Input
	GPIO.setup(PIN_RESPONSE, GPIO.IN)
	
# Task that runs the computer vision software
def ComputerVision():
	while True:
		try:
			# open streams for camera 0
			camera_0 = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
			display_0 = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
			print(getTime() + "Camera 0 started...\n")
			break
		except:
			p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
			print(getTime() + "Camera 0 failed to start...restarting")
			time.sleep(3)
			print(getTime() + "Done!\n")


	while display_0.IsStreaming(): #and display_1.IsStreaming():
		img_0 = camera_0.Capture()
		detections_0 = net.Detect(img_0)
		display_0.Render(img_0)
		display_0.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

		# print the detections
		print(getTime() + "----------CAMERA 0------------")
		print(getTime() + "detected {:d} objects in image".format(len(detections_0)))

		# Response from Arduino
		RESPONSE = GPIO.input(PIN_RESPONSE)
	pass

# Task that controls robot
def RobotControl():
	while(True):
		print("Moop Gabba Meep")
		time.sleep(1)
	pass

def main():

	# Initialize GPIO
	GPIOsetup()
	
	# Threading setup
	task1 = threading.Thread(target=ComputerVision)
	task2 = threading.Thread(target=RobotControl)

	task1.start()
	task2.start()

	task1.join()
	task2.join()

#
### Misc Functions
# Get Overlay Width
def getWidth(detection):
	width = detection.Right - detection.Left
	print("Width = " + str(width) )
	return width

# Get Overlay Height
def getHeight(detection):
	height = detection.Bottom - detection.Top
	print("Height = " + str(height)) 
	return height

# Get Overlay Center
def getCenter(detection):
	center = [(detection.Right - detection.Left)/2, (detection.Bottom - detection.Top/2)]
	print("Center = (" + str(center[0]) + ", " + str(center[1]) + ")")
	return center

# Get Image Center
def getImgCenter(display_0):
	width = display_0.GetWidth()
	height = display_0.GetHeight()
	imgCenter = [width/2, height/2]
	print("Image Center = (" + str(imgCenter[0]) + ", " + str(imgCenter[1]) + ")" )
	return imgCenter

# Get Coordinates of Center of Box
def boxCoord(detection):
	width = getWidth(detection)
	left = detection.Left
	coord_x = left + width/2
	return coord_x

def getTime():
	# Get current date and time
	dt = datetime.datetime.now()
	# Format datetime string
	x = dt.strftime("[%Y-%m-%d %H:%M:%S]	")
	return str(x)


# Run main
if __name__ == '__main__':
	main()

