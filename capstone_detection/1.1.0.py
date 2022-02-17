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
	

# Background

# Alignment Function
def align(object, objectCenter):
	coord = object

	# Choose which coordinate to align with
	# if (object == "Tree"):
	# 	coord = TREE_COORD
	# 	command = PIN_ARM
	# elif (object == "Net"):
	# 	coord = NET_COORD
	# 	command = PIN_LAUNCH
	
	# Align with designated coordinates
	# Right of Center
	if (coord > objectCenter + 10):
		ALIGNMENT = 0x1
		ALIGNED = 0
		GPIO.output(PIN_LEFT, GPIO.HIGH)
		GPIO.output(PIN_RIGHT, GPIO.LOW)
		print("Right of Center")
	# Left of Center
	elif (coord < objectCenter - 10):
		ALIGNMENT = 0x2
		ALIGNED = 0
		GPIO.output(PIN_LEFT, GPIO.LOW)
		GPIO.output(PIN_RIGHT, GPIO.HIGH)
		print("Left of Center")
	#Other
	else:
		ALLIGNMENT = 0x0
		ALIGNED = 1
		GPIO.output(PIN_LEFT, GPIO.LOW)
		GPIO.output(PIN_RIGHT, GPIO.LOW)
		GPIO.output(command, GPIO.HIGH)
	

	# Visual Debug
	net.Allignment(ALIGNMENT)


#main
def main():

	# Initialize GPIO
	GPIOsetup()

	# State machine setup
	state = 0x2
	nextState = 0x2
	print(str(state))

	# Alignment Flags
	LOADED = 1
	ALIGNED = 0
	DETECT_TREE = 0
	DETECT_NET = 0
	RESPONSE = 0

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

		state = nextState

		# State machine states
		# Look for tree
		if (state == IDLE_TREE):
			print("Idle tree")
			# When tree is detected begin aligning
			if (DETECT_TREE == 1):
				state = ALIGN_TREE
		# Align with tree
		elif (state == ALIGN_TREE):
			print("Align tree")
			# Once beads loaded begin looking for the net
			if (LOADED == 1):
				nextState = IDLE_NET
		# Look for net
		elif (state == IDLE_NET):
			print("Idle net")
			# When net is detected begin aligning
			if (DETECT_NET == 1):
				nextState = ALIGN_NET
		# Align with net
		elif (state == ALIGN_NET):
			print("Align net")
			# When beads are no longer loaded (fired) begin looking for tree
			if (LOADED == 0):
				nextState = IDLE_TREE


		# State machine implementation
		# Find Tree
		if (state == IDLE_TREE):
			ALIGNED = 0
			# interact with detections on cam 0
			for detection in detections_0:
				# print(detection)
				class_name = net.GetClassDesc(detection.ClassID)
				print(class_name + " Detected!")
				
				# Check if tree
				if (class_name == "Tree"):
					DETECT_TREE = 1
					DETECT_NET = 0
					break

		# Align with tree
		elif (state == ALIGN_TREE):
			# interact with detections on cam 0
			for detection in detections_0:
				# print(detection)
				class_name = net.GetClassDesc(detection.ClassID)
				print(class_name + " Detected!")
				#getWidth(detection)
				#getHeight(detection)
				center = getCenter(detection)

				# Check if tree
				if (class_name == "Tree"):
					# Align
					while(ALIGNED != 1):
						imgCenter = getImgCenter(display_0)
						align(int(imgCenter[0]), int(center[0]))

					# Check response
					if (RESPONSE == 1):
						LOADED = 1
						break

			ALIGNMENT = 0x0


		# Find net
		elif (state == IDLE_NET):
			ALIGNED =0
			# interact with detections on cam 0
			for detection in detections_0:
				# print(detection)
				class_name = net.GetClassDesc(detection.ClassID)
				print(class_name + " Detected!")
				
				# Check if net
				if (class_name == "Net"):
					print(class_name)
					DETECT_TREE = 0
					DETECT_NET = 1
					break

		# Align with net
		elif (state == ALIGN_NET):
			# interact with detections on cam 0
			for detection in detections_0:
				# print(detection)
				class_name = net.GetClassDesc(detection.ClassID)
				print(class_name + " Detected!")
				#getWidth(detection)
				#getHeight(detection)
				center = getCenter(detection)

				while(ALIGNED != 1):
					# Check if net
					if (class_name == "Net"):
						# Align
						imgCenter = getImgCenter(display_0)
						align(int(imgCenter[0]), int(center[0]))

					# Check response
					if (RESPONSE == 1):
						LOADED = 0
						break

			ALIGNMENT = 0x0
		

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

