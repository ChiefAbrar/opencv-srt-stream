import cv2

from config import WIDTH, HEIGHT, FPS, SRT_URL
from streamer import SRTStreamer


def main():

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    streamer = SRTStreamer(
        WIDTH,
        HEIGHT,
        FPS,
        SRT_URL
    )

    streamer.start()

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(
            frame,
            (WIDTH, HEIGHT)
        )

        streamer.send_frame(frame)

    cap.release()

    streamer.stop()


if __name__ == "__main__":
    main()