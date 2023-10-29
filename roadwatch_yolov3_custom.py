'''
The program recognizes and counts cars on video using YOLOv3
'''

# Run the program from the command line
# cd C:\CRESTL\Programming\PythonCoding\semestr_4\CarCounterYOLOv3
# python car_counter_yolov3.py -y yolo --input videos/10fps.mp4 --output output --skip-frames 5

# import the necessary libraries and functions
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
import numpy as np
import argparse
import imutils
import dlib
import cv2
import os
import json
from matplotlib import pyplot as plt

json_input_file_path = "src\output\output.json"
# json_output_file_path = "src\output\output.json"

# command line argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-y", "--yolo", required = True, type=str,
	help = "path to yolo directory")
ap.add_argument("-i", "--input", required = True, type=str,
	help="path to input video file")
ap.add_argument("-o", "--output", required = True, type=str,
	help="path to output video file")
ap.add_argument("-c", "--confidence", type=float, default=0.01,
	help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip-frames", type=int, default=10,
	help="number of frames to skip between detections"
		 "the higher the number the faster the program works")
args = vars(ap.parse_args())


# classes of objects that can be recognized by the algorithm
with open(args["yolo"] + "/classes.names", 'r') as f:
	CLASSES = [line.strip() for line in f.readlines()]


# Setting yolov3 CUSTOM
print("[INFO] loading model...")
net = cv2.dnn.readNet(args["yolo"] + "/yolov3_608.weights", args["yolo"] + "/yolo-obj.cfg")
print("[INFO] path to weights: ", args["yolo"] + "/yolov3_608.weights")
print("[INFO] path to cfg: ", args["yolo"] + "/yolo-obj.cfg")

'''
# Tuning yolov3 СТОК
print("[INFO] loading model...")
net = cv2.dnn.readNet(args["yolo"] + "/yolov3_608.weights", args["yolo"] + "/yolov3_608.cfg")
print("[INFO] path to weights: ", args["yolo"] + "/yolov3_608.weights")
print("[INFO] path to cfg: ", args["yolo"] + "/yolov3_608.cfg")
'''
layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
output_layers = net.getUnconnectedOutLayersNames()
# Dimensions of the input image
inpWidth = 608
inpHeight = 608

# path to source video
print("[INFO] input directory: ", args["input"])

# read video from disk
print("[INFO] opening video file...")
vs = cv2.VideoCapture(args["input"])

# read clip length from source video
####################################
fps = int(vs.get(cv2.CAP_PROP_FPS))
total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate video duration in seconds
duration_seconds = total_frames / fps

# Convert duration to hours, minutes, and seconds
minutes, seconds = divmod(duration_seconds, 60)
hours, minutes = divmod(minutes, 60)

vid_hrs = hours
vid_mins = minutes
vid_secs = seconds
print(f"Video Duration: {int(hours)}:{int(minutes)}:{int(seconds)}")


# declare a tool for recording the final video to a file, specify the path
writer = None
i = 1
while True:
	if "{}_proccesed.avi".format(i) not in os.listdir(args["output"]):
		writer_path = args["output"] + "/{}_proccesed.avi".format(i)
		break
	else:
		i += 1
print("[INFO] output directory: ", writer_path)

# initialize frame sizes as empty values
# they will be reassigned when analyzing the first frame and only
# this will speed up the programwidth = None
height = None
width = None

# initialize the tracking algorithm
# maxDisappeared = number of frames for which an object can disappear from the video and then again
# will be recognized
# maxDistance = maximum distance between the centers of circles inscribed in car boxes
# If the distance is less than the specified one, then the ID is reassigned

ct = CentroidTracker()
ct.maxDisappeared = 10

# the list of trackers itself
trackers = []
# list of objects to track
trackableObjects = {}



# total number of frames in video
totalFrames = 0

# car counter and temporary variable
total = 0
temp = None

# status: recognition or tracking
status = None

#video frame number
frame_number = 0
count_sedan = 0
count_universal = 0
count_hatchback = 0
count_SUV = 0
count_minivan = 0

# go through each frame of the video
while True:
	frame_number += 1
	frame = vs.read()
	frame = frame[1]


# if frame is empty, the end of the video has been reached
	if frame is None:
		print("=============================================")
		print("The end of the video reached")
		print("Total number of cars on the video is ", total)
		print("Total number of sedan, ", count_sedan)
		print("Total number of universal, ", count_universal)
		print("Total number of hatchback,", count_hatchback)
		print("Total number of SUV, ", count_SUV)
		print("Total number of minivan, ", count_minivan)
		print("=============================================")
		break

	# change the frame size to speed up work
	frame = imutils.resize(frame, width=800)

	# for the dlib library to work, you need to change the colors to RGB instead of BGR
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# frame dimensions
	if width is None or height is None:
		height, width, channels = frame.shape

# this list of boxes can be filled in two ways:
# (1) object detector
# (2) overlay tracker from dlib library
	rects = []

# set the recording path for the final video
	if  writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(writer_path,fourcc, 30,
			(width, height), True)


# every N frames (specified in the "skip_frames" argument) cars are DETECTED
# after this comes TRACKING their boxes
# this increases the speed of the program
	if totalFrames % args["skip_frames"] == 0:
		# create an empty list of trackers
		trackers = []
		# list of class numbers (needed for class signature at car boxes
		class_ids = []

		status = "Detecting..."

# get the blob model from the frame and pass it through the network to get boxes of recognized objects
		blob = cv2.dnn.blobFromImage(frame, 0.00392, (inpWidth, inpHeight), (0, 0, 0), True, crop=False)
		net.setInput(blob)
		outs = net.forward(output_layers)

	# analyze the list of boxes
		for out in outs:
			for detection in out:
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]
				# get the IDs of the most “probable” objects
				if confidence > args["confidence"]:
					print(f"CAR FOUND!")
					print(f"class id = {class_id}")
					if class_id == 0:
						count_sedan += 1
					elif class_id == 1:
						count_universal+=1
					elif class_id == 2:
						count_hatchback+=1
					elif class_id == 3:
						count_SUV += 1
					elif class_id == 4:
						count_minivan += 1 

					center_x = int(detection[0] * width)
					center_y = int(detection[1] * height)
					# this is EXACTLY the WIDTH - that is, the distance from the left edge to the right
					w = int(detection[2] * width)
					# this is EXACTLY THE HEIGHT - that is, the distance from the top edge to the bottom
					h = int(detection[3] * height)

					# Boxing coordinates (2 corner points)
					x1 = int(center_x - w / 2)
					y1 = int(center_y - h / 2)
					x2 = x1 + w
					y2 = y1 + h

					# let's take the maximum radius for CentroidTracker proportional to the size of the car
					ct.maxDistance = w

					print(f"x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}")
					# drawing a test box
					cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
					cv2.putText(frame, CLASSES[class_id], (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

					# create a tracker FOR EACH MACHINE
					tracker = dlib.correlation_tracker()
					# create a rectangle from the box (in fact, this is the box)
					rect = dlib.rectangle(x1, y1, x2, y2)
					# tracker starts tracking EACH BOX
					tracker.start_track(rgb, rect)
					# and each tracker is placed in a common array
					trackers.append(tracker)
					class_ids.append(class_id)

# if the frame is not the Nth one, then it is necessary to work with an array of previously generated trackers, and not boxes
	else:
		for tracker, class_id in zip(trackers, class_ids):

			status = "Tracking..."

			'''
			In one frame the car was recognized. The coordinates of her box were obtained. ALL subsequent 5 frames are these coordinates
			do not go to zero, but change thanks to update(). And each of these five frames is placed in rects predicted
			boxing location program!
			'''
			tracker.update(rgb)
			# get the tracker’s position in the list (these are 4 coordinates)
			pos = tracker.get_position()

			# from the tracker we get the coordinates of the box corresponding to it
			x1 = int(pos.left())
			y1 = int(pos.top())
			x2 = int(pos.right())
			y2 = int(pos.bottom())

			# drawing boxing
			cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
			cv2.putText(frame, CLASSES[class_id], (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

		# and these coordinates are placed in the main list of coordinates of the boxes FOR THE FRAME (drawing will be done on it)
			rects.append((x1, y1, x2, y2))

	'''	
	After the detection of the first machine and until the end of the program, rects will never become [].
	The only condition under which len(objects.keys()) becomes equal to 0 is if the maxDisappeared limit expires, that is
	rects will still be a NOT empty array, but the car will disappear from view for too long.
	'''
	print(f"rects = {rects}")
	objects = ct.update(rects)


# car counting algorithm
	length = len(objects.keys())
	print(f"objects length = {length}")
	if length > total:
		print(f"length > total")
		total += length - total
	if temp is not None:
		if (length > temp):
			print("length > temp")
			total += length - temp
	if length < total:
		print(f"length < total")
		temp = length
	print(f"total is {total}")
	print(f"temp is {temp}\n")

# analyze the array of tracked objects
	for (objectID, centroid) in objects.items():
# check if a trackable object exists for a given ID
		to = trackableObjects.get(objectID, None)

		# if it doesn’t exist, then create a new one corresponding to this centroid
		if to is None:
			to = TrackableObject(objectID, centroid)

		# in any case, place the object in the dictionary
		# (1) ID (2) object
		trackableObjects[objectID] = to


		# display the centroid and ID of the object on the frame
		text = "ID {}".format(objectID + 1)
		cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

	info = [
		("Total", total),
		("Status", status)
	]

	# display information about the number of cars at the edge of the frame
	for (i, (k, v)) in enumerate(info):
		text = "{}: {}".format(k, v)
		cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
		cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 255), 1)

	# write the final frame to the specified directory
	if writer is not None:
		writer.write(frame)



	# show the final frame in a separate window
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# to stop working you must press the "q" key
	if key == ord("q"):
		print("[INFO] process finished by user")
		print("Total number of cars on the video is ", total)
		print("Total number of sedan, ", count_sedan)
		print("Total number of universal, ", count_universal)
		print("Total number of hatchback,", count_hatchback)
		print("Total number of SUV, ", count_SUV)
		print("Total number of minivan, ", count_minivan)

		break

	# because all the above is processing one frame, now you need to increase the number of frames
	# and update the counter
	totalFrames += 1


#json print format
data = {
		"total_cars":str(total),
		"count_hatchback" : str(count_hatchback),
		"count_minivan" : str(count_minivan),
		"count_sedan" : str(count_sedan),
		"count_SUV" : str(count_SUV),
		"count_universal": str(count_universal),
		"vid_hrs": str(vid_hrs),
		"vid_mins" : str(vid_mins),
		"vid_secs" : str(vid_secs),
	}


# the graph is displayed on the screen at the end of the program
plt.show()


with open(json_input_file_path, 'r') as json_file:
    existing_data = json.load(json_file)
existing_data.update(data)

with open(json_input_file_path, 'w') as json_file:
    json.dump(existing_data, json_file, indent=4)

# free up memory for the variable
if writer is not None:
	writer.release()

# close all windows
cv2.destroyAllWindows()

