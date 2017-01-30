import sys
import os
from scipy.misc import *
import time
import numpy as np

sys.path.insert(0, os.path.join(os.environ['CAFFE_ROOT'], 'python'))
import caffe

GENDER_GROUPS = ['female', 'male']

class predictor(object):

    def __init__(self, config):
        if config.get('app').get('mode') == 'gpu':
            caffe.set_mode_gpu()
        self.net = caffe.Net(config.get('app').get('gender').get('model_decl'),
            config.get('app').get('gender').get('model_weights'),
            caffe.TEST)
        self.size = config.get('app').get('Rother').get('size')
        self.margin = config.get('app').get('Rother').get('margin')
        self.means = config.get('app').get('Rother').get('means')

    def predict(self, frame, bbox):
        top, bottom, left, right = bbox
        t = max(top - top * self.margin, 0)
        b = min(bottom + bottom * self.margin, frame.shape[0])
        l = max(left - left * self.margin, 0)
        r = min(right + right * self.margin, frame.shape[1])

        face = frame[t : b, l : r, :].astype(np.float32)
        for c_i in range(3):
            face[:, :, c_i] -= self.means[c_i]
        face = imresize(face, self.size)
        data = np.expand_dims(face.transpose(2, 0, 1), 0)
        start = time.time()
        pred = np.argmax(self.net.forward_all(data=data)['prob'])
        end = time.time()
        return GENDER_GROUPS[pred], end - start