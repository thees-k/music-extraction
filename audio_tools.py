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


def create_analysable_audio(audio_path: Path, wav_name="temp_audio.wav"):
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


def copy_to_tmp_wav(audio_path: Path):
    new_name = "tmp_" + audio_path.stem + ".wav"
    command = f'ffmpeg -loglevel error -i "{audio_path}" "{new_name}"'
    subprocess.call(command, shell=True)
    return Path(new_name)


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
