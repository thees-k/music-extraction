import os
import subprocess
import signal
import sys
from pydub import AudioSegment
import speech_recognition as sr
import zipfile
from enum import Enum
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')


class AnalyzeFileStatus(Enum):
    NOT_EXISTING = 'not_existing'
    EMPTY = 'empty'
    FIRST_LINE_IS_NO_DIGIT = 'first_line_is_no_digit'
    SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT = 'several_lines_and_last_line_is_digit'
    FILE_OK = 'file_ok'


class AnalysisType(Enum):
    FULL = 'Full Analysis'
    CONTINUE = 'Continue Analysis'
    NOT_NECESSARY = 'Analysis is not necessary'


class SpeechFinder:
    SEGMENT_LENGTH_SEC = 20

    def __init__(self, audio_path: str):
        self._audio_path = Path(audio_path)
        self._analyze_file_path = self._build_analyze_file_path()

    def build(self):
        analyze_type = self._get_analyze_type()

        if analyze_type == AnalysisType.NOT_NECESSARY:
            pass
        elif analyze_type == AnalysisType.FULL:
            self._delete_analysis_file_if_exists()
            self._do_analysis()
        elif analyze_type == AnalysisType.CONTINUE:
            end_time, lines = self._prepare_analysis_file()
            self._do_analysis(end_time, lines)
        else:
            raise NotImplementedError(f"Not implemented for {analyze_type}")

    def _prepare_analysis_file(self):
        end_time = None
        with open(self._analyze_file_path, 'r') as file:
            lines = file.readlines()

        # Find the last non-empty line that is a digit and remove it from lines
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line != "":
                if line.isdigit():
                    end_time = int(line)
                    lines = lines[:i]
                    break
                else:
                    raise ValueError("The last non-empty line is not a digit.")

        return end_time, lines

    def _do_analysis(self, start_time=0, old_lines=()):
        wav_path = Path("temp_audio.wav")
        self.convert_audio_to_wav(self._audio_path, wav_path)

        recognizer = sr.Recognizer()
        total_length = AudioSegment.from_wav(wav_path).duration_seconds
        logging.info("Analyzing audio segments... (Press Ctrl+C to interrupt)")

        self._interrupt = False
        signal.signal(signal.SIGINT, self._signal_handler)

        with open(self._analyze_file_path, "w") as file:
            if old_lines:
                file.writelines(old_lines)
            else:
                file.write(f"{self.SEGMENT_LENGTH_SEC}\n")
                logging.info(self.SEGMENT_LENGTH_SEC)

            segment_path = Path("temp_segment.wav")

            while start_time < total_length:
                end_time = start_time + self.SEGMENT_LENGTH_SEC
                if end_time > total_length:
                    end_time = total_length

                try:
                    self.extract_segment(wav_path, start_time, self.SEGMENT_LENGTH_SEC, segment_path)
                    speech_segment = self.get_speech_segment(segment_path, recognizer)
                    if speech_segment is None:
                        file.write(f"{start_time}\n")
                        logging.info(start_time)
                        break
                    elif speech_segment:
                        line = f"{start_time} {speech_segment}"
                        file.write(line + "\n")
                        logging.info(line)
                finally:
                    if os.path.exists(segment_path):
                        os.remove(segment_path)

                start_time = end_time

                if self._interrupt and end_time < total_length:
                    file.write(f"{end_time}\n")
                    logging.info(end_time)
                    break

        os.remove(wav_path)
        logging.info(f"Removed temporary file {wav_path}")
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def _delete_analysis_file_if_exists(self):
        if os.path.isfile(self._analyze_file_path):
            os.remove(self._analyze_file_path)

    def _build_analyze_file_path(self) -> str:
        return str(self._audio_path.with_suffix('.speech'))

    def _get_analyze_type(self) -> AnalysisType:
        status = self._check_file()
        if status in (AnalyzeFileStatus.NOT_EXISTING, AnalyzeFileStatus.EMPTY, AnalyzeFileStatus.FIRST_LINE_IS_NO_DIGIT):
            return AnalysisType.FULL
        elif status == AnalyzeFileStatus.SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT:
            return AnalysisType.CONTINUE
        elif status == AnalyzeFileStatus.FILE_OK:
            return AnalysisType.NOT_NECESSARY
        else:
            raise NotImplementedError(f"Not implemented for {status}")

    def _check_file(self) -> AnalyzeFileStatus:
        if not os.path.isfile(self._analyze_file_path):
            return AnalyzeFileStatus.NOT_EXISTING
        if os.path.getsize(self._analyze_file_path) == 0:
            return AnalyzeFileStatus.EMPTY

        with open(self._analyze_file_path, 'r') as analyze_file:
            lines = analyze_file.readlines()
            first_line = lines[0].strip()
            if not first_line.isdigit():
                return AnalyzeFileStatus.FIRST_LINE_IS_NO_DIGIT

            if len(lines) > 1:
                last_line = find_last_non_empty_line(lines)
                if last_line.isdigit():
                    return AnalyzeFileStatus.SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT
                return AnalyzeFileStatus.FILE_OK
            else:
                return AnalyzeFileStatus.FILE_OK

    def _signal_handler(self, sig, frame):
        self._interrupt = True

    @staticmethod
    def convert_audio_to_wav(audio_path: Path, wav_path: Path):
        command = f'ffmpeg -loglevel error -i "{audio_path}" "{wav_path}"'
        result = subprocess.call(command, shell=True)
        if result != 0:
            logging.error(f"Failed to convert {audio_path} to {wav_path}")
            raise RuntimeError(f"ffmpeg conversion failed for {audio_path}")
        logging.info(f"Converted {audio_path} to {wav_path}")

    @staticmethod
    def extract_segment(wav_path: Path, start_time: int, duration: int, segment_path: Path):
        command = f'ffmpeg -loglevel error -ss {start_time} -t {duration} -i "{wav_path}" "{segment_path}"'
        result = subprocess.call(command, shell=True)
        if result != 0:
            logging.error(f"Failed to extract segment from {wav_path}")
            raise RuntimeError(f"ffmpeg segment extraction failed for {wav_path}")

    @staticmethod
    def get_speech_segment(segment_path: Path, recognizer: sr.Recognizer):
        with sr.AudioFile(str(segment_path)) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language="de-DE")
            except sr.UnknownValueError:
                return ""
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech Recognition service; {e}")
                return None


def find_last_non_empty_line(lines) -> str:
    for line in reversed(lines):
        if line.strip():  # Checks if the string is not empty or whitespace only
            return line.strip()


def zip_textfile(file_path: str):
    zip_path = file_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, arcname=Path(file_path).name)


def main():
    if len(sys.argv) != 2:
        logging.error("Missing audio file")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    if not os.path.isfile(audio_file_path):
        logging.error(f"File not found: {audio_file_path}")
        sys.exit(1)

    SpeechFinder(audio_file_path).build()


if __name__ == "__main__":
    main()
