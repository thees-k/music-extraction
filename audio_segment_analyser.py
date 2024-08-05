from pathlib import Path
from pocketsphinx import AudioFile
from pydub import AudioSegment
import os
import webrtcvad
import struct


class AudioSegmentAnalyser:
    def __init__(self):
        self._language = "en-US"
        self._model_path = os.path.expanduser("~/.local/lib/python3.10/site-packages/pocketsphinx/model")
        self.vad = webrtcvad.Vad(2)  # Sensitivity level 2 (1-3, higher is more sensitive)

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    def get_speech(self, segment_path: Path):
        """
        Perform speech recognition on the given audio segment using Pocketsphinx.
        Filters out non-speech segments using a VAD.

        Args:
            segment_path (Path): Path to the audio segment file.

        Returns:
            str: The recognized text from the audio segment.
        """
        # Check for speech activity
        if not self.is_speech(segment_path):
            print("No speech detected in this segment.")
            return ""

        config = {
            'verbose': False,
            'audio_file': str(segment_path),
            'buffer_size': 2048,
            'no_search': False,
            'full_utt': False,
            'hmm': os.path.join(self._model_path, 'en-us', 'en-us'),
            'lm': os.path.join(self._model_path, 'en-us', 'en-us.lm.bin'),
            'dict': os.path.join(self._model_path, 'en-us', 'cmudict-en-us.dict'),
            'beam': 1e-55,
            'bestpath': True
        }

        audio = AudioFile(**config)
        recognized_text = []

        print("Starting speech recognition...")
        for phrase in audio:
            print(f"Recognized: {phrase}")
            recognized_text.append(str(phrase))

        result = " ".join(recognized_text)
        print(f"Final recognized text: {result}")
        return result

    def is_speech(self, wav_path: Path) -> bool:
        """
        Check if the audio contains speech using VAD.

        Args:
            wav_path (Path): Path to the WAV file.

        Returns:
            bool: True if speech is detected, otherwise False.
        """
        audio = AudioSegment.from_wav(wav_path)
        audio = audio.set_frame_rate(16000).set_channels(1)  # Ensure correct format

        samples = audio.raw_data
        sample_rate = audio.frame_rate
        sample_width = audio.sample_width

        # Validate that the audio format is 16-bit
        if sample_width != 2:
            raise ValueError("Audio must be 16-bit PCM.")

        is_speech_detected = False
        frame_duration_ms = 20  # Use a 20ms frame duration
        bytes_per_frame = int(sample_rate * (frame_duration_ms / 1000.0) * sample_width)

        # Process audio in chunks of 20ms
        for i in range(0, len(samples), bytes_per_frame):
            frame = samples[i:i + bytes_per_frame]
            if len(frame) < bytes_per_frame:
                break
            if self.vad.is_speech(frame, sample_rate):
                is_speech_detected = True
                break

        return is_speech_detected


# Example usage
if __name__ == "__main__":
    analyser = AudioSegmentAnalyser()
    test_audio_path = Path("test_audio.wav")
    print("Recognized Speech: ", analyser.get_speech(test_audio_path))

