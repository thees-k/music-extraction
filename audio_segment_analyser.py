from pathlib import Path
from pocketsphinx import AudioFile, get_model_path
import os


class AudioSegmentAnalyser:
    def __init__(self):
        self._language = "de-DE"
        self._model_path = "/path/to/de-de"  # Update this path to where you have your German models

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    def get_speech(self, segment_path: Path):
        """
        Perform speech recognition on the given audio segment using Pocketsphinx.

        Args:
            segment_path (Path): Path to the audio segment file.

        Returns:
            str: The recognized text from the audio segment.
        """
        config = {
            'verbose': False,
            'audio_file': str(segment_path),
            'buffer_size': 2048,
            'no_search': False,
            'full_utt': False,
            'hmm': os.path.join(self._model_path, 'acoustic-model'),  # Update to the folder containing mdef
            'lm': os.path.join(self._model_path, 'language-model.lm.bin'),  # Update to the language model file
            'dict': os.path.join(self._model_path, 'phonetic.dict')  # Update to the phonetic dictionary
        }

        audio = AudioFile(**config)
        recognized_text = []

        for phrase in audio:
            recognized_text.append(str(phrase))

        return " ".join(recognized_text).strip()
