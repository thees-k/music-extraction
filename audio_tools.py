import logging
import subprocess
from pathlib import Path
from pydub import AudioSegment


def extract_segment(wav_path: Path, start_time: int, duration: int, segment_name="temp_segment.wav"):
    """
    Extract a segment from the WAV audio file.

    Args:
        wav_path (Path): Path to the input WAV file.
        start_time (int): Start time of the segment in seconds.
        duration (int): Duration of the segment in seconds.
        segment_name (str): The output segment file.
    """
    segment_path = Path(segment_name)
    command = f'ffmpeg -loglevel error -ss {start_time} -t {duration} -i "{wav_path}" "{segment_path}"'
    result = subprocess.call(command, shell=True)
    if result != 0:
        logging.error(f"Failed to extract segment from {wav_path}")
        raise RuntimeError(f"ffmpeg segment extraction failed for {wav_path}")
    return segment_path


def convert_audio(audio_path: Path, wav_name="temp_audio.wav"):
    """
    Convert the audio file to WAV format suitable for Pocketsphinx.

    Args:
        audio_path (Path): Path to the input audio file.
        wav_name (str): Name of the output WAV file.
    """
    wav_path = Path(wav_name)
    try:
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(wav_path, format="wav")
        logging.info(f"Converted {audio_path} to {wav_path}")
    except Exception as e:
        logging.error(f"Failed to convert {audio_path} to {wav_path}: {e}")
        raise RuntimeError(f"Conversion to WAV failed for {audio_path}")

    return wav_path


def get_total_length_of_audio(audio_path: Path) -> float:
    """
    Get the total length of the given audio file in seconds
    :param audio_path: the audio file
    :return: the total length of the given audio file in seconds
    """
    return AudioSegment.from_file(audio_path).duration_seconds
