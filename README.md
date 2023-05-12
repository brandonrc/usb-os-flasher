# USB Flasher

USB Flasher is a Python GUI application to flash a USB device with a compressed .xz image file.

## Features

- Select an .xz file from your file system.
- Automatically detects the first USB device connected to your system.
- Safely prepares the USB device by unmounting all partitions, deleting them, and wiping the partition table.
- Decompresses the .xz file and flashes it to the USB device.
- Displays a progress bar while the image is being flashed.

## Prerequisites

- Python 3.7 or higher
- Poetry (for dependency management and building)

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/usb_os_flasher.git
```

### Navigate to the cloned directory

```bash
cd usb_os_flasher
```

### Install the required Python packages

```bash
poetry install
```

## Usage

Run the application:

```bash
poetry run python usb_os_flasher/usb_os_flasher.py
```

## Building a Standalone Executable

Install PyInstaller as a development dependency:

```bash
poetry add pyinstaller --dev
```

Build the standalone executable with PyInstaller:

```bash
poetry run pyinstaller usb_os_flasher/usb_os_flasher.py
```

This will create a `dist` directory containing the standalone application. You can distribute this application to users, and they can run it without needing to have Python or any dependencies installed.

## Notes

- This application should be run with superuser (root) privileges to ensure proper access to the USB device. 
- The application automatically selects the first USB device it finds. If you have multiple USB devices connected and want to select a specific one, you'll need to modify the `get_usb_device` function in the script.
- The cleaning and flashing process can take a while, depending on the size of the image file and the speed of your USB device. Please be patient and do not interrupt the process once it has started.
- Use this application with caution. It will permanently delete all data on the specified USB device. Always ensure you are providing the correct device and image file to avoid data loss.

---

Please replace `"yourusername"` with your GitHub username.