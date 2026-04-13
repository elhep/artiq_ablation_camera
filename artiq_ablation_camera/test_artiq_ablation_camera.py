import sys
import unittest
from sipyco.test.generic_rpc import GenericRPCCase
from sipyco.pc_rpc import Client
from artiq_ablation_camera.artiq_ablation_camera_I import AblationCameraInterface
import abc


class GenericAblationCameraTest(unittest.TestCase, abc.ABC):

    @abc.abstractmethod
    def setUp(self):
        self.artiq_ablation_camera: AblationCameraInterface | Client

    def test_set_camera_exposure(self):
        exposure = 10
        self.artiq_ablation_camera.set_camera_exposure(exposure)
        self.assertEqual(exposure, self.artiq_ablation_camera.get_camera_exposure())

    def test_set_camera_gain(self):
        gain = 10
        self.artiq_ablation_camera.set_camera_gain(gain)
        self.assertEqual(gain, self.artiq_ablation_camera.get_camera_gain())

    def test_set_camera_brightness(self):
        brightness = 10
        self.artiq_ablation_camera.set_camera_brightness(brightness)
        self.assertEqual(brightness, self.artiq_ablation_camera.get_camera_brightness())
    
    def test_set_camera_contrast(self):
        contrast = 30
        self.artiq_ablation_camera.set_camera_contrast(contrast)
        self.assertEqual(contrast, self.artiq_ablation_camera.get_camera_contrast())
    
    def test_set_ROI_x0(self):
        x0 = 30
        self.artiq_ablation_camera.set_ROI_x0(x0)
        self.assertEqual(x0, self.artiq_ablation_camera.get_ROI_x0())
    
    def test_set_ROI_y0(self):
        y0 = 30
        self.artiq_ablation_camera.set_ROI_y0(y0)
        self.assertEqual(y0, self.artiq_ablation_camera.get_ROI_y0())
    
    def test_set_ROI_dx(self):
        dx = 30
        self.artiq_ablation_camera.set_ROI_dx(dx)
        self.assertEqual(dx, self.artiq_ablation_camera.get_ROI_dx())
    
    def test_set_ROI_dy(self):
        dy = 30
        self.artiq_ablation_camera.set_ROI_dy(dy)
        self.assertEqual(dy, self.artiq_ablation_camera.get_ROI_dy())

    def test_set_ROI_enable(self):
        enable = 1
        self.artiq_ablation_camera.set_ROI_enable(enable)
        self.assertEqual(enable, self.artiq_ablation_camera.get_ROI_enable())

    def test_set_target_x0(self):
        x0 = 30
        self.artiq_ablation_camera.set_target_x0(x0)
        self.assertEqual(x0, self.artiq_ablation_camera.get_target_x0())
    
    def test_set_target_y0(self):
        y0 = 30
        self.artiq_ablation_camera.set_target_y0(y0)
        self.assertEqual(y0, self.artiq_ablation_camera.get_target_y0())

    def test_set_target_error_x(self):
        x0 = 30
        # self.artiq_ablation_camera.set_target_errorx(x0)
        self.assertEqual(x0, self.artiq_ablation_camera.get_target_error_x())
    
    def test_set_target_error_y(self):
        y0 = 30
        self.artiq_ablation_camera.set_target_y0(y0)
        self.assertEqual(y0, self.artiq_ablation_camera.get_target_y0())

class TestAblationCameraSim(GenericRPCCase, GenericAblationCameraTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m artiq_ablation_camera.aqctl_artiq_ablation_camera"
            + " -p 3280 --simulation"
        )
        self.artiq_ablation_camera = self.start_server("artiq_ablation_camera", command, 3280)