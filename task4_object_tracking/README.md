# Task 4 — Object Detection and Tracking

Uses Ultralytics YOLO with ByteTrack to detect and track objects in a webcam or video.

## Run with webcam

```bash
python track.py --source 0
```

## Run with a video

```bash
python track.py --source input.mp4
```

The result is written to `output/tracked.mp4`.

The first run may download the YOLO model automatically.
