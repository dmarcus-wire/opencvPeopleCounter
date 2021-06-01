# This module tracks an object from a video stream
# and stores data about the object
# - object id
# - previous centroids
# - existing or new object for counting
# The TrackableObject constructor accepts an
# objectID + centroid and stores them.
# The centroids variable is a list because
# it will contain an object’s centroid location history.

class TrackableObject:
    def __init__(self, objectID, centroid):
        # store the object ID
        # initialize list of centroids
        self.objectID = objectID
        self.centroids = [centroid]

        # initialize boolean if object counted = true
        # initializes counted as False,
        # indicating that the object has not been counted yet
        self.counted = False