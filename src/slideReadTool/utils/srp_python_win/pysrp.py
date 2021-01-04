import ctypes
import os

#apt install libsqlite3-dev
#apt install libopencv-dev
current_file_path = os.path.abspath(__file__)
os.chdir(os.path.split(current_file_path)[0])

class Srp(object):
    def __init__(self):
        self.__hand = 0.
        dll_path="srp.dll"
        # print(dll_path)
        self.__dll = ctypes.cdll.LoadLibrary(dll_path)
        self.__dll.OpenRW.argtypes = [ctypes.c_char_p]
        self.__dll.OpenRW.restype = ctypes.c_ulonglong
        self.__dll.Close.argtypes = [ctypes.c_ulonglong]
        self.__dll.ReadRegionRGB.argtypes = [ctypes.c_ulonglong,  #
                                       ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,  #
                                       ctypes.c_int32, ctypes.c_int32,  #
                                       ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]
        self.__dll.ReadParamInt32.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]
        self.__dll.ReadParamInt64.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64)]
        self.__dll.ReadParamFloat.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_float)]
        self.__dll.ReadParamDouble.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double)]
        self.__dll.WriteParamDouble.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_double]
        self.__dll.WriteOneAnno.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
        self.__dll.CleanAnno.argtypes = [ctypes.c_ulonglong]

    def say_hello(self):
        self.__dll.hello()

    def open(self, path):
        pStr = ctypes.c_char_p()
        pStr.value = bytes(path, 'utf-8')
        self.__hand = self.__dll.OpenRW(pStr)
        pass

    def close(self):
        if self.__hand != 0:
            self.__dll.Close(self.__hand)
            self.__hand = 0.

    def getAttrs(self):
        pwKey = ctypes.c_char_p()
        pwKey.value = bytes("width", 'utf-8')
        pw = ctypes.c_int32(0)
        b0 = self.__dll.ReadParamInt32(self.__hand, pwKey, ctypes.byref(pw))
        phKey = ctypes.c_char_p()
        phKey.value = bytes("height", 'utf-8')
        ph = ctypes.c_int32(0)
        b1 = self.__dll.ReadParamInt32(self.__hand, phKey, ctypes.byref(ph))
        pzKey = ctypes.c_char_p()
        pzKey.value = bytes("level", 'utf-8')
        plevel = ctypes.c_int32(0)
        b2 = self.__dll.ReadParamInt32(self.__hand, pzKey, ctypes.byref(plevel))
        ppKey = ctypes.c_char_p()
        ppKey.value = bytes("mpp", 'utf-8')
        pmpp = ctypes.c_double(0)
        b3 = self.__dll.ReadParamDouble(self.__hand, ppKey, ctypes.byref(pmpp))
        if b0 and b1 and b2 and b3:
            attrs = {"mpp": pmpp.value,  #
                     "level": plevel.value,  #
                     "width": pw.value,  #
                     "height": ph.value  #
                    }
            return attrs
        else:
            return {}
    
    def getLevelDimention(self, level):
        pwKey = ctypes.c_char_p()#level_widths[4]
        pwKey.value = bytes("level_widths["+str(level)+"]", 'utf-8')
        pw = ctypes.c_int32(0)
        b0 = self.__dll.ReadParamInt32(self.__hand, pwKey, ctypes.byref(pw))
        phKey = ctypes.c_char_p()
        phKey.value = bytes("level_heights["+str(level)+"]", 'utf-8')
        ph = ctypes.c_int32(0)
        b1 = self.__dll.ReadParamInt32(self.__hand, phKey, ctypes.byref(ph))
        
        if b0 and b1:
            attrs = {"width": pw.value,  #
                     "height": ph.value  #
                    }
            return attrs
        else:
            return {}

    def ReadRegionRGB(self, level, x, y, width, height):
        buf_len = width*height*3
        plen = ctypes.c_int32(buf_len)
        img = ctypes.create_string_buffer(buf_len)
        ret = self.__dll.ReadRegionRGB(self.__hand, level, x, y, width, height, img, ctypes.byref(plen))
        if ret != 0:
            return img
        else:
            return None

    def WriteScore(self, score):
        keyStr = ctypes.c_char_p()
        keyStr.value = bytes("score", 'utf-8')
        return self.__dll.WriteParamDouble(self.__hand, keyStr, score)
    
    def ReadScore(self):
        keyStr = ctypes.c_char_p()
        keyStr.value = bytes("score", 'utf-8')
        pscore = ctypes.c_double(0)
        self.__dll.ReadParamDouble(self.__hand, keyStr, ctypes.byref(pscore))
        return pscore.value
    
#    def ReadMannuAnnoNum(self):
#        mlen=ctypes.c_int16(1)
#        self.__dll.ReadManualAnnoCount(self.__hand, ctypes.byref(mlen))
#        return mlen.value
    
                    
    def WriteAnno(self, x, y, score):
        return self.__dll.WriteOneAnno(self.__hand, x, y, 0, score);
    
    def WriteManualAnno(self, num, ntype, x, y, w, h, score):   

        return self.__dll.WriteManualAnno(self.__hand, num, 0, x, y, score)

    def CleanAnno(self):
        return self.__dll.CleanAnno(self.__hand);



