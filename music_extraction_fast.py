# music_extraction_fast.py
from pathlib import Path
import audio_tools
import sys
import subprocess
import tempfile
import os

if len(sys.argv) < 2:
    print("Missing argument: <audio file>")
    exit(1)

audio_file = Path(sys.argv[1])
if not audio_file.exists():
    print(f"File \"{audio_file}\" does not exist.")
    exit(1)

output_speech_file = audio_file.with_suffix('.speech')
if output_speech_file.exists():
    print(f"Output speech file '{output_speech_file.name}' already exists.")
    exit(0)

with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Use working directory {tmpdir}")
    print("Copy and then split audio file for analysis...")

    wav_file = audio_tools.create_analysable_audio(tmpdir, audio_file)
    total_length = audio_tools.get_total_length_of_audio(wav_file)
    extraction_length = 300

    for start in range(0, int(total_length), extraction_length):
        end = min(start + extraction_length * 1.0, total_length)
        audio_tools.split_audio(wav_file, start, end, f"{tmpdir}/{start:06d}", ".wav")

    wav_file.unlink()

    print("Audio analysis...")
    venv_python = Path(__file__).parent / '.venv' / 'bin' / 'python3'
    main_py_path = Path(__file__).parent / '__main__.py'
    merge_script = Path(__file__).parent / 'merge_speech_files.sh'
    try:
        subprocess.run(
            f'find . -maxdepth 1 -type f -iname "*.wav" -print0 | xargs -0 -n 1 -P $(nproc) -- "{venv_python}" "{main_py_path}" -a -s',
            shell=True, check=True, cwd=tmpdir
        )
        subprocess.run(
            f'"{merge_script}" "{output_speech_file.resolve()}"',
            shell=True, check=True, cwd=tmpdir
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing commands: {e}")
        exit(1)