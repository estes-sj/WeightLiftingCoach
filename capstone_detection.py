#Authors: Samuel Estes and Trevor Weygandt
#Resources: https://rawgit.com/dusty-nv/jetson-inference/dev/docs/html/python/jetson.inference.html#detectNet

import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys

import numpy as np
import RPi.GPIO as GPIO

sudoPassword = 'Rah2022'
command = 'sudo systemctl restart nvargus-daemon'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

# Pin Definitions
PIN_LEFT = 25
PIN_RIGHT = 9

#
# object detection setup
#IDs(Cup = 1, Net = 2, Beads = 3, Pole = 4, Marshmallow = 5)
#
net = jetson.inference.detectNet(argv=['--model=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/ssd-mobilenet.onnx', 
'--labels=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/labels.txt', '--input-blob=input_0', '--output-cvg=scores', 
'--output-bbox=boxes']) # custom training model

# Flags
# 0 = Center, 1 = Left of Center, 2 = Right of Center
ALLIGNMENT = 0x0




#main
def main():

	# Pin Setups
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN_LEFT, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_RIGHT, GPIO.OUT, initial=GPIO.LOW)

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

		# try:
		# 	# open stream for camera 1
		# 	camera_1 = jetson.utils.videoSource("csi://1")
		# 	display_1 = jetson.utils.videoOutput("display://1")
		# 	print(getTime() + "Camera 1 started...\n")
		# 	break  
		# except:
		# 	p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
		# 	print(getTime() + "Camera 1 failed to start...restarting")
		# 	time.sleep(3)
		# 	print(getTime() + "Done!\n")

	while display_0.IsStreaming(): #and display_1.IsStreaming():
		img_0 = camera_0.Capture()
		detections_0 = net.Detect(img_0)
		display_0.Render(img_0)
		display_0.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

		# print the detections
		print(getTime() + "----------CAMERA 0------------")
		print(getTime() + "detected {:d} objects in image".format(len(detections_0)))

		# interact with detections on cam 0
		for detection in detections_0:
			# print(detection)
			class_name = net.GetClassDesc(detection.ClassID)
			print(class_name + " Detected!")
			#getWidth(detection)
			#getHeight(detection)
			center = getCenter(detection)
			imgCenter = getImgCenter(display_0)
			coord_x = boxCoord(detection)

			# Right of Center
			if (coord_x > imgCenter[0] + 10):
				ALLIGNMENT = 0x1
				GPIO.output(PIN_LEFT, GPIO.HIGH)
				GPIO.output(PIN_RIGHT, GPIO.LOW)
				print("Right of Center")
			# Left of Center
			elif (coord_x < imgCenter[0] - 10):
				ALLIGNMENT = 0x2
				GPIO.output(PIN_LEFT, GPIO.LOW)
				GPIO.output(PIN_RIGHT, GPIO.HIGH)
				print("Left of Center")
			#Other
			else:
				ALLIGNMENT = 0x0
				GPIO.output(PIN_LEFT, GPIO.LOW)
				GPIO.output(PIN_RIGHT, GPIO.LOW)
			
			print("-----------------------------------------")
			net.Allignment(ALLIGNMENT)
			
		#print out performance info
		#detectNet.PrintProfilerTimes()

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

