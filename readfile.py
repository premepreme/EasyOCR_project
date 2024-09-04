import re
import warnings

import cv2
import easyocr
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)


def load_image(image_path: str) -> np.ndarray | None:
    # Load the image
    image = cv2.imread(image_path)
    return image


def preprocess_image(image: np.ndarray) -> np.ndarray:
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def detect_registration_number(
    image: np.ndarray,
) -> tuple[np.ndarray | None, list[tuple] | None]:
    # Easyocr Reader with Thai language and Cropping
    reader = easyocr.Reader(["th"])
    result = reader.readtext(image)

    # Loop through the detected text
    for bbox, text, _prob in result:
        if "เลขทะเบียน" in text:
            # Crop the image using the bounding box coordinates
            (x_min, y_min), (x_max, y_max) = bbox[0], bbox[2]
            cropped_roi = image[y_min - 50 : y_max + 100, x_min - 50 : x_max + 250]
            return cropped_roi, reader.readtext(cropped_roi)
            # Reread the image
    return None, None


def extract_number_from_result(result: list[tuple] | None) -> str | None:
    # Find the Vehicle registration number in the result from cropped image
    pattern = r"\d{2,3}-\d{4}"
    if result:
        for _bbox, text, _prob in result:
            match = re.search(pattern, text)
            if match:
                reg_number = match.group(0)
                return reg_number
    return None
