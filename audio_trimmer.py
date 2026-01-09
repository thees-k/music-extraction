import tempfile
from pathlib import Path
import torch, torchaudio, numpy
from audio_tools import get_total_length_of_audio, split_audio, create_analysable_audio


def _get_begin_of_speech(audio_path):
    speech_timestamps = _get_speech_timestamps(audio_path)
    if speech_timestamps:
        begin_of_speech = speech_timestamps[0]['start'] / 16000
    else:
        return -1

    total_length = get_total_length_of_audio(audio_path)
    if begin_of_speech < 0 or begin_of_speech > total_length:
        raise RuntimeError(f'begin_of_speech ({begin_of_speech}) is not in the range from 0 to {total_length}')
    else:
        return begin_of_speech


def _get_end_of_speech(audio_path):
    speech_timestamps = _get_speech_timestamps(audio_path)
    if speech_timestamps:
        end_of_speech = speech_timestamps[-1]['end'] / 16000
    else:
        return -1

    total_length = get_total_length_of_audio(audio_path)
    if end_of_speech < 0 or end_of_speech > total_length:
        raise RuntimeError(f'end_of_speech ({end_of_speech}) is not in the range from 0 to {total_length}')
    else:
        return end_of_speech


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


def _backup(audio_path):
    original_name = audio_path.name
    backup_name = audio_path.stem + "_with_speech" + audio_path.suffix
    audio_path_backup = audio_path.with_name(backup_name)
    try:
        audio_path.rename(audio_path_backup)
    except FileNotFoundError:
        raise RuntimeError(f'Not found: "{original_name}"')
    except PermissionError:
        raise RuntimeError(f'You do not have permission to rename file "{original_name}".')
    except Exception as e:
        raise RuntimeError(f'An error occurred: {e}')
    return audio_path_backup


class AudioTrimmer:

    def __init__(self, audio_path: Path, to_be_analysed_segment_length: float,
                 less_silence_beginning=0.3, less_silence_end=0.3, with_backup = False, keep_speech_at_end = False):
        self._audio_path = audio_path
        self._to_be_analysed_segment_length = to_be_analysed_segment_length
        self._less_silence_beginning = less_silence_beginning
        self._less_silence_end = less_silence_end
        self._with_backup = with_backup
        self._keep_speech_at_end = keep_speech_at_end
        self._trimmed_length = 0.0
        self._audio_path_backup = None

    def trim(self):
        # reset trimmed_length
        self._trimmed_length = 0.0
        tmp_wav_path = None

        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_wav_path = create_analysable_audio(temp_dir, self._audio_path, wav_name= "tmp_" + self._audio_path.stem + ".wav")
            total_duration = get_total_length_of_audio(tmp_wav_path)
            if total_duration < self._to_be_analysed_segment_length:
                print(f"Length of {self._audio_path} is smaller than {self._to_be_analysed_segment_length} seconds.")
                exit(0)

            begin = self._find_begin(tmp_wav_path)
            end = self._find_end(tmp_wav_path, total_duration)
            self._trimmed_length = end - begin

        file_name = self._audio_path.stem
        suffix = self._audio_path.suffix
        self._audio_path_backup = _backup(self._audio_path)
        split_audio(self._audio_path_backup, begin, end, file_name, suffix)
        if self._audio_path_backup.exists() and not self._with_backup:
            self._audio_path_backup.unlink()
            self._audio_path_backup = None

    def _find_begin(self, tmp_wav_path):
        partial_audio = None
        try:
            partial_audio = split_audio(tmp_wav_path, 0, self._to_be_analysed_segment_length,
                                        f"tmp_begin", tmp_wav_path.suffix)
            end_of_speech = _get_end_of_speech(partial_audio)
            if end_of_speech == -1:
                end_of_speech = 0
            return min(end_of_speech + self._less_silence_beginning, self._to_be_analysed_segment_length)
        finally:
            if partial_audio and partial_audio.exists():
                partial_audio.unlink()


    def _find_end(self, tmp_wav_path, total_duration):
        partial_audio = None
        try:
            partial_audio = split_audio(tmp_wav_path, total_duration - self._to_be_analysed_segment_length, total_duration,
                                        f"tmp_end", tmp_wav_path.suffix)

            if self._keep_speech_at_end:
                end_of_speech = _get_end_of_speech(partial_audio)
                if end_of_speech == -1:
                    end_of_speech = get_total_length_of_audio(partial_audio)
                return min(total_duration, total_duration - self._to_be_analysed_segment_length + end_of_speech + self._less_silence_end)
            else:
                begin_of_speech = _get_begin_of_speech(partial_audio)
                if begin_of_speech == -1:
                    begin_of_speech = get_total_length_of_audio(partial_audio)
                return min(total_duration, total_duration - self._to_be_analysed_segment_length + begin_of_speech - self._less_silence_end)
        finally:
            if partial_audio and partial_audio.exists():
                partial_audio.unlink()

    @property
    def trimmed_length(self):
        return self._trimmed_length

    @property
    def audio_path_backup(self):
        return self._audio_path_backup
