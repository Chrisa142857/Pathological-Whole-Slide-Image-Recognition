import openslide
from .utils.sdpc_python import sdpc
from .utils.srp_python_win import pysrp
import numpy as np
import cv2

class slideCroper:


    def __init__(self, path, level=0):
        self.path = path
        self.level = level

    def open(self):
        
        tail = self.path[self.path.rfind('.'):]

        if tail == '.mrxs' or tail == '.svs':
            self.slide = openslide.OpenSlide(self.path)

        elif tail == '.sdpc':
            self.slide = sdpc.Sdpc()
            self.slide.open(self.path)

        elif tail == '.srp':
            self.slide = pysrp.Srp()
            self.slide.open(self.path)
        else:
            print('Type Error')
            exit()


    def crop(self, x, y, w, h):

        tail = self.path[self.path.rfind('.'):]

        if tail == '.mrxs' or tail == '.svs':
            region = np.array(self.slide.read_region((int(x), int(y)), self.level, (int(w), int(h))))
            region = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
        elif tail == '.sdpc':
            region = np.ctypeslib.as_array(self.slide.getTile(self.level, int(y), int(x), int(w), int(h))).reshape((int(h), int(w), 3))
            region.dtype = np.uint8
        elif tail == '.srp':
            region = np.ctypeslib.as_array(self.slide.ReadRegionRGB(self.level, int(y), int(x), int(w), int(h))).reshape((int(h), int(w), 3))
            region.dtype = np.uint8
        else:
            print(tail, 'Type Error')
            exit()
        return region
    
    def close(self):
        
        tail = self.path[self.path.rfind('.'):]
        if tail == '.sdpc':
            self.slide.close()
        elif tail == '.srp':
            self.slide.close()
