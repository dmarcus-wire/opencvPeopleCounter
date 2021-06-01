# import packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np

# construct centroid class to accept single parameter
# max number of consecutive frames to be lost and removed from tracking
class CentroidTracker:
    def __init__(self, maxDisappeared=50, maxDistance=50):
        # initialize the next uniqueID + 2 ordered dictionaries
        # to keep track of mapping an object ID to its centroid
        # and number of consecutive frames

        # counter used to assign uniqueIDs to each object
        self.nextObjectID = 0
        # dictionary of object and and centroid coordinates
        self.objects = OrderedDict()
        # number of consecutive frames an objectID has been marked as lost for
        self.disappeared = OrderedDict()

        # store the number of maximum consecutive frames
        # an object is allowed to be marked as lost until
        # it is deregistered from tracking
        self.maxDisappeared = maxDisappeared

        # store the maximum distance between centroids
        # if the distance is > max distance, mark object as disappeared
        self.maxDistance = maxDistance

    def register(self, centroid):
        # this method accepts a centroid then adds it to the objects
        # to the dictionary using the next available object ID

        self.objects[self.nextObjectID] = centroid
        # initialize the number oif times an object has disappeared to 0
        self.disappeared[self.nextObjectID] = 0
        # increment the ID so if a new object enters, it gets a new uniqueID
        self.nextObjectID += 1

    def deregsiter(self, objectID):
        # to deregister an objectID, delete it from both
        # objects and disappeared dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]

    # meat and potatoes
    def update(self, rects):
        # update method accepts a list of bounding box rectangles "rects"
        # which is a tuple with (startX, startY, endX, endY) checks if it's empty
        if len(rects) == 0:
            # loop over any existing tracked objects and mark them disappeared
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1

                # if the max number of consecutive frames is reached
                # deregister it
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregsiter(objectID)

            # return as no centroids / data to be updated
            return self.objects

        # initialize a Numpy array of input centroids for the current frame "rect"
        inputCentroids = np.zeros((len(rects), 2), dtype="int")

        # loop over the bounding box rectangles
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            # use the bounding box coordinates to derive centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            # store the centroid in this list
            inputCentroids[i] = (cX, cY)

        # if there are not objects tracked take the input
        # centroids and register each of them
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])

        # otherwise, we are tracking objects and need to match the input centroids
        # to existing object centroids. goal is to track objects and maintain objectIDs
        else:
            # get the objectIDs and corresponding centroid values
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            # compute the distance between each pair of object
            # centroids and input centroids, goal is to match
            # input centroid to existing centroid output a NumPy array of distance D
            D = dist.cdist(np.array(objectCentroids), inputCentroids)

            # (1) find the smallest value in each row (2) sort the row indexes based on min
            rows = D.min(axis=1).argsort()

            # perform a similar process on the columns by finding the smallest
            # value in each column and sorting using the last computed row
            # goal is to have the index values with the smallest corresponding
            # distance at the front of the lists
            cols = D.argmin(axis=1)[rows]

            # determine if update, register, or deregister, need to keep track of which
            # of the rows and column indexes have already been examined
            usedRows = set()
            usedCols = set()

            # loop over the combination of the rows and columns index tuples
            for (row, col) in zip(rows, cols):
                # if already examined, ignore it
                if row in usedRows or col in usedCols:
                    continue

                # if distance between centroids si greater than max distance
                # do not associate two centroids to same object
                if D[row, col] > self.maxDistance:
                    continue

                # otherwise, we found an an input centroid that has
                # (1) smallest Euclidean distance to an existing centroid
                # (2) AND has not been matched to another object
                # grab the object id for current row
                # set its new centroid and reset the disappeared counter
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0

                # indicate we examined each row and col index
                usedRows.add(row)
                usedCols.add(col)

                # compute bot the row and column index that we have not exmined
                # determine which centroid indexes not examined and store in new sets
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)

            # handle object that are lost
            # if the number of object centroids is>= # of input centroids
            # check if the object has been lost
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # grab the objectID for the corresponding row
                    # index and increment the disappeared counter
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1

                    # check if the number of consecutive
                    # frames has been marked disappeared or lost
                    if self.disappeared[objectID] > self.maxDisappeared:
                       self.deregsiter(objectID)

            # loop over the unused cols and regsiter each new centroid
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])
        # return the set of trackable objects
        return self.objects

