import argparse
import subprocess
import cv2
import platform
def capture_command(fps, size, audio, output):
    width, height = map(int, size.split("x"))
    system = platform.system()

    if system == "Darwin":
        av_input = "3:1" if audio else "3:none"
        return [
            "ffmpeg", "-f", "avfoundation", "-framerate", str(fps),
            "-video_size", f"{width}x{height}", "-i", av_input, "-c:v", "libx264", output
        ]
    elif system == "Linux":
        return [
            "ffmpeg", "-f", "x11grab", "-r", str(fps), "-s", f"{width}x{height}", "-i", ":0.0", "-c:v", "libx264", output
        ]
    else:
        return [
            "ffmpeg", "-f", "dshow", "-i", "video=screen-capture-recorder", "-c:v", "libx264", output
        ]

def main():
    parser = argparse.ArgumentParser(description="Screen recorder CLI.")
    parser.add_argument("-n", "--no-audio", action="store_true", help="Do not record audio.")
    parser.add_argument("-r", "--fps", type=int, default=30, help="Framerate (e.g., 30).")
    parser.add_argument("-s", "--size", default="1280x720", help="Resolution (e.g., 1280x720).")
    parser.add_argument("output", nargs="?", default="output.mp4", help="Output file name.")

    args = parser.parse_args()

    cmd = capture_command(args.fps, args.size, not args.no_audio, args.output)
    print(f"Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()