from readfile import load_image, preprocess_image, detect_registration_number, extract_number_from_result

def main(image_path):
    image = load_image(image_path)
    gray_image = preprocess_image(image)

    # Detect registration number and crop image
    cropped_image, result = detect_registration_number(gray_image) # Return the cropped image and text of crop image

    if cropped_image is not None and result is not None: # if found Vehicle registration number
        # Extract registration number from the result
        reg_number = extract_number_from_result(result)
        if reg_number:
            return(reg_number)
        else:
            return cropped_image # if not found return cropped image
    else:
        return cropped_image # if not found return cropped image

if __name__ == "__main__":
    result = main('example.png')
    print(result)