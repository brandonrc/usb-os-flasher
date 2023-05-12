import os
import tkinter as tk
from tkinter import filedialog, ttk
from pyudev import Context
from subprocess import Popen, PIPE, STDOUT
import subprocess
import threading

class FlashApp:
    def __init__(self, root):
        self.root = root
        self.root.title('USB Flasher')
        self.context = Context()

        # Label
        self.label = tk.Label(root, text="Choose an xz file")
        self.label.pack()

        # Button to choose file
        self.button = tk.Button(root, text="Choose file", command=self.load_file)
        self.button.pack()

        # Progress bar
        self.progress = ttk.Progressbar(root, length=200)
        self.progress.pack()

        # Button to flash USB
        self.flash_button = tk.Button(root, text="Flash USB", command=self.flash_usb)
        self.flash_button.pack()

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("xz files", "*.xz")])
        self.label.config(text=self.filename)

    def flash_usb(self):
        # Ensure a file has been selected
        if not hasattr(self, 'filename'):
            self.label.config(text="Please select a file first.")
            return

        # Get the first USB device (for simplicity)
        usb_device = self.get_usb_device()

        if usb_device:
            # Clean and flash the USB device in a new thread to avoid blocking the GUI
            threading.Thread(target=self.clean_and_flash_device, args=(usb_device, self.filename)).start()
        else:
            self.label.config(text="No USB device found.")

    def get_usb_device(self):
        # For simplicity, get the first USB device
        # Modify this to suit your needs
        for device in self.context.list_devices(subsystem='usb'):
            return device.device_node

    def clean_and_flash_device(self, device, filename):
        # Clean the device
        self.clean_device(device)

        # Decompress the xz file
        os.system(f'unxz --keep {filename}')

        # Get the image file name
        image_file = filename.rstrip('.xz')

        # Use the dd command to flash the USB
        # Run dd in a separate process, and get its output
        process = Popen(['sudo', 'dd', f'if={image_file}', f'of={device}', 'bs=4M', 'status=progress'], stdout=PIPE, stderr=STDOUT)
        for line in iter(process.stdout.readline, b''):
            # Parse the output to get the progress
            # This assumes the output is in the format: 'bytes_transferred bytes'
            bytes_transferred = int(line.split()[0])
            self.update_progress(bytes_transferred)

        # Inform the user
        self.label.config(text=f"Flashing {device} with {filename} completed.")

    def update_progress(self, bytes_transferred):
        # Calculate the progress and update the progress bar
        # This assumes the total size is known
        total_size = 1000000000  # Replace with the actual total size
        progress = (bytes_transferred / total_size) * 100
        self.progress['value'] = progress
 
    def clean_device(self, device):
        # Unmount all partitions
        # subprocess.run(['umount', '-f', f'{device}*'], check=False)

        # All images that osbuilder makes has the volume group named root. 
        # We should try to keep this the same when we move to kickstart files
        # and preceed files for ubuntu. '
        
        self.remove_volume_group("rootvg")

        # Remove all partitions
        # subprocess.run(['sudo', 'sfdisk', '--delete', device], check=False)
        self.unmount_and_delete_all_partitions(device=device)

        # Wipe the partition table
        subprocess.run(['sudo', 'wipefs', '--all', device], check=False)

        print(f"Device {device} cleaned successfully.")

    def remove_logical_volume(self, lv_name, vg_name):
        """
        Remove a logical volume.
        lv_name: Logical volume name
        vg_name: Volume group name
        """
        try:
            subprocess.run(['lvremove', '-f', f'{vg_name}/{lv_name}'], check=True)
            print(f"Logical volume {lv_name} removed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to remove logical volume {lv_name}.")

    def remove_volume_group(self, vg_name):
        """
        Remove a volume group.
        vg_name: Volume group name
        """
        try:
            subprocess.run(['vgremove', '-f', vg_name], check=True)
            print(f"Volume group {vg_name} removed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to remove volume group {vg_name}.")

    # TODO: Might need to see how to get the device string from the main 
    # program
    def unmount_and_delete_all_partitions(self, device):
        # Find all partitions for the device
        partitions = [f"/dev/{f}" for f in os.listdir('/dev') if f.startswith(device.split('/')[-1])]

        # Unmount all partitions
        for partition in partitions:
            try:
                subprocess.check_call(['umount', partition])
                print(f"Successfully unmounted {partition}.")
            except subprocess.CalledProcessError:
                print(f"Could not unmount {partition}.")

        # Delete all partitions
        try:
            subprocess.check_call(['sfdisk', '--delete', device])
            print(f"Successfully deleted all partitions on {device}.")
        except subprocess.CalledProcessError:
            print(f"Could not delete partitions on {device}.")


root = tk.Tk()
app = FlashApp(root)
root.mainloop()