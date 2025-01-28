# music_extraction_fast.py
from pathlib import Path
import audio_tools
import sys


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
    exit(1)
except PermissionError:
    print(f"Permission denied: Unable to create '{target_directory}'.")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

wav_file = audio_tools.create_analysable_audio(str(target_directory), audio_file)

total_length = audio_tools.get_total_length_of_audio(wav_file)

extraction_length = 300

start = 0
while start < total_length:
    audio_tools.split_audio(wav_file, start, min (start + extraction_length, total_length), f"{str(target_directory)}/{start:06d}", ".wav")
    start += extraction_length

wav_file.unlink()

#
#  Inside "target_directory" execute:
#
#  find . -maxdepth 1 -type f -iname \*.wav -print0 | xargs -0 -n 1 -P $(nproc) music_extraction.sh -a -s
#  merge_speech_files.sh result.speech
#

message = f"""
Now go into folder "{str(target_directory)}" and execute:

find . -maxdepth 1 -type f -iname \\*.wav -print0 | xargs -0 -n 1 -P $(nproc) music_extraction.sh -a -s
merge_speech_files.sh "../{audio_file.with_suffix('.speech').name}"
"""
print(message)
