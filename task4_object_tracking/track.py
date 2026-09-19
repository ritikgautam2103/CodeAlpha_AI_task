import argparse
from pathlib import Path
import cv2
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument("--source", default="0", help="0 for webcam or path to a video file")
parser.add_argument("--model", default="yolo11n.pt", help="Ultralytics YOLO model")
parser.add_argument("--tracker", default="bytetrack.yaml", help="Tracker config")
args = parser.parse_args()

source = int(args.source) if args.source.isdigit() else args.source
output_dir = Path(__file__).resolve().parent / "output"
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "tracked.mp4"

model = YOLO(args.model)

cap = cv2.VideoCapture(source)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video source: {args.source}")

fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 1:
    fps = 30.0

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter(
    str(output_path),
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height),
)

print("Press Q to stop.")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    results = model.track(
        frame,
        persist=True,
        tracker=args.tracker,
        conf=0.35,
        verbose=False,
    )

    annotated = results[0].plot()
    writer.write(annotated)

    cv2.imshow("YOLO Object Detection + Tracking", annotated)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()
print(f"Saved output to: {output_path}")
