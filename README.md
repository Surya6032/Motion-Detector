# Motion-Detector

Detects transient motion in a video feed. If said motion is large enough, and recent enough, reports that there is motion!

The motion detected state is then held for some user specified amount of time even when no motion is detected until finally the program declares that no motion is detected.

# Dependencies
- OpenCV 2
- Image Utilities (imutils)
- Pandas

# Working Theory
OpenCV is used to calculate absolute frame deltas against the most recent saved frame and the current frame. The frame deltas are then passed through a threshold filter, and bounding boxes are drawn around contours of the thresholded frame. (The frequency of saving frames is determined via the user parameter.)

A sufficiently large bounding box derived from the contours of a thresholded frame delta image is considered movement.
