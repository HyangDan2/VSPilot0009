
import numpy as np
import cv2

def generate_pattern_image(freq, angle, size):
    x = np.linspace(0, 2 * np.pi * freq, size)
    y = np.sin(x)
    pattern = np.tile(y, (size, 1))
    pattern = ((pattern + 1) / 2 * 255).astype(np.uint8)

    M = cv2.getRotationMatrix2D((size // 2, size // 2), angle, 1)
    rotated = cv2.warpAffine(pattern, M, (size, size))
    return rotated

def calculate_moire_intensity(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.abs(fshift)
    energy = np.sum(magnitude ** 2)
    norm_energy = energy / (image.shape[0] * image.shape[1])
    return norm_energy ** 0.5

def quantize_intensity(intensity, levels=10):
    return min(int(intensity / 255 * levels), levels)

def generate_heatmap(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.log(np.abs(fshift) + 1)
    mag_norm = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heatmap = cv2.applyColorMap(mag_norm, cv2.COLORMAP_JET)
    return heatmap
