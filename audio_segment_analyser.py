from pathlib import Path
import wave
from vosk import Model, KaldiRecognizer
import os
import json

# This software uses the Vosk library for speech recognition.
# Vosk is licensed under the Apache License 2.0.


class AudioSegmentAnalyser:
    def __init__(self):
        model_path = os.path.expanduser("~/.local/models/vosk-model-small-de-0.15")  # small version
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path {model_path} does not exist. Please download and unzip a Vosk model.")

        self.model = Model(model_path)
        self._total_word_count = 0

    def get_speech(self, segment_path: Path):
        """
        Perform speech recognition on the given audio segment using Vosk.

        Args:
            segment_path (Path): Path to the audio segment file.

        Returns:
            str: The recognized text from the audio segment.
        """
        wf = wave.open(str(segment_path), "rb")

        # Ensure the audio file is in the correct format
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be WAV format with mono channel, 16-bit samples, and 16 kHz sample rate.")

        recognizer = KaldiRecognizer(self.model, wf.getframerate())

        self._total_word_count = 0
        text = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                words = self.fetch_words(recognizer.Result())
                self._append_words_to_text(text, words)

        words = self.fetch_words(recognizer.FinalResult())
        self._append_words_to_text(text, words)

        if self._total_word_count > 4:
            return " ".join(text)
        else:
            return ""

    def _append_words_to_text(self, recognized_text, words):
        word_count = len(words.split())
        if word_count:
            self._total_word_count += word_count
            recognized_text.append(words)

    @staticmethod
    def fetch_words(result):
        return json.loads(result)['text'].strip()


# Example usage
if __name__ == "__main__":
    analyser = AudioSegmentAnalyser()
    test_audio_path = Path("test_audio.wav")  # Update to your test audio file path
    print("Recognized Speech: ", analyser.get_speech(test_audio_path))
