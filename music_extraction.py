import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from audio_trimmer import AudioTrimmer
from speech_finder import SpeechFinder
from music_segments_finder import find as find_music_segments
from seconds_formatter import seconds_to_min_sec
from music_segments_finder import MusicSegment
import re


"""
Extracts music parts from an audio file (e.g. a radio recording)
"""


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


def split_audio(audio_path, segments):
    file_extension = os.path.splitext(audio_path)[1]
    for no, segment in enumerate(segments, start=1):
        start, end = segment.begin_seconds, segment.end_seconds
        output_path = f'{no:02d}_{extraction_name}{file_extension}'
        duration = end - start
        command = create_ffmpeg_split_command(file_extension, audio_path, output_path, start, duration)
        subprocess.call(command, shell=True)
        # TODO dont hardcode 25.0
        audio_trimmer = AudioTrimmer(Path(output_path), 25.0, with_backup = True)
        audio_trimmer.trim()
        print(f"Exported {output_path} from ~{seconds_to_min_sec(start)} to ~{seconds_to_min_sec(end)} "
              f"({seconds_to_min_sec(audio_trimmer.trimmed_length)})")


def create_ffmpeg_split_command(file_extension, audio_path, output_path, start, duration):
    if file_extension.lower() in [".flac", ".wav"]:
        return f'ffmpeg -loglevel error -i "{audio_path}" -ss {start} -t {duration} "{output_path}"'
    else:
        return f'ffmpeg -loglevel error -ss {start} -i "{audio_path}" -t {duration} -c copy "{output_path}"'


def get_user_combined_segments(segments):
    user_input = get_user_input_segments_to_keep()
    if user_input == "":
        return segments
    else:
        segments_to_keep = parse_user_input(user_input)
        return combine_segments(segments, segments_to_keep)


def get_user_confirmation(question):
    return not input(f"{question} (Y/n): ").lower() == 'n'


def init_argument_parser() -> Namespace:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('audio_file', metavar='audio file', type=str,
                        help='The audio file that should be analysed / where music parts should be extracted from')

    # Option without argument (a flag!):
    parser.add_argument('-a', '--analyse', action='store_true',
                        help='If set, the audio file will be analysed only (for later faster extraction)')

    return parser.parse_args()


def sanitize_filename(name):
    """
    Remove or replace invalid filename characters.
    """
    # Use regex to replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def get_user_input_extraction_name():
    user_input = input(f'Specify a name for the extraction segments or press the Enter key for default naming'
                       f' ("{extraction_name}"): ')
    sanitized_input = sanitize_filename(user_input.strip())
    return sanitized_input if sanitized_input != "" else extraction_name


extraction_name = "extraction"


def main():
    args = init_argument_parser()

    audio_path = args.audio_file
    if not os.path.isfile(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)

    lines, total_length = SpeechFinder(audio_path).find_segments()

    if not args.analyse:
        segments = find_music_segments(lines, total_length)
        while True:
            print_music_segments(segments)
            combined_segments = get_user_combined_segments(segments)
            print_music_segments(combined_segments)
            if get_user_confirmation("Selected segments okay?"):
                break
        global extraction_name
        extraction_name = get_user_input_extraction_name()
        split_audio(audio_path, combined_segments)


if __name__ == "__main__":
    main()
