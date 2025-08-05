
import os
import csv
import cv2
import matplotlib.pyplot as plt
from datetime import datetime

def save_result(image_path, image, intensity, quantized):
    cv2.imwrite(image_path, image)

    csv_path = os.path.splitext(image_path)[0] + ".csv"
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Moire Intensity", "Quantized Value"])
        writer.writerow([intensity, quantized])

    thumb_path = os.path.splitext(image_path)[0] + ".thumb.png"
    thumbnail = cv2.resize(image, (128, 128))
    cv2.imwrite(thumb_path, thumbnail)

def save_all_result(log_base_dir, image, heatmap, intensity, quantized, series):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(log_base_dir, f"log_{timestamp}")
    os.makedirs(log_dir, exist_ok=True)

    cv2.imwrite(os.path.join(log_dir, "moire.png"), image)
    cv2.imwrite(os.path.join(log_dir, "heatmap.png"), heatmap)

    with open(os.path.join(log_dir, "metrics.csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Moire Intensity", "Quantized Value"])
        writer.writerow([intensity, quantized])

    xs = [p.x() for p in series.pointsVector()]
    ys = [p.y() for p in series.pointsVector()]
    plt.figure()
    plt.plot(xs, ys)
    plt.title("Moire Intensity History")
    plt.xlabel("Time")
    plt.ylabel("Intensity")
    plt.grid()
    plt.savefig(os.path.join(log_dir, "intensity_plot.png"))
    plt.close()
