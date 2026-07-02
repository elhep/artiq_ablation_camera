from artiq_ablation_camera.artiq_ablation_camera_I import AblationCameraInterface, AblationCameraException
import numpy as np
from enum import Enum
import serial
from typing import Optional, Union
from PIL import Image

CHUNK_SIZE = 1024

class COMMANDS(Enum):
    CAM_EXPOSURE = ":camera:exposure"
    CAM_GAIN = ":camera:gain"
    CAM_BRIGHTNESS = ":camera:brightness"
    CAM_CONTRAST = ":camera:contrast"

    ROI_X0 = ":roi:x0"
    ROI_Y0 = ":roi:y0"
    ROI_DX = ":roi:dx"
    ROI_DY = ":roi:dy"
    ROI_ENABLE = ":roi:enable"

    TARGET_X0 = ":target:x0"
    TARGET_Y0 = ":target:y0"
    TARGET_TOLERANCE = ":target:tolerance"
    TARGET_ERRX = ":target:error:x"
    TARGET_ERRY = ":target:error:y"
    TARGET_HIT = ":target:hit"

    CENTROID_X0 = ":centroid:x0"
    CENTROID_Y0 = ":centroid:y0"

    IMAGE_CAPTURE = ":image:capture"
    IMAGE_PREV = ":image:preview"
    IMAGE_GET = ":image:image"
    IMAGE_ROI = ":image:roi"

class COMMAND_STATUS(Enum):
    OK = ":OK"
    UNKNOWN = ":ERR:UNKNOWN"
    NOT_QUERRY = ":ERR:NOTQUERRY"
    NOT_SET = ":ERR:NOTSET"
    ERROR = ":ERR"

    PARSE_ERROR = ":ERR:PARSE"
    COM_ERROR = ":ERR:COM"

class AblationCamera(AblationCameraInterface):

    def __init__(self, device: str, baudrate: int = 115200, timeout: float = 1.0):
        self.device = device
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial: Optional[serial.Serial] = None
        self._status_update_active = False
        self.connect()
    
    def log(self, msg: str) -> None:
        print(f"[{self.__class__.__name__}] {msg}")

    def connect(self) -> COMMAND_STATUS:
        """Open serial connection to the controller."""
        try:
            self.serial = serial.Serial(
                port=self.device,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            self.log(f"Connected to {self.device}")
        except serial.SerialException:
            self.log(f"Failed to connect to {self.device}")
            return COMMAND_STATUS.COM_ERROR
        return COMMAND_STATUS.OK
    
    def close(self) -> None:
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
    
    def _send_write_command(self, command: COMMANDS, value: Union[int, float]) -> COMMAND_STATUS:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR
        
        cmd = f"{command.value} {value}\r\n"
        self.log(f"Write command: {cmd.strip()}")

        try:
            self.serial.read_all()
            self.serial.write(cmd.encode(errors="ignore"))
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            self.log(f"Write response: {resp}")
        except:
            self.log("Serial device caused an exception!")
            return COMMAND_STATUS.COM_ERROR

        parsed_resp = self._parse_response(resp)
        if type(parsed_resp) == COMMAND_STATUS:
            return parsed_resp
        return COMMAND_STATUS.COM_ERROR
    
    def _send_read_command(self, command: COMMANDS) -> Union[COMMAND_STATUS, float]:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR

        cmd = f"{command.value}?\r\n"
        self.log(f"Read command: {cmd.strip()}")

        try:
            self.serial.read_all()
            self.serial.write(cmd.encode(errors="ignore"))
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            self.log(f"Read response: {resp}")
        except:
            self.log("Serial device caused an exception!")
            return COMMAND_STATUS.COM_ERROR
        return self._parse_response(resp)

    def _parse_response(self, response: str) -> Union[COMMAND_STATUS, float]:
        for status in COMMAND_STATUS:
            if status.value in response:
                return status
        try:
            parsed_val = float(response[1:])
            return parsed_val
        except ValueError:
            return COMMAND_STATUS.PARSE_ERROR

    async def get_camera_exposure(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.CAM_EXPOSURE)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_camera_exposure(self, val: int) -> str:
        return self._send_write_command(COMMANDS.CAM_EXPOSURE, val).value

    async def get_camera_gain(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.CAM_GAIN)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_camera_gain(self, val: int) -> str:
        return self._send_write_command(COMMANDS.CAM_GAIN, val).value

    async def get_camera_brightness(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.CAM_BRIGHTNESS)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_camera_brightness(self, val: int) -> str:
        return self._send_write_command(COMMANDS.CAM_BRIGHTNESS, val).value

    async def get_camera_contrast(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.CAM_CONTRAST)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_camera_contrast(self, val: int) -> str:
        return self._send_write_command(COMMANDS.CAM_CONTRAST, val).value


    async def get_ROI_x0(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.ROI_X0)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_ROI_x0(self, val: int) -> str:
        return self._send_write_command(COMMANDS.ROI_X0, val).value

    async def get_ROI_y0(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.ROI_Y0)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_ROI_y0(self, val: int) -> str:
        return self._send_write_command(COMMANDS.ROI_Y0, val).value

    async def get_ROI_dx(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.ROI_DX)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_ROI_dx(self, val: int) -> str:
        return self._send_write_command(COMMANDS.ROI_DX, val).value

    async def get_ROI_dy(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.ROI_DY)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_ROI_dy(self, val: int) -> str:
        return self._send_write_command(COMMANDS.ROI_DY, val).value

    async def get_ROI_enable(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.ROI_ENABLE)
        if type(val) == float:
            return int(val)
        return val.value

    async def set_ROI_enable(self, val: int) -> str:
        return self._send_write_command(COMMANDS.ROI_ENABLE, val).value


    async def get_target_x0(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.TARGET_X0)
        if type(val) == float:
            return val
        return val.value

    async def set_target_x0(self, val: float) -> str:
        return self._send_write_command(COMMANDS.TARGET_X0, val).value

    async def get_target_y0(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.TARGET_Y0)
        if type(val) == float:
            return val
        return val.value

    async def set_target_y0(self, val: float) -> str:
        return self._send_write_command(COMMANDS.TARGET_Y0, val).value

    async def get_target_tolerance(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.TARGET_TOLERANCE)
        if type(val) == float:
            return val
        return val.value

    async def set_target_tolerance(self, val: float) -> str:
        return self._send_write_command(COMMANDS.TARGET_TOLERANCE, val).value

    async def get_target_error_x(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.TARGET_ERRX)
        if type(val) == float:
            return val
        return val.value

    async def get_target_error_y(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.TARGET_ERRY)
        if type(val) == float:
            return val
        return val.value

    async def get_target_is_hit(self) -> Union[str, int]:
        val = self._send_read_command(COMMANDS.TARGET_HIT)
        if type(val) == float:
            return int(val)
        return val.value


    async def get_centroid_x0(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.CENTROID_X0)
        if type(val) == float:
            return val
        return val.value

    async def get_centroid_y0(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.CENTROID_Y0)
        if type(val) == float:
            return val
        return val.value


    async def trigger_capture_image(self) -> str:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR.value
        
        cmd = f"{COMMANDS.IMAGE_CAPTURE.value}\r\n"
        self.log(f"Trigger capture command: {cmd.strip()}")

        try:
            self.serial.read_all()
            self.serial.write(cmd.encode(errors="ignore"))
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            self.log(f"Response: {resp}")
        except:
            self.log("Serial device caused an exception!")
            return COMMAND_STATUS.COM_ERROR.value

        parsed_resp = self._parse_response(resp)
        if type(parsed_resp) == COMMAND_STATUS:
            return parsed_resp.value
        return COMMAND_STATUS.COM_ERROR.value
    
    async def wait_for_image_ready(self) -> str:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR.value

        try:
            self.serial.timeout = 5
            counter = 4
            while not (resp := self.serial.readline().decode(errors="ignore")).endswith("Camera snapshot taken!"):
                if counter == 0:
                    break
                counter -= 1
            self.log(f"Response: {resp}")
        except:
            return COMMAND_STATUS.COM_ERROR.value
        finally:
            self.serial.timeout = 1
        
        parsed_resp = self._parse_response(resp)
        if type(parsed_resp) == COMMAND_STATUS:
            return parsed_resp.value
        return COMMAND_STATUS.COM_ERROR.value


    async def get_roi_image(self) -> Union[str, list[list[int]]]:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR.value
        
        cmd = f"{COMMANDS.IMAGE_ROI.value}?\r\n"
        self.log(f"Get image command: {cmd.strip()}")

        try:
            self.serial.read_all()
            self.serial.write(cmd.encode(errors="ignore"))
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            tokens = resp.split()
            w = tokens[1]
            h = tokens[2]
            b_count = tokens[3]
            size = w * h * b_count
            self.log(f"IMG expected byte count: {size}")

            self.serial.timeout = 5
            data = self.serial.read(size)
            self.serial.timeout = 1

            self.log(f"IMG read byte count: {len(data)}")
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            self.log(f"IMG read response: {resp}") #TODO Check why it returns weird values
            resp = self._parse_response(resp)
            
        except:
            self.log("Serial device caused an exception!")
            return COMMAND_STATUS.COM_ERROR.value
        
        # if resp != COMMAND_STATUS.OK:
        #     if type(resp) == COMMAND_STATUS:
        #         return resp.value
        #     return str(resp)
        
        try:
            img = Image.frombytes(
                "L",
                (w, h),
                data,
                "raw",
                "L"
            )
        except:
            self.log("Parsing image failed")
            return COMMAND_STATUS.PARSE_ERROR.value
        
        arr_image = np.array(img, dtype=np.uint8)
        return arr_image.tolist()
    
    async def get_image(self) -> Union[str, list[list[int]]]:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR.value
        
        cmd = f"{COMMANDS.IMAGE_GET.value}?\r\n"
        self.log(f"Get image command: {cmd.strip()}")

        try:
            self.serial.read_all()
            self.serial.write(cmd.encode(errors="ignore"))
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            size = int(resp.split()[1])
            self.log(f"IMG expected byte count: {size}")

            self.serial.timeout = 5
            data = self.serial.read(size)
            self.serial.timeout = 1

            self.log(f"IMG read byte count: {len(data)}")
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            self.log(f"IMG read response: {resp}") #TODO Check why it returns weird values
            resp = self._parse_response(resp)
            
        except:
            self.log("Serial device caused an exception!")
            return COMMAND_STATUS.COM_ERROR.value
        
        # if resp != COMMAND_STATUS.OK:
        #     if type(resp) == COMMAND_STATUS:
        #         return resp.value
        #     return str(resp)
        
        try:
            img = Image.frombytes(
                "L",
                (640, 480),
                data,
                "raw",
                "L"
            )
        except:
            self.log("Parsing image failed")
            return COMMAND_STATUS.PARSE_ERROR.value
        
        arr_image = np.array(img, dtype=np.uint8)
        return arr_image.tolist()
    
    async def get_image_preview(self) -> Union[str, list[list[list[int]]]]:
        if self.serial is None:
            if self.connect() == COMMAND_STATUS.COM_ERROR:
                return COMMAND_STATUS.COM_ERROR.value

        cmd = f"{COMMANDS.IMAGE_PREV.value}?\r\n"
        self.log(f"Get image command: {cmd}")
        try:
            self.serial.read_all()
            self.serial.write(cmd.encode("ascii"))
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            size = int(resp.split()[1])
            self.log(f"IMG PREVIEW expected byte count: {size}")

            self.serial.timeout = 5
            data = self.serial.read(size)
            self.serial.timeout = 1

            self.log(f"IMG PREVIEW read byte count: {len(data)}")
            while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
                pass
            self.log(f"IMG PREVIEW response: {resp}")
            resp = self._parse_response(resp)
        except:
            self.log("Serial device caused an exception!")
            return COMMAND_STATUS.COM_ERROR.value
        
        # if resp != COMMAND_STATUS.OK:
        #     if type(resp) == COMMAND_STATUS:
        #         return resp.value
        #     return str(resp)
        
        try:
            img = Image.frombytes(
                "RGB",
                (640, 480),
                data,
                "raw",
                "BGR"
            )
        except:
            self.log("Parsing image failed")
            return COMMAND_STATUS.PARSE_ERROR.value
        
        arr_image = np.array(img, dtype=np.uint8)
        return arr_image.tolist()