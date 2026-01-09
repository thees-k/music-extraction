# music_extraction_fast.py
from pathlib import Path
import audio_tools
import sys
import subprocess
import shutil


if len(sys.argv) == 1:
    print("Missing argument: <audio file>")
    exit(1)

file_name = sys.argv[1]
audio_file = Path(file_name)
if not audio_file.exists():
    print(f"File \"{file_name}\" does not exist.")
    exit(1)

file_name = audio_file.name

target_directory = Path(str(audio_file.parent) + "/tmp_speech")

try:
    target_directory.mkdir()
    print(f"Directory '{target_directory}' created.")
except FileExistsError:
    print(f"Directory '{target_directory}' already exists.")
    exit(0)
except PermissionError:
    print(f"Permission denied: Unable to create '{target_directory}'.")
    exit(0)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(0)

wav_file = audio_tools.create_analysable_audio(str(target_directory), audio_file)

total_length = audio_tools.get_total_length_of_audio(wav_file)

extraction_length = 300

start = 0
while start < total_length:
    audio_tools.split_audio(wav_file, start, min(start + extraction_length *1.0, total_length), f"{str(target_directory)}/{start:06d}", ".wav")
    start += extraction_length

wav_file.unlink()

print("Audio analysis is being performed.")
try:
    subprocess.run(
        'find . -maxdepth 1 -type f -iname "*.wav" -print0 | xargs -0 -n 1 -P $(nproc) -- music_extraction.sh -a -s',
        shell=True, check=True, cwd=target_directory
    )
    output_speech_file = audio_file.with_suffix('.speech').name
    subprocess.run(
        f'merge_speech_files.sh "../{output_speech_file}"',
        shell=True, check=True, cwd=target_directory
    )
except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing commands: {e}")
    exit(1)

# Delete the target_directory after processing
try:
    shutil.rmtree(target_directory)
    print(f"Deleted temporary directory '{target_directory}'.")
except Exception as e:
    print(f"Failed to delete temporary directory '{target_directory}': {e}")