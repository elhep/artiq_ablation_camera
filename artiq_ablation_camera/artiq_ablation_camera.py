from artiq_ablation_camera.artiq_ablation_camera_I import AblationCameraInterface, AblationCameraException
import numpy as np
from enum import Enum
import serial
from typing import Optional, Union
from PIL import Image
from io import BytesIO
import logging

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
    TARGET_ERRX = ":target:error_x"
    TARGET_ERRY = ":target:error_y"
    TARGET_HIT = ":target:hit"

    CENTROID_X0 = ":centroid:x0"
    CENTROID_Y0 = ":centroid:y0"

    IMAGE_CAPTURE = ":image:capture"
    IMAGE_PREV = ":image:preview"

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

    def connect(self) -> None:
        """Open serial connection to the controller."""
        try:
            self.serial = serial.Serial(
                port=self.device,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
        except serial.SerialException as e:
            raise AblationCameraException(f"Failed to connect to {self.device}: {e}")
    
    def close(self) -> None:
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
    
    def _send_write_command(self, command: COMMANDS, value: Union[int, float]) -> COMMAND_STATUS:
        if self.serial is None:
            return COMMAND_STATUS.COM_ERROR
        cmd = f"{command.value} {value}\r\n"
        logging.debug(f"CMD: {cmd}")
        self.serial.write(cmd.encode("ascii"))
        while not (resp := self.serial.readline().decode("ascii")).startswith(":"):
            pass
        logging.debug("RSP: {resp}")
        parsed_resp = self._parse_response(resp)
        if type(parsed_resp) == COMMAND_STATUS:
            return parsed_resp
        return COMMAND_STATUS.COM_ERROR
    
    def _send_read_command(self, command: COMMANDS) -> Union[COMMAND_STATUS, float]:
        if self.serial is None:
            return COMMAND_STATUS.COM_ERROR
        cmd = f"{command.value}?\r\n"
        self.serial.write(cmd.encode("ascii"))
        while not (resp := self.serial.readline().decode("ascii")).startswith(":"):
            pass
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
        val = self._send_read_command(COMMANDS.TARGET_X0)
        if type(val) == float:
            return val
        return val.value

    async def get_centroid_y0(self) -> Union[str, float]:
        val = self._send_read_command(COMMANDS.TARGET_X0)
        if type(val) == float:
            return val
        return val.value


    async def trigger_capture_image(self) -> str:
        if self.serial is None:
            return COMMAND_STATUS.COM_ERROR.value
        cmd = f"{COMMANDS.IMAGE_CAPTURE.value}\r\n"
        self.serial.write(cmd.encode("ascii"))
        while not (resp := self.serial.readline().decode("ascii")).startswith(":"):
            pass
        parsed_resp = self._parse_response(resp)
        if type(parsed_resp) == COMMAND_STATUS:
            return parsed_resp.value
        return COMMAND_STATUS.COM_ERROR.value

    async def get_image(self) -> Union[str, list[list[list[int]]]]:
        if self.serial is None:
            return COMMAND_STATUS.COM_ERROR.value
        cmd = f"{COMMANDS.IMAGE_PREV.value}?\r\n"
        self.serial.write(cmd.encode("ascii"))
        while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
            pass
        size = int(resp.split()[1])
        print(f"Read Bytes: {size}")
        # read_ok = False
        data = self.serial.read(size)
        print("Image received")
        while not (resp := self.serial.readline().decode(errors="ignore")).startswith(":"):
            pass
        resp = self._parse_response(resp)
        if resp != COMMAND_STATUS.OK:
            return resp.value
        print(resp.value)
        # # while (chunk := self.serial.read(CHUNK_SIZE)) != b'':
        # #     data += chunk
        # #     if chunk[-4:] == "END\n":
        # #         read_ok = True
        # #         break
        # if not read_ok:
        #     return COMMAND_STATUS.COM_ERROR.value
        # image = Image.open(BytesIO(data))
        try:
            img = Image.frombytes(
                "RGB",
                (640, 480),
                data,
                "raw",
                "BGR"
            )
            print("RGB image parsed")
        except:
            try:
                img = Image.frombytes(
                    "L",
                    (640, 480),
                    data,
                    "raw",
                    "L"
                )
            except:
                img = None
        if img is None:
            return COMMAND_STATUS.ERROR.value
        arr_image = np.array(img)
        return arr_image.tolist()