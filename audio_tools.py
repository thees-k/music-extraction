import logging
import os
import subprocess
from pathlib import Path
from pydub import AudioSegment
import shutil


def extract_segment(wav_path: Path, start_time: int, duration: int, segment_name="temp_segment.wav"):
    """
    Extract a segment from the WAV audio file.

    Args:
        wav_path (Path): Path to the input WAV file.
        start_time (int): Start time of the segment in seconds.
        duration (int): Duration of the segment in seconds.
        segment_name (str): The output segment file.
    """
    segment_path = wav_path.parent / segment_name
    command = f'ffmpeg -loglevel error -ss {start_time} -t {duration} -i "{wav_path}" "{segment_path}"'
    result = subprocess.call(command, shell=True)
    if result != 0:
        logging.error(f"Failed to extract segment from {wav_path}")
        raise RuntimeError(f"ffmpeg segment extraction failed for {wav_path}")
    return segment_path


def create_analysable_audio(temp_dir: str, audio_path: Path, wav_name="temp_audio.wav") -> Path:
    wav_path = Path(os.path.join(temp_dir, wav_name))
    try:
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)

        # Check if the audio is already a mono WAV with frame rate 16000
        if (
            audio.frame_rate == 16000 and
            audio.channels == 1 and
            audio_path.suffix.lower() == ".wav"
        ):
            # Copy the file directly
            shutil.copy(audio_path, wav_path)
            logging.info(f"Copied {audio_path} to {wav_path} as it already meets the requirements.")
        else:
            # Convert the audio to mono WAV with frame rate 16000
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_path, format="wav")
            logging.info(f"Converted {audio_path} to {wav_path}")
    except Exception as e:
        logging.error(f"Failed to process {audio_path}: {e}")
        raise RuntimeError(f"Failed to process {audio_path}")

    return wav_path


def get_total_length_of_audio(audio_path: Path) -> float:
    """
    Get the total length of an audio file in seconds using ffprobe.

    Args:
        audio_path (Path): Path to the audio file.

    Returns:
        float: Total length of the audio file in seconds.
    """
    command = [
        'ffprobe', '-i', str(audio_path),
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=p=0'
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        duration_str = result.stdout.strip()
        duration = float(duration_str)
        return duration
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while retrieving audio duration: {e}")
        raise RuntimeError(f"Retrieving audio duration failed for {audio_path}")


def split_audio(audio_path, start, end, output_name: str, suffix: str) -> Path:
    output_path = Path(output_name + suffix)
    duration = end - start
    command = create_ffmpeg_split_command(suffix, audio_path, output_path, start, duration)
    subprocess.call(command, shell=True)
    return output_path


def create_ffmpeg_split_command(suffix, audio_path, output_path, start, duration):
    if suffix.lower() in [".flac", ".wav"]:
        return f'ffmpeg -loglevel error -i "{audio_path}" -ss {start} -t {duration} "{output_path}"'
    else:
        return f'ffmpeg -loglevel error -ss {start} -i "{audio_path}" -t {duration} -c copy "{output_path}"'


def mp3_gain(mp3_audio_path: Path):
    try:
        result = subprocess.call(f"mp3gain -r -k \"{str(mp3_audio_path)}\"", shell=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error executing mp3gain: {e}")
