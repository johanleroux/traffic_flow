import cv2
from models.object import Object


class Haarcascade:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier('data/cars.xml')
        self.objects = []
        self.frameWidth = 0
        self.frameHeight = 0

    def detect(self, frame):
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        newObjects = self.cascade.detectMultiScale(grayFrame, 1.1, 3)

        # Process the neural network's results
        self.processFrame(newObjects)

        del grayFrame

        return self.objects

    def processFrame(self, newObjects):
        self.objects = []

        for (x, y, w, h) in newObjects:
            if w > 200 or h > 200:
                continue
            if w < 50 or h < 50:
                continue

            detectedObject = Object()
            detectedObject.id = 0

            detectedObject.name = "car"
            detectedObject.score = 0
            detectedObject.x = x + int(w / 2)
            detectedObject.y = y + int(h / 2)
            detectedObject.w = w
            detectedObject.h = h
            detectedObject.hiddenFrames = 0

            self.objects.append(detectedObject)
