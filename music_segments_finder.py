from music_segment import MusicSegment


def find(lines: list, total_length: float):
    segment_length_sec = int(lines[0])

    last_speech_begin = 0
    last_speech_end = 0
    last_speech = "..."

    segments = []
    for line in lines[1:]:
        first_word, speech = fetch_first_word_and_speech(line)

        if not speech:
            break

        speech_begin = int(first_word)
        if speech_begin > last_speech_end:
            segments.append(MusicSegment(last_speech_begin, last_speech, speech_begin + segment_length_sec, speech))

        last_speech_begin = speech_begin
        last_speech_end = speech_begin + segment_length_sec
        last_speech = speech

    speech_begin = total_length
    speech = "..."
    if speech_begin > last_speech_end:
        segments.append(MusicSegment(last_speech_begin, last_speech, speech_begin, speech))

    return segments


def fetch_first_word_and_speech(line: str):
    first_word = line.split(" ")[0]
    speech = line[len(first_word) + 1:]
    return first_word, speech
