from pathlib import Path
import wave
from vosk import Model, KaldiRecognizer
import os
import json


class AudioSegmentAnalyser:
    def __init__(self):
        # Initialize Vosk model
        model_path = os.path.expanduser("~/.local/lib/vosk-model-de-0.21")  # Update this to your Vosk model path
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path {model_path} does not exist. Please download and unzip a Vosk model.")

        self.model = Model(model_path)

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

        recognized_text = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                recognized_text.append(result['text'])
            else:
                partial_result = json.loads(recognizer.PartialResult())

        final_result = json.loads(recognizer.FinalResult())
        recognized_text.append(final_result['text'])

        return " ".join(recognized_text)


# Example usage
if __name__ == "__main__":
    analyser = AudioSegmentAnalyser()
    test_audio_path = Path("test_audio.wav")  # Update to your test audio file path
    print("Recognized Speech: ", analyser.get_speech(test_audio_path))
