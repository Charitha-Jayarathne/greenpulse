from datetime import datetime


# --------------------------------------------------
# AI Schedule
# --------------------------------------------------

MORNING_START_HOUR = 8
MORNING_END_HOUR = 9

EVENING_START_HOUR = 20
EVENING_END_HOUR = 21


# --------------------------------------------------
# Store today's AI request information
# --------------------------------------------------

ai_request_date = None
morning_request_done = False
evening_request_done = False


# --------------------------------------------------
# Check whether AI advice can be generated
# --------------------------------------------------

def can_generate_ai_advice():

    global ai_request_date
    global morning_request_done
    global evening_request_done

    now = datetime.now()

    today = now.date()
    current_hour = now.hour

    # --------------------------------------------------
    # Reset schedule when a new day starts
    # --------------------------------------------------

    if ai_request_date != today:

        ai_request_date = today

        morning_request_done = False
        evening_request_done = False


    # --------------------------------------------------
    # Morning AI window
    # --------------------------------------------------

    if MORNING_START_HOUR <= current_hour < MORNING_END_HOUR:

        if not morning_request_done:
            return True


    # --------------------------------------------------
    # Evening AI window
    # --------------------------------------------------

    if EVENING_START_HOUR <= current_hour < EVENING_END_HOUR:

        if not evening_request_done:
            return True


    # --------------------------------------------------
    # No AI request currently allowed
    # --------------------------------------------------

    return False


# --------------------------------------------------
# Record an AI request
# --------------------------------------------------

def record_ai_request():

    global ai_request_date
    global morning_request_done
    global evening_request_done

    now = datetime.now()

    today = now.date()
    current_hour = now.hour


    # --------------------------------------------------
    # Reset schedule when a new day starts
    # --------------------------------------------------

    if ai_request_date != today:

        ai_request_date = today

        morning_request_done = False
        evening_request_done = False


    # --------------------------------------------------
    # Record morning request
    # --------------------------------------------------

    if MORNING_START_HOUR <= current_hour < MORNING_END_HOUR:

        morning_request_done = True


    # --------------------------------------------------
    # Record evening request
    # --------------------------------------------------

    elif EVENING_START_HOUR <= current_hour < EVENING_END_HOUR:

        evening_request_done = True


# --------------------------------------------------
# Get today's AI request count
# --------------------------------------------------

def get_ai_request_count():

    global ai_request_date
    global morning_request_done
    global evening_request_done

    today = datetime.now().date()

    if ai_request_date != today:

        ai_request_date = today

        morning_request_done = False
        evening_request_done = False


    count = 0

    if morning_request_done:
        count += 1

    if evening_request_done:
        count += 1


    return count