# Face Extraction And Description
This simple app aims to extract faces from the stream (live camera stream or existing video file or even the bunch of frames etc.) and shows you all possible information about the person accordingly to his facial features.

Currently supports *age* and *gender* recognition.

# Requirements
* [Ubuntu](https://www.ubuntu.com/) (tested 16.04)
* [Python](https://www.python.org/) 2.x (tested 2.7.12)
* [OpenCV](http://opencv.org/) 2.4.x (tested 2.4.12.3, manual build)
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
1. Camera calibration
    * fill the section *calibration* in the your config file (see `configs/config.yml.example` for possible parameters) with the appropriate values
    * run 

        `./calibrate.sh PATH_TO_CONFIG`

    Calibrations will be saved in the `calibrations` subfolder with name specified in the config.

2. Downloading pre-trained models.

    Currently this solution supports two models both for *age* and *gender* recognition from two different papers:

    * *Age and Gender Classification using Convolutional Neural Networks*. Gil Levi, Tal Hassner, 2015 [1]

        This model trained on [Adience](http://www.openu.ac.il/home/hassner/Adience/data.html) dataset.

    * *DEX: Deep EXpectation of apparent age from a single image*. Rasmus Rothe, Radu Timofte, Luc Van Gool, 2015 [2]

        This model based on the pre-trained one on ImageNet2014 dataset [3] and then fine-tuned on [IMDB-WIKI](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/). Actually this project uses the model which was additionally fine-tuned on the [LAP challendge](http://gesture.chalearn.org/) dataset.

    This repository already provides network declarations (see `models` subfolder), pre-trained weights can donwloaded via running

    `./download_models.sh`

3. Running the app
    * fill the section *app* in the your config file (see `configs/config.yml.example` for possible parameters) with the appropriate values
    * run 

        `CAFFE_ROOT=/path/to/caffe/ ./run.sh PATH_TO_CONFIG`

    You should see a resizable window with your stream (camera or video file) overlaid by the facial b-boxes and facial descriptions.

# References
1. [Project page](http://www.openu.ac.il/home/hassner/projects/cnn_agegender/)

2. [Project page](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/)

    @article{Rothe-IJCV-2016,

    author = {Rasmus Rothe and Radu Timofte and Luc Van Gool},
  
    title = {Deep expectation of real and apparent age from a single image without facial landmarks},
  
    journal = {International Journal of Computer Vision (IJCV)},
  
    year = {2016},
  
    month = {July},

    }
    
    @InProceedings{Rothe-ICCVW-2015,
    
    author = {Rasmus Rothe and Radu Timofte and Luc Van Gool},
    
    title = {DEX: Deep EXpectation of apparent age from a single image},
    
    booktitle = {IEEE International Conference on Computer Vision Workshops (ICCVW)},
    
    year = {2015},
    
    month = {December},
    
    }

3. [Project page](http://www.robots.ox.ac.uk/~vgg/research/very_deep/)

    *Very  deep  convolutional  networks  for  large-scale  image  recognition*. K.  Simonyan  and  A.  Zisserman, 2014.