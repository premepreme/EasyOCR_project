import numpy as np

from readfile import (
    detect_registration_number,
    extract_number_from_result,
    load_image,
    preprocess_image,
)


def main(image_path: str) -> str | np.ndarray | None:
    image = load_image(image_path)
    gray_image = preprocess_image(image)

    # Detect registration number and crop image
    cropped_image, result = detect_registration_number(
        gray_image
    )  # Return the cropped image and text of the cropped image

    if cropped_image is not None and result is not None:
        # Extract registration number from the result
        reg_number = extract_number_from_result(result)
        if reg_number:
            return reg_number
        else:
            return cropped_image  # If not found, return cropped image
    else:
        return cropped_image  # If not found, return cropped image


if __name__ == "__main__":
    result = main("example.png")
    print(result)
