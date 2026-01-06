import cv2
import numpy as np
import mss
import time

# Output video file
output_file = "screen_recording.mp4"

# Frame rate
fps = 15

# Screen capture
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Full screen

    width = monitor["width"]
    height = monitor["height"]

    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    print("Recording started... Press CTRL+C to stop.")

    try:
        while True:
            start_time = time.time()

            # Capture screen
            img = sct.grab(monitor)

            # Convert to numpy array
            frame = np.array(img)

            # Convert BGRA → BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Write frame
            out.write(frame)

            # Control FPS
            elapsed = time.time() - start_time
            sleep_time = max(0, (1 / fps) - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    finally:
        out.release()
        cv2.destroyAllWindows()
