# WebCam Motion Detector 


# importing OpenCV, time and Pandas library 
import cv2, time, pandas 
# importing datetime class from datetime library 
from datetime import datetime 

# Assigning our static_back to None 
static_back = None

# List when any moving object appear 
motion_list = [ None, None ] 

# Time of movement 
time = [] 

# Initializing DataFrame, one column is start 
# time and other column is end time 
df = pandas.DataFrame(columns = ["Start", "End"]) 

# Creating a VideoCapture object to record video using webcam
video = cv2.VideoCapture(0) 

# Infinite while loop to treat stack of image as video 
while True: 
	# Reading frame(image) from video 
	check, frame = video.read() 

	# Initializing motion = 0(no motion) 
	motion = 0

	# Converting color image to gray_scale image 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

	gray = cv2.GaussianBlur(gray, (21, 21), 0)     #Converting gray scale frame to GaussianBlur

	if static_back is None: 
		static_back = gray                         #this is used to store the first frame of the video
		continue
	diff_frame = cv2.absdiff(static_back, gray)    #Calculate the difference between the first frame and other frames

	# If change in between static background and 
	# current frame is greater than 30 it will show white color(255) 
	thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 

	#Defines the contour area. Basically, add the borders.
	(_, cnts, _) = cv2.findContours(thresh_frame.copy(), 
					cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    #Removes noises and shadows. Basically, it will keep only that part white which has area greater than 10000 pixels
	for contour in cnts: 
		if cv2.contourArea(contour) < 10000: 
			continue
		motion = 1
		#Creates a green rectangular box
		(x, y, w, h) = cv2.boundingRect(contour) 
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 

	# List of status for every frame
	motion_list.append(motion) 

	motion_list = motion_list[-2:] 

	# Record datetime when change occurs
	if motion_list[-1] == 1 and motion_list[-2] == 0: 
		time.append(datetime.now()) 

	# Record datetime when change occurs
	if motion_list[-1] == 0 and motion_list[-2] == 1: 
		time.append(datetime.now()) 

	# Displaying image in different formats
	cv2.imshow("Gray Frame", gray) 
	cv2.imshow("Difference Frame", diff_frame) 
	cv2.imshow("Threshold Frame", thresh_frame)
	cv2.imshow("Color Frame", frame) 

	key = cv2.waitKey(1) 
	# q will end the program
	if key == ord('q'): 
		if motion == 1: 
			time.append(datetime.now()) 
		break

# Appending time of motion in DataFrame 
for i in range(0, len(time), 2): 
	df=df.append({"Start":time[i],"End":time[i+1]},ignore_index=True)

# Creating a csv file in which time of movements will be saved 
df.to_csv("Time_of_movements.csv") 

video.release() 

# Destroying all the windows 
cv2.destroyAllWindows() 
