try:
    from pyueye import ueye
    from pyueye_example_utils import (uEyeException, Rect, get_bits_per_pixel,
								  ImageBuffer, MemoryInfo, check)

except:
    None

import numpy as np
import cv2



class CameraDummy(object):
    """
    A class for working with cameras in OpenCV.
    """

    def __init__(self, camera_index=0):
        """
        Initialize a CameraDummy object with the specified camera index.

        :param camera_index: Index of the camera to use (default is 0).
        """
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        self._run_flag = True




    def list_connected_cameras(self):
        """
        List connected cameras.

        :return: A list of connected camera descriptions.
        """
        connected_cameras = []
        for i in range(10):  # Assume a maximum of 10 cameras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                connected_cameras.append(f'Camera {i}')
                cap.release()  # Release the camera for other uses
        return connected_cameras

    def change_camera(self, camera_index):
        """
        Change the active camera to the one with the specified index.

        :param camera_index: Index of the camera to switch to.
        """
        if self.cap is not None:
            self.cap.release()
        self.cap = self._choose_camera(camera_index)
        self.camera_index = camera_index

    def run(self):
        """
        Start capturing video from the selected camera.
        """
        self.ret, self.frame = self.cap.read()

    def stop(self):
        """
        Stop capturing video.
        """
        self._run_flag = False

    def release(self):
        """
        Release the active camera.
        """
        if self.cap is not None:
            self.cap.release()
    
    
    def update_gain(self, gain_value=10):
        pass



            
        





class UeyeCamera:
    def __init__(self, number: int):
        self.pcMem = ueye.c_mem_p()
        self.memId = ueye.int()  
        self.pitch = ueye.int()
        self.hCam = ueye.HIDS(number)
        self.rectAOI = ueye.IS_RECT()
        ueye.is_InitCamera(self.hCam, None)

    def init(self, x: int = 0, y: int = 0, width = 1000,
             height= 1000, exposure: float = 2.0,
             trigger: bool = False, delay: int = 0):
        

        x = x - x % 8
        width = width - width % 8
        y = y - y % 2
        height = height - height % 2
        
        self.width = ueye.int(int(width))
        self.height = ueye.int(int(height))
        self.bpp = ueye.int(get_bits_per_pixel(self.get_colormode()))

        self.rectAOI = ueye.IS_RECT()
        self.rectAOI.s32X = ueye.int(x)
        self.rectAOI.s32Y = ueye.int(y)
        self.rectAOI.s32Width = ueye.int(width)
        self.rectAOI.s32Height = ueye.int(height)
        ueye.is_AOI(self.hCam, ueye.IS_AOI_IMAGE_SET_AOI,
                    self.rectAOI, ueye.sizeof(self.rectAOI))

        ueye.is_SetColorMode(self.hCam, ueye.IS_GET_COLOR_MODE)
        ueye.is_AllocImageMem(self.hCam, self.width, self.height,
                              self.bpp, self.pcMem, self.memId)
        ueye.is_AddToSequence(self.hCam, self.pcMem, self.memId)
        ueye.is_InquireImageMem(self.hCam, self.pcMem, self.memId,
                               self.width, self.height, self.bpp, self.pitch)

        ms = ueye.DOUBLE(exposure)
        ueye.is_Exposure(self.hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, 
                         ms, ueye.sizeof(ms))

        if trigger:
            ueye.is_SetExternalTrigger(self.hCam, ueye.IS_SET_TRIGGER_LO_HI)
            d = ueye.int(delay)
            ueye.is_SetTriggerDelay(self.hCam, d)

        ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)

    def capture(self):
        ueye.is_FreezeVideo(self.hCam, ueye.IS_WAIT)
        img = ueye.get_data(self.pcMem, self.width, self.height,
                            self.bpp, self.pitch, False)
        img = np.reshape(img, (self.height.value, self.width.value, 3))
        return img
    
    def update_gain(self, gain_value=10):
        ueye.is_SetHardwareGain(
            self.hCam,
            gain_value,
            ueye.IS_IGNORE_PARAMETER,
            ueye.IS_IGNORE_PARAMETER,
            ueye.IS_IGNORE_PARAMETER,
        )
    
    def stop(self):
        ueye.is_StopLiveVideo(self.hCam, ueye.IS_FORCE_VIDEO_STOP)
        ueye.is_FreeImageMem(self.hCam, self.pcMem, self.memId)
        ueye.is_ExitCamera(self.hCam)
    def exit(self):
        ret = None
        if self.hCam is not None:
            ret = ueye.is_ExitCamera(self.hCam)
        if ret == ueye.IS_SUCCESS:
            self.hCam = None

    def release(self):
        pass

    def get_format_list(self):
        count = ueye.UINT()
        check(ueye.is_ImageFormat(self.hCam, ueye.IMGFRMT_CMD_GET_NUM_ENTRIES, count, ueye.sizeof(count)))
        format_list = ueye.IMAGE_FORMAT_LIST(ueye.IMAGE_FORMAT_INFO * count.value)
        format_list.nSizeOfListEntry = ueye.sizeof(ueye.IMAGE_FORMAT_INFO)
        format_list.nNumListElements = count.value
        check(ueye.is_ImageFormat(self.hCam, ueye.IMGFRMT_CMD_GET_LIST,
                                    format_list, ueye.sizeof(format_list)))
        return format_list    
    
    def check(ret):
        if ret != ueye.IS_SUCCESS:
            raise uEyeException(ret)
        else:
            return ueye.IS_SUCCESS

    def get_colormode(self):
        ret = ueye.is_SetColorMode(self.hCam, ueye.IS_GET_COLOR_MODE)
        return ret

    def get_aoi(self):
            rect_aoi = ueye.IS_RECT()
            ueye.is_AOI(self.hCam, ueye.IS_AOI_IMAGE_GET_AOI, rect_aoi, ueye.sizeof(rect_aoi))
            print((int(rect_aoi.s32X),
                        int(rect_aoi.s32Y),
                        int(rect_aoi.s32Width),
                        int(rect_aoi.s32Height)))
            return (int(rect_aoi.s32X),
                        int(rect_aoi.s32Y),
                        int(rect_aoi.s32Width),
                        int(rect_aoi.s32Height))