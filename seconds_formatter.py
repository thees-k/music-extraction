
def seconds_to_min_sec(seconds):
    full_seconds = int(seconds)
    millis = round((seconds - full_seconds) * 1000)
    minutes = full_seconds // 60
    remaining_seconds = full_seconds % 60
    if millis:
        return f"{minutes}:{remaining_seconds:02}.{millis:03}"
    else:
        return f"{minutes}:{remaining_seconds:02}"
