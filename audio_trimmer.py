from pathlib import Path
# import torch, torchaudio, numpy
import torch
from audio_tools import get_total_length_of_audio, copy_to_tmp_wav, split_audio


def _get_begin_of_speech(audio_path):
    speech_timestamps = _get_speech_timestamps(audio_path)
    if speech_timestamps:
        return speech_timestamps[0]['start'] / 16000


def _get_end_of_speech(audio_path):
    speech_timestamps = _get_speech_timestamps(audio_path)
    if speech_timestamps:
        return speech_timestamps[-1]['end'] / 16000

def _get_speech_timestamps(audio_path, threshold=0.5, min_speech_duration_ms=250):
    torch.set_num_threads(1)

    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
    (get_speech_timestamps, _, read_audio, _, _) = utils

    wav = read_audio(audio_path)
    return get_speech_timestamps(
        wav,
        model,
        sampling_rate=16000,
        threshold=threshold,
        min_speech_duration_ms=min_speech_duration_ms
    )


class AudioTrimmer:

    def __init__(self, audio_path: Path, to_be_analysed_segment_length: float,
                 less_silence_beginning=0.2, less_silence_end=0.2, with_backup = False):
        self._audio_path = audio_path
        self._to_be_analysed_segment_length = to_be_analysed_segment_length
        self._less_silence_beginning = less_silence_beginning
        self._less_silence_end = less_silence_end
        self._with_backup = with_backup
        self._trimmed_length = 0.0
        self._backup_name = ""

    def trim(self):
        # reset trimmed_length
        self._trimmed_length = 0.0
        tmp_wav_path = None
        try:
            tmp_wav_path = copy_to_tmp_wav(self._audio_path)
            total_duration = get_total_length_of_audio(tmp_wav_path)
            if total_duration < self._to_be_analysed_segment_length:
                print(f"Length of {self._audio_path} is smaller than {self._to_be_analysed_segment_length} seconds.")
                exit(0)

            begin = self._find_begin(tmp_wav_path)
            end = self._find_end(tmp_wav_path, total_duration)
            self._trimmed_length = end - begin
        finally:
            if tmp_wav_path and tmp_wav_path.exists():
                tmp_wav_path.unlink()

        file_name = self._audio_path.stem
        suffix = self._audio_path.suffix
        audio_path_backup = self._backup(self._audio_path)
        split_audio(audio_path_backup, begin, end, file_name, suffix)
        if audio_path_backup.exists() and not self._with_backup:
            audio_path_backup.unlink()

    def _find_begin(self, tmp_wav_path):
        partial_audio = None
        try:
            partial_audio = split_audio(tmp_wav_path, 0, self._to_be_analysed_segment_length,
                                        f"tmp_begin", tmp_wav_path.suffix)
            end_of_speech = _get_end_of_speech(partial_audio)
            if end_of_speech:
                return end_of_speech + self._less_silence_beginning
            else:
                return 0.0
        finally:
            if partial_audio and partial_audio.exists():
                partial_audio.unlink()


    def _find_end(self, tmp_wav_path, total_duration):
        partial_audio = None
        try:
            partial_audio = split_audio(tmp_wav_path, total_duration - self._to_be_analysed_segment_length, total_duration,
                                        f"tmp_end", tmp_wav_path.suffix)
            begin_of_speech = _get_begin_of_speech(partial_audio)
            if begin_of_speech:
                return total_duration - (self._to_be_analysed_segment_length - begin_of_speech) - self._less_silence_end
            else:
                return total_duration
        finally:
            if partial_audio and partial_audio.exists():
                partial_audio.unlink()

    def _backup(self, audio_path):
        original_name = audio_path.name
        self._backup_name = audio_path.stem + "_with_speech" + audio_path.suffix
        audio_path_backup = audio_path.with_name(self._backup_name)
        try:
            audio_path.rename(audio_path_backup)
        except FileNotFoundError:
            raise RuntimeError(f'Not found: "{original_name}"')
        except PermissionError:
            raise RuntimeError(f'You do not have permission to rename file "{original_name}".')
        except Exception as e:
            raise RuntimeError(f'An error occurred: {e}')
        return audio_path_backup

    @property
    def trimmed_length(self):
        return self._trimmed_length

    @property
    def backup_name(self):
        return self._backup_name
