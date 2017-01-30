import os
import cv2
import numpy as np
from glob import glob
import time
from config import config
import click


@click.command()
@click.option('-c', '--config', 'conf_path',
              help='Path to the config file',
              type=click.Path(exists=True))
def calibrate(conf_path):
    config.read(conf_path)

    calib_img_paths = sorted(glob(os.path.join(config.get('calibration').get('frames_path'),
        config.get('calibration').get('template'))))

    if config.get('calibration').get('results').get('save'):
        if not os.path.exists(config.get('calibration').get('results').get('path')):
            os.makedirs(config.get('calibration').get('results').get('path'))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        config.get('calibration').get('criteria').get('corners_max_it'),
        config.get('calibration').get('criteria').get('corners_eps'))

    PATTERN = tuple(config.get('calibration').get('pattern'))
    objp = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
    objp[:, : 2] = np.mgrid[0 : PATTERN[0], 0 : PATTERN[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = []
     
    IMG_SIZE = None
    for i_f, calib_f in enumerate(calib_img_paths, start=1):
        print '[{}] [INFO] Processing frame \'{}\'..'.format(time.strftime("%H:%M:%S"),
                                                           os.path.basename(calib_f))
        break_flag = False
        for el in config.get('calibration').get('excluded'):
            if str(el) in os.path.basename(calib_f):
                print '[{}] [INFO]     Frame is in excluded list. Ignoring.'.format(time.strftime("%H:%M:%S"))
                break_flag = True
                break
                
        if break_flag:
            continue

        img = cv2.imread(calib_f)
        if IMG_SIZE is None:
            IMG_SIZE = img.shape[:2][::-1]
        else:
            if img.shape[:2][::-1] != IMG_SIZE:
                print '[{}] [WARNING] Image shape is inconsistent!'.format(time.strftime("%H:%M:%S"))
            
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, PATTERN, None)
        
        if ret == True:
            objpoints.append(objp)
            
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
            
            if config.get('calibration').get('results').get('save'):
                cv2.drawChessboardCorners(img, PATTERN, corners, True)
                cv2.imwrite(os.path.join(config.get('calibration').get('results').get('path'),
                                         os.path.basename(calib_f)), img)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        config.get('calibration').get('criteria').get('cam_mtx_max_it'),
        config.get('calibration').get('criteria').get('cam_mtx_eps'))

    print '[{}] [INFO] Calculating camera matrix..'.format(time.strftime("%H:%M:%S"))
    _, camera_mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, IMG_SIZE, None, None,
        None, None, 0, criteria)

    err_sum = 0.0
    for i in xrange(len(objpoints)):
        imgpts, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], camera_mtx, dist)
        err_sum += cv2.norm(imgpoints[i], imgpts, cv2.NORM_L2) / len(imgpts)
    print '[{}] [INFO]     Re-projection error: {}'.format(time.strftime("%H:%M:%S"), err_sum / len(objpoints))

    print '[{}] [INFO] Calculating new camera matrix..'.format(time.strftime("%H:%M:%S"))
    camera_mtx_new, _ = cv2.getOptimalNewCameraMatrix(camera_mtx, dist, IMG_SIZE, 0.8, IMG_SIZE, centerPrincipalPoint=True)

    res = {
        'cmtx': camera_mtx,
        'cmtx_new': camera_mtx_new,
        'dist': dist
    }

    np.save(os.path.join('calibrations', config.get('calibration').get('out_name')), res)

    print '[{}] [INFO] Calibration done. Resluts saved in \'calibrations/{}.npy\''.format(time.strftime("%H:%M:%S"),
                                                                                          config.get('calibration').get('out_name'))

if __name__ == "__main__":
    calibrate()
