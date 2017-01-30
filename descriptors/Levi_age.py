import sys
import os
from scipy.misc import *
import time
import numpy as np

caffe_root = '/home/alexandr/distr/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe
caffe.set_mode_cpu()

AGE_GROUPS = ['0-2', '4-6', '8-13', '15-20', '25-32', '38-43', '48-53', '60+']

class predictor(object):

    def __init__(self, config):
        if config.get('app').get('mode') == 'gpu':
            caffe.set_mode_gpu()
        self.net = caffe.Net(config.get('app').get('age').get('model_decl'),
            config.get('app').get('age').get('model_weights'),
            caffe.TEST)
        blob = caffe.proto.caffe_pb2.BlobProto()
        data = open(config.get('app').get('Levi').get('mean_file') , 'rb').read()
        blob.ParseFromString(data)
        self.means = caffe.io.blobproto_to_array(blob)
        self.size = config.get('app').get('Levi').get('size')

    def predict(self, frame, bbox):
        face = frame[bbox[0] : bbox[1], bbox[2] : bbox[3], :].astype(np.float32)
        face = imresize(face, self.size)
        data = np.expand_dims(face.transpose(2, 0, 1), 0) - self.means
        data = data[:, :, 14:-15, 14:-15]
        start = time.time()
        pred = np.argmax(self.net.forward_all(data=data)['prob'])
        end = time.time()
        return AGE_GROUPS[pred], end - start
