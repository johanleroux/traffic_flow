from pprint import pprint

import models.debug as Debug
from models.object import Object


class Tracker:
    def __init__(self):
        self.objects = []
        self.detectedObjects = []
        self.ids = 0
        self.trackableFrames = 10
        self.changes = False

    def getVisibleObjects(self):
        return list(filter(lambda x: x.hiddenFrames == 0, self.objects))

    def getHiddenObjects(self):
        return list(filter(lambda x: x.hiddenFrames > 0, self.objects))

    def getObjects(self):
        return self.objects

    def getPeopleObjects(self):
        return list(
            filter(lambda x: x.name == 'person', self.getVisibleObjects()))

    def getObjectsOfName(self, objectName):
        return list(filter(lambda x: x.name == objectName, self.objects))

    def addObject(self, object):
        detectedObject = Object()
        detectedObject.id = self.ids
        detectedObject.name = object.name
        detectedObject.score = object.score
        detectedObject.x = object.x
        detectedObject.y = object.y
        detectedObject.w = object.w
        detectedObject.h = object.h
        detectedObject.hiddenFrames = 0
        self.objects.append(detectedObject)
        self.ids += 1

    def updateObject(self, uniqueId, updateObject):
        for _index, val in enumerate(self.getObjects()):
            if val.id == uniqueId:
                for _i, detectedObject in enumerate(self.detectedObjects):
                    if detectedObject.id == updateObject:
                        val.score = detectedObject.score
                        val.x = detectedObject.x
                        val.y = detectedObject.y
                        val.w = detectedObject.w
                        val.h = detectedObject.h
                        val.hiddenFrames = 0
                return

    def delObject(self, uniqueId):
        for index, val in enumerate(self.getObjects()):
            if val.id == uniqueId:
                del self.objects[index]
                return

    def track(self, frameObjects):
        self.changes = False
        self.detectedObjects = frameObjects

        # increase the hiddenFrames of all existing objects
        for _i, obj in enumerate(self.getObjects()):
            obj.hiddenFrames += 1

        # stop if no objects have been detected
        if len(self.detectedObjects) == 0:
            return self

        # if not currently tracking any objects
        # initialize everything detected
        if len(self.getObjects()) == 0:
            for _index, val in enumerate(self.detectedObjects):
                self.addObject(val)
            return self

        # set temp ids to objects currently detected
        for _index, val in enumerate(self.detectedObjects):
            val.id = "tmp" + str(_index)

        # calculate distances between new objects detected
        # and older objects currently in the system
        # distance calculation done per object type
        distances = {}
        for _index, detectedObject in enumerate(self.detectedObjects):
            if detectedObject.name not in distances:
                distances[detectedObject.name] = {}

            distances[detectedObject.name][detectedObject.id] = {}

            for _index2, systemObject in enumerate(self.getObjects()):
                if (detectedObject.name == systemObject.name):
                    distances[detectedObject.name][detectedObject.id][
                        systemObject.id] = detectedObject.distanceTo(
                            systemObject)

        # make a list of all detected objects not yet
        # assigned to system objects
        assignedObjects = []

        # loop through the distances calculated and
        # assign the objects to closest related
        for category, items in distances.items():
            # if closest not defined
            closestFrom = ["undefined"] * len(self.getObjectsOfName(category))
            closestTo = ["undefined"] * len(self.getObjectsOfName(category))
            closestDist = [999999999.99] * len(self.getObjectsOfName(category))

            for index, distances in items.items():
                # if object assigned skip
                if index in assignedObjects: continue

                i = 0
                for index2, dist in distances.items():
                    if dist < closestDist[i]:
                        closestFrom[i] = index
                        closestTo[i] = index2
                        closestDist[i] = dist
                    i += 1

            for index, val in enumerate(self.detectedObjects):
                closestIndex = -1
                for index, key in enumerate(closestFrom):
                    if val.id == key and closestDist[index] <= 999999999.99:
                        if closestIndex == -1:
                            closestIndex = index
                        elif closestDist[index] < closestDist[closestIndex]:
                            closestIndex = index

                if closestIndex != -1 and closestDist[closestIndex] < 30:
                    self.updateObject(closestTo[closestIndex],
                                      closestFrom[closestIndex])
                    assignedObjects.append(closestFrom[closestIndex])

        # assign objects not yet assigned
        for _index, val in enumerate(self.detectedObjects):
            if val.id not in assignedObjects:
                self.changes = True
                self.addObject(val)

        # remove objects to old
        for _i, obj in enumerate(self.getObjects()):
            if obj.hiddenFrames > self.trackableFrames:
                self.delObject(obj.id)

        return self

    def debug(self):
        if self.getVisibleObjects() is not None and len(self.getVisibleObjects()) > 0:
            Debug.info('==================================')
            Debug.info('Visible objects detected:')
            for obj in self.getVisibleObjects():
                Debug.info('   [{0}] {1} - {2:.0%} |[{3},{4}]'.format(
                    obj.id, obj.name, obj.score, obj.w, obj.h))
            
            Debug.info('==================================')
        else:
            Debug.info('Nothing detected in the frame')

