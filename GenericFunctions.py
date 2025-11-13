from datetime import datetime

def parse_date(date_str: str) -> datetime.date:
    """Parse a date string in MM/DD/YY format into a datetime.date.
    Example: '11/13/25' -> datetime.date(2025, 11, 13)"""
    return datetime.strptime(date_str, '%m/%d/%y').date()


