WIDTH = 640
HEIGHT = 360
FPS = 30

SRT_URL = (
    "srt://127.0.0.1:8890"
    "?streamid=publish:webcam"
    "&mode=caller"
    "&latency=10000"
    "&rcvlatency=10000"
    "&peerlatency=10000"
    "&tlpktdrop=1"
)