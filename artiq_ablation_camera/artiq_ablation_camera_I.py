import abc
from typing import Union

class AblationCameraException(Exception):
    pass

class AblationCameraInterface(abc.ABC):

    @abc.abstractmethod
    async def get_camera_exposure(self) -> Union[str, int]:
        '''Get the exposure value of the camera
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_camera_exposure(self, val: int) -> str:
        '''Set the exposure value of the camera
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_camera_gain(self) -> Union[str, int]:
        '''Get the gain value of the camera
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_camera_gain(self, val: int) -> str:
        '''Set the gain value of the camera
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_camera_brightness(self) -> Union[str, int]:
        '''Get the brightness value of the camera
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_camera_brightness(self, val: int) -> str:
        '''Set the brightness value of the camera
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_camera_contrast(self) -> Union[str, int]:
        '''Get the contrast value of the camera
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_camera_contrast(self, val: int) -> str:
        '''Set the contrast value of the camera
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''


    @abc.abstractmethod
    async def get_ROI_x0(self) -> Union[str, int]:
        '''Get x-coordinate of startpoint of ROI
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_ROI_x0(self, val: int) -> str:
        '''Set x-coordinate of startpoint of ROI
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_ROI_y0(self) -> Union[str, int]:
        '''Get y-coordinate of startpoint of ROI
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_ROI_y0(self, val: int) -> str:
        '''Set y-coordinate of startpoint of ROI
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_ROI_dx(self) -> Union[str, int]:
        '''Get x-direction size of ROI
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_ROI_dx(self, val: int) -> str:
        '''Set x-direction size of ROI
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_ROI_dy(self) -> Union[str, int]:
        '''Get y-direction size of ROI
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_ROI_dy(self, val: int) -> str:
        '''Set y-direction size of ROI
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_ROI_enable(self) -> Union[str, int]:
        '''Get the state of ROI being used in calculations
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_ROI_enable(self, val: int) -> str:
        '''Set whether to use ROI in centroid calculation
        Args:
            val: New value to be set (0 or 1)
        
        Returns:
            Operation status 
        '''


    @abc.abstractmethod
    async def get_target_x0(self) -> Union[str, float]:
        '''Get x-coordinate of the target point
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_target_x0(self, val: float) -> str:
        '''Set x-coordinate of the target point
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_target_y0(self) -> Union[str, float]:
        '''Get y-coordinate of the target point
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_target_y0(self, val: float) -> str:
        '''Set y-coordinate of the target point
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_target_tolerance(self) -> Union[str, float]:
        '''Get maximal error between target and actual detection point
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def set_target_tolerance(self, val: float) -> str:
        '''Set maximal error between target and actual detection point
        Args:
            val: New value to be set
        
        Returns:
            Operation status 
        '''

    @abc.abstractmethod
    async def get_target_error_x(self) -> Union[str, float]:
        '''Get x-direction error between target and calculated centroid
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def get_target_error_y(self) -> Union[str, float]:
        '''Get x-direction error between target and calculated centroid
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def get_target_is_hit(self) -> Union[str, int]:
        '''Get a value whether, the measured point is at the target
        
        Returns:
            Requested value or an operation status in case of error
        '''


    @abc.abstractmethod
    async def get_centroid_x0(self) -> Union[str, float]:
        '''Get the x-coordinate of the calculated centroid
        
        Returns:
            Requested value or an operation status in case of error
        '''

    @abc.abstractmethod
    async def get_centroid_y0(self) -> Union[str, float]:
        '''Get the y-coordinate of the calculated centroid
        
        Returns:
            Requested value or an operation status in case of error
        '''


    @abc.abstractmethod
    async def trigger_capture_image(self) -> str:
        '''Send a trigger command to capture an image
        
        Returns:
            Operation status
        '''

    @abc.abstractmethod
    async def get_image(self) -> Union[str, list[list[list[int]]]]:
        '''Get the whole grayscale image

        Returns:
            Operation status in case of an error
            Image as a list
            [[[R G B], ..., [R G B]]
                 .      .       .            
             [[R G B], ..., [R G B]]]
        '''