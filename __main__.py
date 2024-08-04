import os
import subprocess
import sys
from speech_finder import SpeechFinder
from music_segments_finder import find as find_music_segments
from seconds_formatter import seconds_to_min_sec
from music_segments_finder import MusicSegment


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


def get_user_confirmation(question):
    return not input(f"{question} (Y/n): ").lower() == 'n'


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 __main__.py <path_to_mp3>")
        sys.exit(1)

    mp3_path = sys.argv[1]

    if not os.path.isfile(mp3_path):
        print(f"File not found: {mp3_path}")
        sys.exit(1)

    lines, total_length = SpeechFinder(mp3_path).find_segments()
    segments = find_music_segments(lines, total_length)

    while True:
        print_music_segments(segments)
        combined_segments = get_user_combined_segments(segments)
        print_music_segments(combined_segments)
        if get_user_confirmation("Selected segments okay?"):
            break

    if get_user_confirmation("Do you want to split the MP3 based on these segments?"):
        split_mp3(mp3_path, combined_segments)


if __name__ == "__main__":
    main()
