import os
import time

from dotenv import load_dotenv
from imutils.video import FPS

import cv2
from models.haarcascade import Haarcascade
from models.mobilenet import Mobilenet
from models.tracker import Tracker
from models.video import Video

load_dotenv()

def main():
    # Initialize FPS Monitor
    fps = FPS().start()

    # Initalize Video Capture
    video = Video()

    # Object Recognition
    # objectRecognition = Mobilenet()
    objectRecognition = Haarcascade()

    # Initialize Object Tracker
    objectTracker = Tracker()

    # Frame Counter
    frameCount = 1
    frameMod = 1

    # Process Frames
    while True:
        frame = video.fetchFrame()
        if frame is None: continue

        # Only read x amount of frames (performance boost)
        # Detect objects in frame
        if frameCount % frameMod == 0:
            # Detect objects in frame
            recognisedObjects = objectRecognition.detect(video.fetchRoiFrame())
            # cv2.imshow("ROI", video.fetchRoiFrame())

            # Track objects detected
            objectTracker.track(recognisedObjects)

            # Debug Object Tracker Data
            objectTracker.debug()

        # Update Frame Counter
        frameCount += 1
        fps.update()
        fps.stop()

        # Draw Frame
        video.drawFrame(objectTracker, fps, frameCount)
        cv2.imshow("Traffic Flow", frame)

        # input("")

        # Quit (q) shortcut
        c = cv2.waitKey(1)
        if c == ord("q"):
            break

    # Release Capture Device
    video.releaseCapture()
    cv2.destroyAllWindows()


main()
