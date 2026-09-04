import re
from datetime import datetime


def validate_passport_data(data):
    """
    Validate extracted passport data.

    Expected fields:
    - name
    - passport_number
    - date_of_birth
    - expiry_date
    """

    issues = []

    # Required fields
    required_fields = [
        "name",
        "passport_number",
        "date_of_birth",
        "expiry_date"
    ]

    for field in required_fields:
        value = data.get(field)

        if not value or not str(value).strip():
            issues.append(f"Missing required field: {field}")

    # Passport number format
    passport_number = data.get("passport_number")

    if passport_number:
        passport_number = str(passport_number).strip().upper()

        # Basic passport-number check:
        # 1-2 letters followed by 6-8 digits
        if not re.fullmatch(r"[A-Z]{1,2}[0-9]{6,8}", passport_number):
            issues.append("Invalid passport number format")

    # Date validation helper
    def check_date(field_name):
        value = data.get(field_name)

        if not value:
            return None

        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except ValueError:
            issues.append(
                f"Invalid date format for {field_name}; expected YYYY-MM-DD"
            )
            return None

    date_of_birth = check_date("date_of_birth")
    expiry_date = check_date("expiry_date")

    # Date of birth should not be in the future
    today = datetime.now().date()

    if date_of_birth and date_of_birth > today:
        issues.append("Date of birth cannot be in the future")

    # Passport must not be expired
    if expiry_date and expiry_date < today:
        issues.append("Passport has expired")

    valid = len(issues) == 0

    return {
        "valid": valid,
        "issues": issues
    }