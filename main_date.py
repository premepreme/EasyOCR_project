from datetime import datetime

from readdate import convert_to_datetime, detect_date_month, read_image


def main(image_path: str) -> datetime | None:
    results = read_image(image_path)

    detected_date, detected_year = detect_date_month(results)


    parsed_date = convert_to_datetime(detected_date, detected_year)


    if parsed_date:
        return parsed_date
    else:
        return None


if __name__ == "__main__":
    result = main(
        "example.png"
    )
    print(result)
