from datetime import datetime


def analyze_cycle_patterns(cycles):
    """
    Analyze cycle consistency and variability.
    Returns structured pattern insights.
    """

    if not cycles or len(cycles) < 3:
        return {
            "average_cycle_length": None,
            "cycle_variability_days": None,
            "irregular": False
        }

    lengths = []

    for i in range(1, len(cycles)):
        delta = (cycles[i].start_date - cycles[i - 1].start_date).days
        lengths.append(delta)

    if not lengths:
        return {
            "average_cycle_length": None,
            "cycle_variability_days": None,
            "irregular": False
        }

    avg_length = sum(lengths) / len(lengths)
    variability = max(lengths) - min(lengths)

    return {
        "average_cycle_length": round(avg_length, 1),
        "cycle_variability_days": variability,
        "irregular": variability > 7  # more than 7 days difference = irregular
    }