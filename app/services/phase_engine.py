from datetime import date


def determine_current_phase(cycles, pattern_data):
    """
    Determines current menstrual phase safely.
    """

    # Defensive: ensure cycles is list
    if not isinstance(cycles, list) or not cycles:
        return {
            "current_phase": "unknown",
            "phase_day": None,
            "phase_stability": "insufficient_data"
        }

    last_cycle = cycles[-1]

    if not hasattr(last_cycle, "start_date") or not last_cycle.start_date:
        return {
            "current_phase": "unknown",
            "phase_day": None,
            "phase_stability": "insufficient_data"
        }

    today = date.today()
    cycle_day = (today - last_cycle.start_date).days + 1

    avg_length = pattern_data.get("average_cycle_length") or 28

    # Phase boundaries
    if cycle_day <= 5:
        phase = "menstrual"
    elif cycle_day <= avg_length / 2:
        phase = "follicular"
    elif cycle_day <= avg_length - 14:
        phase = "ovulatory"
    else:
        phase = "luteal"

    return {
        "current_phase": phase,
        "phase_day": cycle_day,
        "phase_stability": "normal"
    }