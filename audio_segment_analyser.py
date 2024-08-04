from pathlib import Path

import speech_recognition as sr
import socket


class AudioSegmentAnalyser:
    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._language = "de-DE"
        if not AudioSegmentAnalyser._check_internet_connection():
            print("Program cannot be executed without connection to the internet")
            exit(1)

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    @classmethod
    def _check_internet_connection(cls, timeout=2):
        """
        Check if there is an internet connection by attempting to connect to a well-known host.

        Args:
            timeout (int, optional): Timeout in seconds for the connection attempt. Defaults to 2.

        Returns:
            bool: True if the internet connection is available, False otherwise.
        """
        try:
            # Try to connect to a well-known host (Google DNS server) on port 53 (DNS service)
            socket.setdefaulttimeout(timeout)
            host = socket.gethostbyname("8.8.8.8")
            s = socket.create_connection((host, 53), timeout)
            s.close()
            return True
        except OSError:
            return False

    def get_speech(self, segment_path: Path):
        """
        Perform speech recognition on the given audio segment.

        Args:
            segment_path (Path): Path to the audio segment file.

        Returns:
            str: The recognized text from the audio segment.
        """
        with sr.AudioFile(str(segment_path)) as source:
            audio_data = self._recognizer.record(source)
            try:
                return self._recognizer.recognize_google(audio_data, language=self._language)
            except sr.UnknownValueError:
                return ""
