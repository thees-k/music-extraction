from music_segment import MusicSegment
from music_segments_finder import find as find_music_segments


def find(lines: list, total_length: float):
    segment_length_sec = int(lines[0])

    segments = []
    last_segment = None

    for segment in find_music_segments(lines, total_length):
        if last_segment:
            segments.append(create_music_speech_segment(last_segment, segment, segment_length_sec))
        last_segment = segment

    if last_segment:
        if last_segment.end_seconds < total_length:
            segments.append(MusicSegment(last_segment.begin_seconds, last_segment.speech_before, total_length, "..."))
        else:
            segments.append(last_segment)

    return segments


def create_music_speech_segment(music_segment: MusicSegment, next_music_segment: MusicSegment, segment_length_sec: int) -> MusicSegment:
    return MusicSegment(music_segment.begin_seconds, music_segment.speech_before, next_music_segment.begin_seconds + segment_length_sec, next_music_segment.speech_before)

