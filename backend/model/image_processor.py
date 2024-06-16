import numpy as np
import time


class ImageProcessor:
    def __init__(self):
        print('ImageProcessor created')
        time.sleep(10)
        print('ImageProcessor Loaded')

    def image_to_label(self, image=None):
        return np.random.randint(1, 3)

