from unittest.mock import patch

from app.ai_scheduler import (
    can_generate_ai_advice,
    record_ai_request,
    get_ai_request_count
)


print("\nGreenPulse MQTT AI Schedule Test")
print("--------------------------")


# --------------------------------------------------
# Simulate morning AI window
# --------------------------------------------------

with patch("app.ai_scheduler.datetime") as mock_datetime:

    mock_datetime.now.return_value.hour = 8
    mock_datetime.now.return_value.date.return_value = "2026-10-03"

    # First AI request
    allowed = can_generate_ai_advice()

    print("\nMorning AI Window")
    print("--------------------------")

    print(f"AI Request Allowed: {allowed}")

    if allowed:
        record_ai_request()

    print(
        f"AI Request Count: "
        f"{get_ai_request_count()}"
    )


    # Second request
    second_allowed = can_generate_ai_advice()

    print(
        f"Second Morning Request Allowed: "
        f"{second_allowed}"
    )


print("\nScheduled AI test completed.")