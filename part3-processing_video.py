import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

option = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshhold': 0.25,
    'gpu': 1.0
}

tfnet = TFNet(option)

capture = cv2.VideoCapture('The_Biggest_Cat_Hug.mp4')
colors = [tuple(255 * np.random.rand(3)) for i in range(5)]

while (capture.isOpened()):
    start_time = time.time()
    ret, frame = capture.read()  # true or false
    results = tfnet.return_predict(frame)
    # if video hasn't ended
    if ret:
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            frame = cv2.rectangle(frame, tl, br, color, 7)
            frame = cv2.putText(
                frame, label, tl, cv2.FONT_HERSHEY_COMPLET, 1, (0, 0, 0), 2)

        cv2.imshow('frame', frame)
        print('FPS {:.1f}'.format(1 / (time.time() - start_time)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if video has ended
        else:
            capture.release()
            cv2.destroyAllWindows()
            break
