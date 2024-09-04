import warnings
from datetime import datetime

import easyocr

warnings.filterwarnings("ignore", category=FutureWarning)


def read_image(image_path: str) -> list[tuple]:
    # Initialize the EasyOCR reader with the Thai language
    reader = easyocr.Reader(["th"], gpu=True)
    # Read the text from the image
    results = reader.readtext(image_path)
    return results


def detect_date_month(results: list[tuple]) -> tuple[str | None, str | None]:
    # All possible variations of Thai months
    thai_months = [
        "ม.ค",
        "ก.พ",
        "มี.ค",
        "เม.ย",
        "พ.ค",
        "มิ.ย",
        "ก.ค",
        "ส.ค",
        "ก.ย",
        "ต.ค",
        "พ.ย",
        "ธ.ค",  # With 1 dot in mid
        "มค",
        "กพ",
        "มีค",
        "เมย",
        "พค",
        "มิย",
        "กค",
        "สค",
        "กย",
        "ตค",
        "พย",
        "ธค",  # Without dots
        "ม.ค.",
        "ก.พ.",
        "มี.ค.",
        "เม.ย.",
        "พ.ค.",
        "มิ.ย.",
        "ก.ค.",
        "ส.ค.",
        "ก.ย.",
        "ต.ค.",
        "พ.ย.",
        "ธ.ค.",  # With standard dots
        "มค.",
        "กพ.",
        "มีค.",
        "เมย.",
        "พค.",
        "มิย.",
        "กค.",
        "สค.",
        "กย.",
        "ตค.",
        "พย.",
        "ธค.",  # With 1 dot at the end
    ]

    detected_date = None
    detected_year = None

    for i, (_bbox, text, _prob) in enumerate(results):
        if any(month in text for month in thai_months):
            detected_date = text
            if i + 1 < len(results):
                next_text = results[i + 1][1]
                # Simple digit check and range validation
                if next_text.isdigit() and 2400 <= int(next_text) <= 2600:
                    detected_year = next_text
            break
    return detected_date, detected_year


def convert_to_datetime(
    detected_date: str | None, detected_year: str | None
) -> str | None:
    if detected_date and detected_year:
        try:
            full_date_str = f"{detected_date} {detected_year}"
            # Convert Thai year to Gregorian year
            gregorian_year = int(detected_year) - 543

            # Month translation dictionary
            month_translation = {
                "ม.ค": "Jan",
                "ก.พ": "Feb",
                "มี.ค": "Mar",
                "เม.ย": "Apr",
                "พ.ค": "May",
                "มิ.ย": "Jun",
                "ก.ค": "Jul",
                "ส.ค": "Aug",
                "ก.ย": "Sep",
                "ต.ค": "Oct",
                "พ.ย": "Nov",
                "ธ.ค": "Dec",  # With 1 dot in mid
                "มค": "Jan",
                "กพ": "Feb",
                "มีค": "Mar",
                "เมย": "Apr",
                "พค": "May",
                "มิย": "Jun",
                "กค": "Jul",
                "สค": "Aug",
                "กย": "Sep",
                "ตค": "Oct",
                "พย": "Nov",
                "ธค": "Dec",  # Without dots
                "ม.ค.": "Jan",
                "ก.พ.": "Feb",
                "มี.ค.": "Mar",
                "เม.ย.": "Apr",
                "พ.ค.": "May",
                "มิ.ย.": "Jun",
                "ก.ค.": "Jul",
                "ส.ค.": "Aug",
                "ก.ย.": "Sep",
                "ต.ค.": "Oct",
                "พ.ย.": "Nov",
                "ธ.ค.": "Dec",  # With standard dots
                "มค.": "Jan",
                "กพ.": "Feb",
                "มีค.": "Mar",
                "เมย.": "Apr",
                "พค.": "May",
                "มิย.": "Jun",
                "กค.": "Jul",
                "สค.": "Aug",
                "กย.": "Sep",
                "ตค.": "Oct",
                "พย.": "Nov",
                "ธค.": "Dec",  # With 1 dot at the end
            }

            # Replace Thai month abbreviation with English equivalent
            for thai_month, eng_month in month_translation.items():
                full_date_str = full_date_str.replace(thai_month, eng_month)


            # Replace the year in the date string
            full_date_str = full_date_str.replace(detected_year, str(gregorian_year))
            full_date_str = full_date_str.replace('.', '')


            # Parse the date
            parsed_date = datetime.strptime(full_date_str, "%d %b %Y")
            parsed_date = parsed_date.replace(hour=23, minute=59, second=59)

            return parsed_date
        except ValueError:
            return None
    else:
        return None
