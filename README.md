# People Counter with OpenCv and Python

![](output_test_01.gif)

![](output_people.gif)

![](output_cars.gif)
Application:
1. in and out of a store
1. view of a security camera

Object Detection vs tracking:
1. Detection
   - where in a image/frame an object is
   - computationally expensive
   - slower
   - algs: Haar cascades, HOG + Linear SVM, Faster R-CNNs, YOLO, Single Shot Detector (SSD)
1. Tracking
   - accept x, y cooridates where an object is
   - assigns unique ID
   - predicts the objects location based on gradient/optical flow
   - algs: MedianFlow, MOSSE, GOTURN, kernalized correlation filters, discriminative correlation filters, etc.

Accurate trackers will combine both detection and tracking.   

OpenCV object tracking algorithms: https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/

Phases:
1. Detect (every N frames)
   - Detect objects
   - Detect new objects
   - Find "lost" objects
1. Track (until the Nth frame)
   - Track objects
   
Project Structure
```angular2html
.
├── Pipfile                         # required packages for code
├── README.md                       # you are here
├── main.ipynb                      # main jupyter notebook code
├── main.py                         # main python code
├── mobilenet_ssd                   # Caffe deep learning model
├── output                          # output generated from the model
├── requirements.txt                # required packages for code
├── submodules                      # helper scripts
│   ├── __init__.py
│   ├── centroidtracker.py    # track an objects center
│   └── trackableobject.py    # detect an object
└── videos                          # input videos if not using web cam
```

# References
1. https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/
1. https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/