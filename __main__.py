import os
import subprocess
import sys
from pathlib import Path
from pydub import AudioSegment

import speech_finder
from speech_finder import build_analyze_file_path, AnalyzeFileStatus, check_file, SpeechFinder


def find_music_segments(lines, total_length):
    segment_length_sec = int(lines[0].strip())

    segments = []
    music_begin = 0
    last_speech = "..."

    for line in lines[1:]:
        first_word = line.split(" ")[0]
        print(f"first_word '{first_word}'")
        speech_begin = int(first_word)
        speech = line[len(first_word) + 1:].strip()

        if speech and speech_begin > music_begin + segment_length_sec:
            segments.append(MusicSegment(music_begin, last_speech, speech_begin + segment_length_sec, speech))

        if speech:
            last_speech = speech
            music_begin = speech_begin

    if int(total_length) > music_begin + segment_length_sec:
        segments.append(MusicSegment(music_begin, last_speech, total_length, "..."))

    return segments


class MusicSegment:
    def __init__(self, begin_seconds, speech_before, end_seconds, speech_after):
        self.begin_seconds = begin_seconds
        self.speech_before = speech_before
        self.end_seconds = end_seconds
        self.speech_after = speech_after

    def __str__(self):
        duration = self.end_seconds - self.begin_seconds
        return (f"{seconds_to_min_sec(self.begin_seconds)} {self.speech_before}\n"
                f"{seconds_to_min_sec(self.end_seconds)} {self.speech_after}\n"
                f"{seconds_to_min_sec(duration)}")


def seconds_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02}"


def print_music_segments(segments):
    print("\nMusic segments:")
    for no, segment in enumerate(segments, start=1):
        print(f"{no})")
        print(segment)
        print()


def merge_segments(segments, from_no, to_no):
    return MusicSegment(segments[from_no - 1].begin_seconds, segments[from_no - 1].speech_before,
                        segments[to_no - 1].end_seconds, segments[to_no - 1].speech_after)


def get_user_input_segments_to_keep():
    user_input = input("Enter the segments to keep (e.g., 1,2-3,6) or press the Enter key to keep all: ")
    return "".join(user_input.split())


def parse_user_input(user_input):
    segments_to_keep = []
    parts = user_input.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            segments_to_keep.append((start, end))
        else:
            segments_to_keep.append((int(part), int(part)))
    return segments_to_keep


def combine_segments(segments, segments_to_keep):
    combined_segments = []
    for start, end in segments_to_keep:
        combined_segment = merge_segments(segments, start, end)
        combined_segments.append(combined_segment)
    return combined_segments


def get_user_confirmation():
    return not input("Selected segments okay? (Y/n): ").lower() == 'n'


def split_mp3(mp3_path, segments):
    for i, segment in enumerate(segments, start=1):
        start, end = segment.begin_seconds, segment.end_seconds
        output_path = f"output_segment_{i:02d}.mp3"  # Format the output filename with leading zeros
        command = f'ffmpeg -loglevel error -ss {start} -to {end} -i "{mp3_path}" -c copy "{output_path}"'
        subprocess.call(command, shell=True)
        print(f"Exported segment {i} from {seconds_to_min_sec(start)} to {seconds_to_min_sec(end)} to {output_path}")


def get_user_combined_segments(segments):
    user_input = get_user_input_segments_to_keep()
    if user_input == "":
        return segments
    else:
        segments_to_keep = parse_user_input(user_input)
        return combine_segments(segments, segments_to_keep)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 __main__.py <path_to_mp3>")
        sys.exit(1)

    mp3_path = sys.argv[1]

    if not os.path.isfile(mp3_path):
        print(f"File not found: {mp3_path}")
        sys.exit(1)

    analyze_file = build_analyze_file_path(Path(mp3_path))
    total_length = AudioSegment.from_mp3(mp3_path).duration_seconds

    status = check_file(analyze_file)
    if status is not AnalyzeFileStatus.FILE_OK:
        SpeechFinder(mp3_path).find_segments()
    with open(analyze_file, 'r') as file:
        lines = [line for line in file.readlines() if line.strip()]

    segments = find_music_segments(lines, total_length)

    while True:
        print_music_segments(segments)
        combined_segments = get_user_combined_segments(segments)
        print_music_segments(combined_segments)
        if get_user_confirmation():
            break

    if not input("Do you want to split the MP3 based on these segments? (Y/n): ").lower() == 'n':
        split_mp3(mp3_path, combined_segments)


if __name__ == "__main__":
    main()
