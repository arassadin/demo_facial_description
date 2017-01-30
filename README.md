# Face Extraction And Description
This simple app aims to extract faces from the stream (live camera stream or existing video file or even the bunch of frames etc.) and shows you all possible information about the person accordingly to his facial features.

Currently supports *age* and *gender* recognition.

# Requirements
* [Ubuntu](https://www.ubuntu.com/) (tested 16.04)
* [Python](https://www.python.org/) 2.x (tested 2.7.12)
* [OpenCV](http://opencv.org/) 2.4.x
* [Caffe](http://caffe.berkeleyvision.org/) with Python bindings
* [Dlib](http://dlib.net/) with Python bindings
* [NumPy](http://www.numpy.org/)
* [SciPy](https://www.scipy.org/)
* [Click](click.pocoo.org/)

# Installation
1. Install OpenCV from the repository (the easiest way) or as described [here](http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html).
2. Build Caffe manually as described [here](http://caffe.berkeleyvision.org/install_apt.html). Don't forget about Python bindings:

    `make pycaffe`

3. Run

    `sudo pip install -U -r requirements.txt`

    from the root of the repository.

# HowTo
