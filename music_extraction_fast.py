# music_extraction_fast.py
from pathlib import Path
import audio_tools
import sys
import subprocess
import tempfile


if len(sys.argv) == 1:
    print("Missing argument: <audio file>")
    exit(1)

file_name = sys.argv[1]
audio_file = Path(file_name)
if not audio_file.exists():
    print(f"File \"{file_name}\" does not exist.")
    exit(1)

audio_file_directory_string = audio_file.parent.resolve().as_posix()

file_name = audio_file.name
output_speech_file_path = audio_file.with_suffix('.speech')

if output_speech_file_path.exists():
    print(f"Output speech file '{output_speech_file_path.name}' already exists.")
    exit(0)

with tempfile.TemporaryDirectory() as target_directory:

    print(f"Use working directory {target_directory}")

    print("Copy and then split audio file for analysis...")

    wav_file = audio_tools.create_analysable_audio(target_directory, audio_file)

    total_length = audio_tools.get_total_length_of_audio(wav_file)

    extraction_length = 300

    start = 0
    while start < total_length:
        audio_tools.split_audio(wav_file, start, min(start + extraction_length *1.0, total_length), f"{target_directory}/{start:06d}", ".wav")
        start += extraction_length

    wav_file.unlink()

    print("Audio analysis...")
    try:
        subprocess.run(
            'find . -maxdepth 1 -type f -iname "*.wav" -print0 | xargs -0 -n 1 -P $(nproc) -- music_extraction.sh -a -s',
            shell=True, check=True, cwd=target_directory
        )
        subprocess.run(
            f'merge_speech_files.sh "{audio_file_directory_string}/{output_speech_file_path.name}"',
            shell=True, check=True, cwd=target_directory
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing commands: {e}")
        exit(1)

