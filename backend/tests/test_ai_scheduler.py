from unittest.mock import patch
from datetime import datetime

from app.ai_scheduler import (
    can_generate_ai_advice,
    record_ai_request,
    get_ai_request_count
)


print("\nGreenPulse AI Scheduler Test")
print("--------------------------")


# --------------------------------------------------
# Test Morning AI Window
# --------------------------------------------------

morning_time = datetime(
    2026, 10, 3, 8, 15
)


with patch(
    "app.ai_scheduler.datetime"
) as mock_datetime:

    mock_datetime.now.return_value = morning_time

    print("\nMorning AI Window")
    print("--------------------------")

    print(
        "AI Request Allowed:",
        can_generate_ai_advice()
    )

    record_ai_request()

    print(
        "AI Request Count:",
        get_ai_request_count()
    )

    print(
        "Second Morning Request Allowed:",
        can_generate_ai_advice()
    )


# --------------------------------------------------
# Test Evening AI Window
# --------------------------------------------------

evening_time = datetime(
    2026, 10, 3, 20, 15
)


with patch(
    "app.ai_scheduler.datetime"
) as mock_datetime:

    mock_datetime.now.return_value = evening_time

    print("\nEvening AI Window")
    print("--------------------------")

    print(
        "AI Request Allowed:",
        can_generate_ai_advice()
    )

    record_ai_request()

    print(
        "AI Request Count:",
        get_ai_request_count()
    )

    print(
        "Second Evening Request Allowed:",
        can_generate_ai_advice()
    )