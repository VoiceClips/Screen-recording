#DEFAULT_FPS = 15
#DEFAULT_FILE_EXTENSION = "mkv"
#ACCEPTABLE_FILE_EXTENSIONS = ["avi", "mp4", "mov", "mkv", "ogv", "webm"]
#DEFAULT_CAPTURE_AUDIO_DEVICE = "pulse"
#DEFAULT_CAPTURE_DISPLAY_DEVICE = ":0.0"
#DEFAULT_AUDIO_CODEC = "aac"
#DEFAULT_VIDEO_CODEC = "h264"

#vcodecs = {
#    "h264_lossless": ["-c:v", "libx264", "-g", "15", "-crf", "0", "-pix_fmt", "yuv444p"],
#    "h264": ["-c:v", "libx264", "-vprofile", "baseline", "-g", "15", "-crf", "1", "-pix_fmt", "yuv420p"],
#    "mpeg4": ["-c:v", "mpeg4", "-g", "15", "-qmax", "1", "-qmin", "1"],
#    "huffyuv": ["-c:v", "huffyuv"],
#    "ffv1": ["-c:v", "ffv1", "-coder", "1", "-context", "1"],
#    "vp8": ["-c:v", "libvpx", "-g", "15", "-qmax", "1", "-qmin", "1"],
#}

#acodecs = {
#    "pcm": ["-c:a", "pcm_s16le"],
#    "vorbis": ["-c:a", "libvorbis", "-b:a", "320k"],
#    "mp3": ["-c:a", "libmp3lame", "-b:a", "320k"],
#    "aac": ["-c:a", "libvo_aacenc", "-b:a", "320k"],
#    "ffaac": ["-strict", "experimental", "-c:a", "aac", "-b:a", "320k"],
#q}
import platform

DEFAULT_FPS = 30
DEFAULT_FILE_EXTENSION = "mp4"
ACCEPTABLE_FILE_EXTENSIONS = ["avi", "mp4", "mov", "mkv", "webm"]

if platform.system() == "Darwin":
    DEFAULT_CAPTURE_DISPLAY_DEVICE = "1:0"  # Screen + mic input
    DEFAULT_CAPTURE_AUDIO_DEVICE = "0"  # Fallback for macOS mic if not default
elif platform.system() == "Linux":
    DEFAULT_CAPTURE_DISPLAY_DEVICE = ":0.0"
    DEFAULT_CAPTURE_AUDIO_DEVICE = "default"
else:
    DEFAULT_CAPTURE_DISPLAY_DEVICE = "desktop"
    DEFAULT_CAPTURE_AUDIO_DEVICE = "audio=Microphone"
