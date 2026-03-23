import subprocess
import threading
import queue


class SRTStreamer:
    def __init__(self, width, height, fps, url):
        self.width = width
        self.height = height
        self.fps = fps
        self.url = url

        self.process = None
        self.queue = queue.Queue(maxsize=2)

        self.running = False
        self.thread = None

    def start(self):

        cmd = [
            "ffmpeg",

            "-loglevel", "error",

            "-fflags", "nobuffer",
            "-flags", "low_delay",

            "-f", "rawvideo",
            "-pix_fmt", "bgr24",

            "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps),

            "-i", "-",

            "-c:v", "libx264",

            "-preset", "ultrafast",
            "-tune", "zerolatency",

            "-g", "30",
            "-keyint_min", "30",

            "-bf", "0",
            "-refs", "1",

            "-b:v", "2M",
            "-maxrate", "2M",
            "-bufsize", "2M",

            "-pix_fmt", "yuv420p",

            "-flush_packets", "1",

            "-f", "mpegts",

            self.url
        ]

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            bufsize=0
        )

        self.running = True

        self.thread = threading.Thread(
            target=self._worker,
            daemon=True
        )

        self.thread.start()

    def _worker(self):

        while self.running:

            try:

                frame = self.queue.get(timeout=1)

                if frame is None:
                    break

                self.process.stdin.write(frame.tobytes())

            except Exception:
                pass

    def send_frame(self, frame):

        if not self.running:
            return

        try:

            self.queue.put_nowait(frame)

        except queue.Full:

            try:
                self.queue.get_nowait()
                self.queue.put_nowait(frame)

            except:
                pass

    def stop(self):

        self.running = False

        try:

            self.queue.put(None)

        except:
            pass

        if self.process:
            self.process.terminate()