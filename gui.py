import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
from PIL import Image, ImageTk
import mss  # For live preview
from capture import video_capture_command
from constants import DEFAULT_FPS, DEFAULT_FILE_EXTENSION, ACCEPTABLE_FILE_EXTENSIONS
from utils import get_desktop_resolution

class ScreenRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Recorder with Full-Screen Capture")
        self.recording_process = None
        self.screen_capture_active = False

        # GUI layout
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.preview_frame = tk.Frame(self.main_frame, width=640, height=480)
        self.preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.preview_frame.pack_propagate(False)

        self.video_canvas = tk.Label(self.preview_frame, bg="black")
        self.video_canvas.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.preview_label = tk.Label(self.control_frame, text="Recording Controls", font=("Helvetica", 16))
        self.preview_label.pack(pady=10)

        default_width, default_height = get_desktop_resolution()
        self.res_label = tk.Label(self.control_frame, text="Resolution (WxH):")
        self.res_label.pack()
        self.resolution_entry = tk.Entry(self.control_frame)
        self.resolution_entry.insert(0, f"{default_width}x{default_height}")
        self.resolution_entry.pack(pady=5)

        self.fps_label = tk.Label(self.control_frame, text="Frames per Second (FPS):")
        self.fps_label.pack()
        self.fps_entry = tk.Entry(self.control_frame)
        self.fps_entry.insert(0, str(DEFAULT_FPS))
        self.fps_entry.pack(pady=5)

        self.audio_checkbox = tk.BooleanVar(value=True)
        self.audio_checkbutton = tk.Checkbutton(self.control_frame, text="Record Audio", variable=self.audio_checkbox)
        self.audio_checkbutton.pack(pady=5)

        self.start_button = tk.Button(self.control_frame, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.control_frame, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=5)

    def show_preview(self):
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # Capture the primary screen
            while self.screen_capture_active:
                frame = sct.grab(monitor)
                img = Image.frombytes("RGB", frame.size, frame.rgb)
                img_resized = img.resize((640, 480))
                imgtk = ImageTk.PhotoImage(image=img_resized)
                self.video_canvas.imgtk = imgtk
                self.video_canvas.config(image=imgtk)
                self.master.after(100)

    def start_recording(self):
        resolution = self.resolution_entry.get()
        fps = int(self.fps_entry.get())
        width, height = map(int, resolution.split('x'))
        record_audio = self.audio_checkbox.get()

        # Ask user where to save the recording
        file_type = filedialog.asksaveasfilename(defaultextension=f".{DEFAULT_FILE_EXTENSION}",
                                                 filetypes=[(ext.upper(), f"*.{ext}") for ext in ACCEPTABLE_FILE_EXTENSIONS])
        if not file_type:
            messagebox.showinfo("Cancelled", "File save cancelled.")
            return

        # Start live preview using `mss`
        self.screen_capture_active = True
        threading.Thread(target=self.show_preview, daemon=True).start()

        # Start recording directly to output file
        command = video_capture_command(fps, width, height, record_audio, file_type)
        self.recording_process = subprocess.Popen(command)

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_recording(self):
        self.screen_capture_active = False  # Stop live preview

        if self.recording_process:
            self.recording_process.terminate()
            self.recording_process.wait()

        self.video_canvas.config(image="")  # Clear live preview

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        messagebox.showinfo("Recording Stopped", "Recording saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = ScreenRecorderApp(root)
    root.mainloop()
