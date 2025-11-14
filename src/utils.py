import re
from datetime import datetime

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

def get_cur_datetime():
    # Current date and time
    now = datetime.now()

    # Format as string
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def format_vnd(val):
    try:
        # Step 1: Ensure it is a number (handle strings like "20.0")
        num = float(val)

        # Step 2: Logic check based on your example
        # 20.0 -> 20.000 implies input is in 'thousands' unit
        real_value = num * 1000

        # Step 3: Format with standard commas (2,000,000)
        # {:,.0f} means: use commas, 0 decimal places
        s = "{:,.0f}".format(real_value)

        # Step 4: Swap commas (US) to dots (VN)
        return f"{s.replace(',', '.')} VND"

    except (ValueError, TypeError):
        # Return original if it's text (e.g., "N/A")
        return val

def clean_decimal(val):
    """
    Convert a value to a number if possible:
    - If whole number, return int
    - If float, return float
    - If string that cannot be converted, return as-is
    """
    try:
        # Convert string with comma as decimal separator
        if isinstance(val, str):
            val = val.replace(',', '.')  # "20,5" -> "20.5"
        num = float(val)

        # If it's a whole number, return int
        if num.is_integer():
            return int(num)
        return num
    except (ValueError, TypeError):
        # If it cannot be converted, return original
        return val