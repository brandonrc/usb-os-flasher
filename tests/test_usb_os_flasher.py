import unittest
from unittest.mock import patch
import usb_os_flasher

class TestUSBFlasher(unittest.TestCase):
    @patch('usb_os_flasher.subprocess.run')
    def test_remove_partitions(self, mock_run):
        usb_os_flasher.remove_partitions("/dev/sdX")
        mock_run.assert_called_with(["sudo", "parted", "/dev/sdX", "--script", "--", "rm", "all"], check=True)

    @patch('usb_os_flasher.subprocess.run')
    def test_flash_image(self, mock_run):
        usb_os_flasher.flash_image("/path/to/image.xz", "/dev/sdX")
        mock_run.assert_called_with(
            ['xzcat', '/path/to/image.xz', '|', 'sudo', 'dd', 'of=/dev/sdX', 'bs=4M', 'status=progress'], 
            check=True
        )

if __name__ == '__main__':
    unittest.main()