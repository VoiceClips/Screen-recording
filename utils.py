import tkinter
import glob
import cv2
from typing import Tuple

def get_desktop_resolution() -> Tuple[int, int]:
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width, height

def get_default_output_path(ext: str = "mkv") -> str:
    filenames = glob.glob(f"out_????.{ext}")
    for i in range(1, 10000):
        name = f"out_{i:04d}.{ext}"
        if name not in filenames:
            return name
    return f"out_9999.{ext}"

def list_available_devices():
    index = 0
    available_devices = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        available_devices.append(f"Device {index}")
        cap.release()
        index += 1
    return available_devices

def list_available_audio_devices():
    # Placeholder: List available audio devices
    return ["Default Microphone", "External Microphone"]
