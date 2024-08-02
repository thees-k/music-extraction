from math import isclose


class MusicSegment:
    def __init__(self, begin_seconds: int, speech_before: str, end_seconds: float, speech_after: str):
        self.begin_seconds = begin_seconds
        self.speech_before = speech_before
        self.end_seconds = end_seconds
        self.speech_after = speech_after

    def __repr__(self):
        duration = self.end_seconds - self.begin_seconds
        return (f"{seconds_to_min_sec(self.begin_seconds)} {self.speech_before}\n"
                f"{seconds_to_min_sec(self.end_seconds)} {self.speech_after}\n"
                f"{seconds_to_min_sec(duration)}")

    def __eq__(self, other):
        return (self.begin_seconds == other.begin_seconds and
                self.speech_before == other.speech_before and
                isclose(self.end_seconds, other.end_seconds, abs_tol=0.01) and
                self.speech_after == other.speech_after)


def seconds_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02}"
