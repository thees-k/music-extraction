import logging
import subprocess
from pathlib import Path
from pydub import AudioSegment


def extract_segment(flac_path: Path, start_time: int, duration: int, segment_name="temp_segment.flac"):
    """
    Extract a segment from the FLAC audio file.

    Args:
        flac_path (Path): Path to the input FLAC file.
        start_time (int): Start time of the segment in seconds.
        duration (int): Duration of the segment in seconds.
        segment_name (Path): Path to the output segment file.
    """
    segment_path = Path(segment_name)
    command = f'ffmpeg -loglevel error -ss {start_time} -t {duration} -i "{flac_path}" -c copy "{segment_path}"'
    result = subprocess.call(command, shell=True)
    if result != 0:
        logging.error(f"Failed to extract segment from {flac_path}")
        raise RuntimeError(f"ffmpeg segment extraction failed for {flac_path}")
    return segment_path


def convert_audio_to_flac(audio_path: Path, flac_name="temp_audio.flac"):
    """
    Convert the audio file to FLAC format.

    Args:
        audio_path (Path): Path to the input audio file.
        flac_name (Path): Name of the output FLAC file.
    """
    flac_path = Path(flac_name)
    command = f'ffmpeg -loglevel error -i "{audio_path}" "{flac_path}"'
    result = subprocess.call(command, shell=True)
    if result != 0:
        logging.error(f"Failed to convert {audio_path} to {flac_path}")
        raise RuntimeError(f"ffmpeg conversion failed for {audio_path}")
    logging.info(f"Converted {audio_path} to {flac_path}")
    return flac_path


def get_total_length_of_audio(audio_path: Path) -> float:
    """
    Get the total length of the given audio file in seconds
    :param audio_path: the audio file
    :return: the total length of the given audio file in seconds
    """
    return AudioSegment.from_file(audio_path).duration_seconds
