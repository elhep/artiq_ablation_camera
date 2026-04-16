from artiq_ablation_camera.artiq_ablation_camera_I import AblationCameraInterface
import dataclasses as dc
from typing import Union

@dc.dataclass
class CAMERA_T:
    exposure: int
    gain: int
    brightness: int
    contrast: int

@dc.dataclass
class ROI_T:
    x0: int
    y0: int
    dx: int
    dy: int
    enable: int

@dc.dataclass
class TARGET_T:
    x0: float
    y0: float
    tolerance: float
    error_x: float
    error_y: float
    is_hit: int

@dc.dataclass
class CENTROID_T:
    x0: float
    y0: float

class AblationCameraSim(AblationCameraInterface):

    def __init__(self):
        self.camera = CAMERA_T(0, 0, 0, 0)
        self.roi = ROI_T(0, 0, 0, 0, 0)
        self.target = TARGET_T(0., 0., 0., 0., 0., 0)
        self.centroid = CENTROID_T(0., 0.)
    
    def close(self):
        pass
    
    async def get_camera_exposure(self) -> Union[str, int]:
        return self.camera.exposure

    async def set_camera_exposure(self, val: int) -> str:
        self.camera.exposure = val
        return ":OK"

    async def get_camera_gain(self) -> Union[str, int]:
        return self.camera.gain

    async def set_camera_gain(self, val: int) -> str:
        self.camera.gain = val
        return ":OK"

    async def get_camera_brightness(self) -> Union[str, int]:
        return self.camera.brightness

    async def set_camera_brightness(self, val: int) -> str:
        self.camera.brightness = val
        return ":OK"

    async def get_camera_contrast(self) -> Union[str, int]:
        return self.camera.contrast

    async def set_camera_contrast(self, val: int) -> str:
        self.camera.contrast = val
        return ":OK"


    async def get_ROI_x0(self) -> Union[str, int]:
        return self.roi.x0

    async def set_ROI_x0(self, val: int) -> str:
        self.roi.x0 = val
        return ":OK"

    async def get_ROI_y0(self) -> Union[str, int]:
        return self.roi.y0

    async def set_ROI_y0(self, val: int) -> str:
        self.roi.y0 = val
        return ":OK"

    async def get_ROI_dx(self) -> Union[str, int]:
        return self.roi.dx

    async def set_ROI_dx(self, val: int) -> str:
        self.roi.dx = val
        return ":OK"

    async def get_ROI_dy(self) -> Union[str, int]:
        return self.roi.dy

    async def set_ROI_dy(self, val: int) -> str:
        self.roi.dy = val
        return ":OK"

    async def get_ROI_enable(self) -> Union[str, int]:
        return self.roi.enable

    async def set_ROI_enable(self, val: int) -> str:
        self.roi.enable = val
        return ":OK"


    async def get_target_x0(self) -> Union[str, float]:
        return self.target.x0

    async def set_target_x0(self, val: float) -> str:
        self.target.x0 = val
        return ":OK"

    async def get_target_y0(self) -> Union[str, float]:
        return self.target.y0

    async def set_target_y0(self, val: float) -> str:
        self.target.y0 = val
        return ":OK"

    async def get_target_tolerance(self) -> Union[str, float]:
        return self.target.tolerance

    async def set_target_tolerance(self, val: float) -> str:
        self.target.tolerance = val
        return ":OK"

    async def get_target_error_x(self) -> Union[str, float]:
        return self.target.error_x

    async def get_target_error_y(self) -> Union[str, float]:
        return self.target.error_y

    async def get_target_is_hit(self) -> Union[str, int]:
        return self.target.is_hit


    async def get_centroid_x0(self) -> Union[str, float]:
        return self.centroid.x0

    async def get_centroid_y0(self) -> Union[str, float]:
        return self.centroid.y0


    async def trigger_capture_image(self) -> str:
        return ":OK"

    async def get_image(self) -> Union[str, list[list[int]]]:
        ret_image: list[list[int]] = []
        for i in range(360):
            ret_image.append([])
            for j in range(360):
                if i == 1 and j == 1:
                    ret_image[i].append(255)
                else:
                    ret_image[i].append(0)
        return ret_image
    
    async def get_image_prev(self) -> Union[str, list[list[list[int]]]]:
        ret_image: list[list[list[int]]] = []
        for i in range(360):
            ret_image.append([])
            for j in range(360):
                if i == 1 and j == 1:
                    ret_image[i].append([255, 255, 255])
                else:
                    ret_image[i].append([0, 0, 0])
        return ret_image