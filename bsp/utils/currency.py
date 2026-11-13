def indian_currency_commas(number):
    """
    Format a number using the Indian currency numbering system (e.g., 1,50,000).
    """
    number = int(round(number))
    num_str = str(number)
    if len(num_str) <= 3:
        return num_str
    
    last_three = num_str[-3:]
    remaining = num_str[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    return ','.join(parts) + ',' + last_three


def format_indian_currency(number):
    """
    Returns currency string prefixed with Indian Rupee symbol (₹).
    """
    formatted = indian_currency_commas(number)
    return f"₹{formatted}"

