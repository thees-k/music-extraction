
def seconds_to_min_sec(seconds):
    full_seconds = int(seconds)
    millis = seconds - full_seconds
    minutes = full_seconds // 60
    remaining_seconds = full_seconds % 60
    if millis:
        return f"{minutes}:{remaining_seconds:02}.{int(millis * 1000)}"
    else:
        return f"{minutes}:{remaining_seconds:02}"
