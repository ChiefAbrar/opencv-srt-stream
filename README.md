# opencv-srt-stream

Webcam streaming with **near real-time latency** using:

* Python
* OpenCV
* FFmpeg
* SRT (Secure Reliable Transport)
* MediaMTX
* WebRTC (for browser viewing)

---

# Architecture

Python captures webcam frames and streams via SRT to MediaMTX.

MediaMTX converts the stream to WebRTC for browser playback.

Pipeline:

Python → FFmpeg → SRT → MediaMTX → WebRTC → Browser

---

# Folder Structure

```
srt_webcam_stream/
│
├── main.py
├── streamer.py
├── config.py
├── requirements.txt
└── mediamtx.yml
```

---

# Requirements

Install dependencies:

```
pip install -r requirements.txt
```

Install FFmpeg:

Windows:
https://www.gyan.dev/ffmpeg/builds/

Mac:

```
brew install ffmpeg
```

Linux:

```
sudo apt install ffmpeg
```

Install MediaMTX:

https://github.com/bluenviron/mediamtx

---

# MediaMTX Config

Create:

mediamtx.yml

```
paths:
  webcam:
    source: publisher
```

Run MediaMTX:

```
mediamtx
```

---

# How to Run

Start MediaMTX:

```
mediamtx
```

Start webcam stream:

```
python main.py
```

---

# View Stream on Laptop Browser

Open browser:

```
http://127.0._.___:8889/webcam
```

or using LAN IP:

```
http://192.168._.___:8889/webcam
```

Latency:
~50–120 ms

---

# View Stream on Phone

Connect phone to same WiFi network.

Open browser:

```
http://192.168._.___:8889/webcam
```

Replace IP with your PC IP.

Find IP:

Windows:

```
ipconfig
```

Mac/Linux:

```
ifconfig
```

---

# View using VLC (SRT player)

Install VLC:

https://www.videolan.org/

Open network stream:

```
srt://192.168._.___:8890?streamid=read:webcam
```

---

# Configuration

config.py:

```
WIDTH = 640
HEIGHT = 360
FPS = 30

SRT_URL = (
    "srt://127.0._._:8890"
    "?streamid=publish:webcam"
    "&mode=caller"
    "&latency=10000"
    "&rcvlatency=10000"
    "&peerlatency=10000"
    "&tlpktdrop=1"
)
```

---

# SRT Parameter Explanation (Official References)

Official repository:

https://github.com/Haivision/srt

SRT is designed for **sub-second latency streaming**. ([GitHub][1])

---

## latency

Defines how long SRT buffers packets for retransmission.

Lower latency:

* faster delivery
* higher chance of visual glitches

Higher latency:

* smoother playback
* more delay

Typical low latency value:
100 ms or lower. ([gcore.com][2])

In this project:

```
latency=20000
```

20 ms buffer.

---

## rcvlatency and peerlatency

These define buffering on receiver and sender side.

SRT negotiates latency between peers and uses the higher value. ([SRT Lab][3])

Used for packet recovery when network jitter occurs.

---

## tlpktdrop

Too-late packet drop.

If enabled, late packets are discarded instead of delaying playback.

Improves real-time feel.

Recommended for live streaming. ([OSSRS][4])

---

## TSBPD (timestamp-based packet delivery)

SRT uses timestamps to determine packet playback time.

Helps maintain stable timing between frames. ([SRT Lab][5])

---

# Expected Latency

Localhost:
50–120 ms

LAN:
80–150 ms

Internet:
150–400 ms

Latency depends on:

* network RTT
* encoding speed
* CPU performance

SRT latency roughly equals configured buffer + network RTT. ([SRT Lab][5])

---

# Troubleshooting

## No video in browser

Check:

MediaMTX running

```
WebRTC listener opened on :8889
```

Correct path:

```
streamid=publish:webcam
```

Browser URL:

```
http://IP:8889/webcam
```

---

## High latency

Try reducing:

resolution
FPS
latency parameter

Example:

```
WIDTH = 426
HEIGHT = 240
FPS = 24
```

---

## Firewall blocking

Allow ports:

8889 (WebRTC)
8890 (SRT)

---

# Advanced Improvements

Possible upgrades:

GPU encoding (NVENC)
WebRTC-only streaming
Docker deployment
OBS integration
multi-camera streaming

---

# References

SRT Official GitHub:
https://github.com/Haivision/srt

SRT Cookbook:
https://srtlab.github.io/srt-cookbook/

SRT RFC Draft:
https://haivision.github.io/srt-rfc/draft-sharabayko-srt.html

MediaMTX:
https://github.com/bluenviron/mediamtx

FFmpeg:
https://ffmpeg.org/

---

# License

MIT License

---

[1]: https://github.com/Haivision/srt
[2]: https://gcore.com/docs/streaming/live-streaming/protocols/srt
[3]: https://srtlab.github.io/srt-cookbook/protocol/tsbpd/latency-negotiation.html
[4]: https://ossrs.net/lts/en-us/docs/v7/doc/srt
[5]: https://srtlab.github.io/srt-cookbook/protocol/tsbpd/latency.html
