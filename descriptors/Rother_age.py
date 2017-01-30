import sys
import os
from scipy.misc import *
import time
import numpy as np

sys.path.insert(0, os.path.join(os.environ['CAFFE_ROOT'], 'python'))
import caffe

class predictor(object):

    def __init__(self, config):
        if config.get('app').get('mode') == 'gpu':
            caffe.set_mode_gpu()
        self.net = caffe.Net(config.get('app').get('age').get('model_decl'),
            config.get('app').get('age').get('model_weights'),
            caffe.TEST)
        self.size = config.get('app').get('Rother').get('size')
        self.margin = config.get('app').get('Rother').get('margin')
        self.means = config.get('app').get('Rother').get('means')

    def predict(self, frame, bbox):
        start = time.time()
        top, bottom, left, right = bbox
        t = max(int(top - top * self.margin), 0)
        b = min(int(bottom + bottom * self.margin), frame.shape[0])
        l = max(int(left - left * self.margin), 0)
        r = min(int(right + right * self.margin), frame.shape[1])

        face = frame[t : b, l : r, :].astype(np.float32)
        for c_i in range(3):
            face[:, :, c_i] -= self.means[c_i]
        face = imresize(face, self.size)
        data = np.expand_dims(face.transpose(2, 0, 1), 0)
        pred = np.argmax(self.net.forward_all(data=data)['prob'])
        end = time.time()
        return pred, end - start
