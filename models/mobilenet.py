import imutils
import numpy as np

import cv2
from models.detectable_objects import DETECTABLE_OBJECTS
from models.object import Object


class Mobilenet:
    def __init__(self):
        self.net = cv2.dnn.readNetFromCaffe(
            "data/MobileNetSSD_deploy.prototxt.txt",
            "data/MobileNetSSD_deploy.caffemodel")
        self.objects = []
        self.frameWidth = 0
        self.frameHeight = 0

    def detect(self, frame):
        # Resize frame to reduce size and increase speeds
        (self.h, self.w) = frame.shape[:2]
        mobilenetFrame = cv2.resize(frame, (300, 300))

        # Preprocess a blob that has normalized input through
        # mean subtraction and scaled the image appropriately
        blob = cv2.dnn.blobFromImage(mobilenetFrame, 0.01, (300, 300), 127.5)

        # Set input for the neural network
        # and then process the input
        self.net.setInput(blob)
        newObjects = self.net.forward()

        # Process the neural network's results
        self.processFrame(newObjects)

        del mobilenetFrame

        return self.objects

    def processFrame(self, newObjects):
        self.objects = []

        for i in np.arange(0, newObjects.shape[2]):
            score = newObjects[0, 0, i, 2]
            idx = int(newObjects[0, 0, i, 1])

            if score > 0.5 and DETECTABLE_OBJECTS[idx] == 'car':
                box = newObjects[0, 0, i, 3:7] * np.array(
                    [self.w, self.h, self.w, self.h])
                (startX, startY, endX, endY) = box.astype("int")

                detectedObject = Object()
                detectedObject.id = 0

                detectedObject.name = DETECTABLE_OBJECTS[idx]
                detectedObject.score = score
                detectedObject.x = int((endX + startX) / 2)
                detectedObject.y = int((endY + startY) / 2)
                detectedObject.w = endX - startX
                detectedObject.h = endY - startY
                detectedObject.hiddenFrames = 0

                if detectedObject.w > 200 or detectedObject.h > 200:
                    continue

                self.objects.append(detectedObject)
