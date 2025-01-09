import platform

def video_capture_command(fps, width, height, audio, output_path):
    system = platform.system()
    if system == "Darwin":  # macOS
        av_input = "1:none" if not audio else "1:0"  # Full screen + audio input
        return [
            "ffmpeg", "-f", "avfoundation", "-framerate", str(fps),
            "-video_size", f"{width}x{height}",
            "-pix_fmt", "uyvy422",  # Fixed pixel format for macOS
            "-i", av_input, "-c:v", "libx264",
            "-preset", "ultrafast", "-c:a", "aac", "-b:a", "128k", output_path
        ]
    elif system == "Linux":
        return [
            "ffmpeg", "-f", "x11grab", "-r", str(fps), "-s", f"{width}x{height}",
            "-i", ":0.0", "-f", "pulse", "-i", "default", "-c:v", "libx264",
            "-preset", "ultrafast", "-c:a", "aac", "-b:a", "128k", output_path
        ]
    elif system == "Windows":
        return [
            "ffmpeg", "-f", "gdigrab", "-framerate", str(fps), "-i", "desktop",
            "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-b:a", "128k", output_path
        ]
