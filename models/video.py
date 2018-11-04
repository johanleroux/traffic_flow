import os
import time

import imutils
from dotenv import load_dotenv

import cv2
import models.debug as Debug


class Video:
    def __init__(self):
        Debug.info('Loading video capture device')
        self.objects = []
        self.videoCapture = None
        self.frame = None
        self.videoCapture = cv2.VideoCapture(os.getenv("TEST_DATA"))
        self.videoCapture.set(cv2.CAP_PROP_FPS, 10)
        time.sleep(1.0)

    def fetchFrame(self):
        r, self.frame = self.videoCapture.read()
        if r:
            return self.frame
        return None
    
    def fetchRoiFrame(self):
        return self.frame[int(os.getenv("TEST_ROI_Y1")):int(os.getenv("TEST_ROI_Y2")), int(os.getenv("TEST_ROI_X1")):int(os.getenv("TEST_ROI_X2"))]

    def fetchFrameWidth(self):
        return self.videoCapture.get(3)

    def fetchFrameHeight(self):
        return self.videoCapture.get(4)

    def fetchVideoFps(self):
        return self.videoCapture.get(5)

    def releaseCapture(self):
        self.videoCapture.release()
    
    def fullFrameX(self, point):
        return int(os.getenv("TEST_ROI_X1")) + point

    def fullFrameY(self, point):
        return int(os.getenv("TEST_ROI_Y1")) + point

    def drawFrame(self, objectTracker, fps, frameCount):
        cv2.putText(self.frame, "{:.2f}fps".format(fps.fps()), (0, 15),
            cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 0), 1, cv2.LINE_AA)
        
        cv2.putText(self.frame, "Detected {}".format(objectTracker.ids), (0, 35),
            cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 0), 1, cv2.LINE_AA)

        cv2.putText(self.frame, "{}".format(frameCount), (0, 55),
            cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 0), 1, cv2.LINE_AA)

        # ROI Region
        cv2.rectangle(
            self.frame, 
            (int(os.getenv("TEST_ROI_X1")), int(os.getenv("TEST_ROI_Y1"))),
            (int(os.getenv("TEST_ROI_X2")), int(os.getenv("TEST_ROI_Y2"))),
            (0, 255, 0), 
            1
        )

        if objectTracker.getVisibleObjects() is None or len(objectTracker.getVisibleObjects()) == 0:
            return

        for obj in objectTracker.getVisibleObjects():
            cv2.rectangle(
                self.frame, 
                (self.fullFrameX(obj.startX()), self.fullFrameY(obj.startY())),
                (self.fullFrameX(obj.endX()), self.fullFrameY(obj.endY())),
                (0, 0, 255),
                2
            )

            cv2.circle(
                self.frame, 
                (self.fullFrameX(obj.x), self.fullFrameY(obj.y)),
                3, 
                (0, 0, 255),
                -1
            )

            cv2.putText(
                self.frame, 
                "[{0}]".format(obj.id), 
                (self.fullFrameX(obj.startX() + 2), self.fullFrameY(obj.startY() + 20)),
                cv2.FONT_HERSHEY_PLAIN, 
                1.5, 
                (0, 0, 0), 
                1, 
                cv2.LINE_AA
            )
