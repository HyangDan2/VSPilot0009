
import numpy as np
import cv2

import numpy as np

def generate_pattern_image(params: dict, size):
    """
    다양한 파형 기반 Moiré 간섭 이미지 생성 함수
    Supports: sin, square, triangle, checker
    """
    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)

    theta1 = np.deg2rad(params.get('angle1', 0))
    theta2 = np.deg2rad(params.get('angle2', 0))

    freq1 = params.get('freq1', 11)
    freq2 = params.get('freq2', 10)

    type1 = params.get('pattern_type1', 'sin')
    type2 = params.get('pattern_type2', 'sin')

    def base_pattern(freq, theta, ptype):
        Xr = X * np.cos(theta) + Y * np.sin(theta)
        Yr = -X * np.sin(theta) + Y * np.cos(theta)
        wave = 2 * np.pi * freq * Xr / size

        if ptype == "sin":
            return np.sin(wave)
        elif ptype == "square":
            return np.sign(np.sin(wave))
        elif ptype == "triangle":
            return 2 * np.abs(2 * (wave / (2*np.pi) % 1) - 1) - 1
        elif ptype == "checker":
            checks = ((np.floor(freq * Xr / size) + np.floor(freq * Yr / size)) % 2)
            return checks * 2 - 1  # normalize to [-1, 1]
        elif ptype == "sawtooth":
            return 2 * ((wave / (2*np.pi)) % 1) - 1
        else:
            raise ValueError(f"Unsupported pattern type: {ptype}")

    pattern1 = base_pattern(freq1, theta1, type1)
    pattern2 = base_pattern(freq2, theta2, type2)

    moire = (pattern1 + pattern2) / 2
    normalized = ((moire + 1) / 2 * 255).astype(np.uint8)
    return normalized


def calculate_moire_intensity(image: np.ndarray) -> float:
    """
    이미지의 Moiré 강도(에너지 루트 값)를 계산

    Args:
        image (np.ndarray): 그레이스케일 이미지 (2D)

    Returns:
        float: 정규화된 Moiré 강도
    """
    assert image.ndim == 2, "Input must be a 2D grayscale image."

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.abs(fshift)

    # 전체 주파수 영역 에너지
    energy = np.sum(magnitude ** 2)
    norm_energy = energy / (image.shape[0] * image.shape[1])

    return np.sqrt(norm_energy)


def quantize_intensity(intensity: float, levels: int = 10) -> int:
    """
    Moiré 강도를 0~levels 구간으로 정량화

    Args:
        intensity (float): 계산된 강도 값
        levels (int): quantization 구간 수 (기본 10)

    Returns:
        int: 0 ~ levels 정수값
    """
    q = int(intensity / 255 * levels)
    return int(np.clip(q, 0, levels))


def generate_heatmap(image: np.ndarray) -> np.ndarray:
    """
    FFT 기반 Heatmap 생성 (Color Map 적용)

    Args:
        image (np.ndarray): 그레이스케일 이미지 (2D)

    Returns:
        np.ndarray: 컬러 heatmap (BGR)
    """
    assert image.ndim == 2, "Input must be a 2D grayscale image."

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude = np.log(np.abs(fshift) + 1)

    # 정규화 (0 ~ 255)
    mag_norm = cv2.normalize(magnitude, np.zeros_like(magnitude, dtype=np.float32), 0, 255, cv2.NORM_MINMAX)
    mag_norm = mag_norm.astype(np.uint8)

    heatmap = cv2.applyColorMap(mag_norm, cv2.COLORMAP_JET)
    return heatmap