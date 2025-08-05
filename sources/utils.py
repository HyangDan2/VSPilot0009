
import numpy as np
import cv2

def generate_pattern_image(freq1, angle1, freq2, angle2, size):
    """
    정현파 기반 Moiré 간섭 이미지 생성 함수
    (기존 함수 구조 유지, 내부는 과학적 모델로 교체)
    """
    import numpy as np

    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)

    theta1 = np.deg2rad(angle1)
    theta2 = np.deg2rad(angle2)

    # 첫 번째 패턴
    pattern1 = np.sin(2 * np.pi * freq1 * (X * np.cos(theta1) + Y * np.sin(theta1)) / size)

    # 두 번째 패턴
    pattern2 = np.sin(2 * np.pi * freq2 * (X * np.cos(theta2) + Y * np.sin(theta2)) / size)

    # 파형 간섭
    moire = (pattern1 + pattern2) / 2

    # 0~255 정규화
    moire_normalized = ((moire + 1) / 2 * 255).astype(np.uint8)

    return moire_normalized

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
    mag_norm = np.zeros_like(magnitude, dtype=np.float32)
    cv2.normalize(magnitude, mag_norm, 0, 255, cv2.NORM_MINMAX)
    mag_norm = mag_norm.astype(np.uint8)
    heatmap = cv2.applyColorMap(mag_norm, cv2.COLORMAP_JET)
    return heatmap
