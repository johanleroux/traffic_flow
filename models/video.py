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

    def fetchFrameWidth(self):
        return self.videoCapture.get(3)

    def fetchFrameHeight(self):
        return self.videoCapture.get(4)

    def fetchVideoFps(self):
        return self.videoCapture.get(5)

    def releaseCapture(self):
        self.videoCapture.release()

    def drawFrame(self, objects, fps):
        cv2.putText(self.frame, "{: .2f}fps".format(fps.fps()), (0, 25),
            cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 1, cv2.LINE_AA)

        if objects is None or len(objects) == 0:
            return

        for obj in objects:
            cv2.rectangle(self.frame, (obj.startX(), obj.startY()),
                          (obj.endX(), obj.endY()), (0, 0, 255), 2)

            cv2.circle(self.frame, (obj.x, obj.y), 3, (0, 0, 255), -1)

            cv2.putText(self.frame, "[{0}] {1}".format(obj.id, obj.name), (obj.startX() + 2, obj.startY() + 20),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.putText(self.frame, "{0:.0%}".format(obj.score), (obj.startX() + 2, obj.startY() + 40),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 1, cv2.LINE_AA)
