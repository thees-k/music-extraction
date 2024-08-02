from music_segment import MusicSegment


def find(lines: list, total_length: float):
    segment_length_sec = int(lines[0])

    segments = []
    music_begin = 0
    last_speech = "..."

    for line in lines[1:]:
        first_word = line.split(" ")[0]
        speech_begin = int(first_word)
        speech = line[len(first_word) + 1:]

        if speech and speech_begin > music_begin + segment_length_sec:
            segments.append(MusicSegment(music_begin, last_speech, speech_begin + segment_length_sec, speech))

        if speech:
            last_speech = speech
            music_begin = speech_begin

    if int(total_length) > music_begin + segment_length_sec:
        segments.append(MusicSegment(music_begin, last_speech, total_length, "..."))

    return segments
