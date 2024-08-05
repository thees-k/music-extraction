from pathlib import Path
from pocketsphinx import AudioFile
import os


class AudioSegmentAnalyser:
    def __init__(self):
        self._language = "en-US"  # Using English for testing
        self._model_path = os.path.expanduser("~/.local/lib/python3.10/site-packages/pocketsphinx/model")

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
            'verbose': False,  # Enable verbose to see detailed logging
            'audio_file': str(segment_path),
            'buffer_size': 2048,
            'no_search': False,
            'full_utt': False,
            'hmm': os.path.join(self._model_path, 'en-us', 'en-us'),
            'lm': os.path.join(self._model_path, 'en-us', 'en-us.lm.bin'),
            'dict': os.path.join(self._model_path, 'en-us', 'cmudict-en-us.dict'),
            'beam': 1e-60,  # Default is 1e-48, you can adjust this for sensitivity
            'bestpath': True
        }

        audio = AudioFile(**config)
        recognized_text = []

        for phrase in audio:
            recognized_text.append(str(phrase))

        return " ".join(recognized_text)


# Example usage
if __name__ == "__main__":
    analyser = AudioSegmentAnalyser()
    # Use a test WAV file path here
    test_audio_path = Path("test_audio.wav")
    print("Recognized Speech: ", analyser.get_speech(test_audio_path))
