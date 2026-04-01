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


class TestAblationCameraSim(GenericRPCCase, GenericAblationCameraTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m artiq_ablation_camera.aqctl_artiq_ablation_camera"
            + " -p 3280 --simulation"
        )
        self.artiq_ablation_camera = self.start_server("artiq_ablation_camera", command, 3280)