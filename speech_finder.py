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
import socket

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')


class AnalyzeFileStatus(Enum):
    """
    Enumeration to represent the status of the analysis file.
    """
    NOT_EXISTING = 'not_existing'
    EMPTY = 'empty'
    FIRST_LINE_IS_NO_DIGIT = 'first_line_is_no_digit'
    SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT = 'several_lines_and_last_line_is_digit'
    FILE_OK = 'file_ok'


class AnalysisType(Enum):
    """
    Enumeration to represent the type of analysis to be performed.
    """
    FULL = 'Full Analysis'
    CONTINUE = 'Continue Analysis'
    NOT_NECESSARY = 'Analysis is not necessary'


class SpeechFinder:
    """
    Class to handle the analysis of an audio file, finding and saving speech segments.

    Attributes:
        SEGMENT_LENGTH_SEC (int): Length of each audio segment in seconds.
        _audio_path (Path): Path to the audio file to be analyzed.
        _analyze_file_path (str): Path to the file where analysis results are stored.
        _interrupt (bool): Flag to indicate if the process was interrupted.
    """

    SEGMENT_LENGTH_SEC = 20

    def __init__(self, audio_path: str):
        """
        Initialize the SpeechFinder with the given audio file path.

        Args:
            audio_path (str): Path to the audio file.
        """
        self._audio_path = Path(audio_path)
        self._analyze_file_path = self._build_analyze_file_path()
        self._interrupt = False

    def find_segments(self):
        """
        Determine the type of analysis to perform and execute it.
        """
        analyze_type = self._get_analyze_type()

        if not self.check_internet_connection():
            logging.error("Program cannot be executed without connection to the internet")
            exit(1)

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
        """
        Prepare the analysis file by reading its content and finding the last non-empty digit line.

        Returns:
            Tuple[int, List[str]]: End time and lines read from the file.
        """
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
        """
        Perform the speech recognition analysis on the audio file, segment by segment.

        Args:
            start_time (int, optional): The time to start the analysis from. Defaults to 0.
            old_lines (tuple, optional): Existing lines from a previous analysis. Defaults to ().
        """
        flac_path = Path("temp_audio.flac")
        self.convert_audio_to_flac(self._audio_path, flac_path)

        recognizer = sr.Recognizer()
        total_length = AudioSegment.from_file(flac_path).duration_seconds
        logging.info("Analyzing audio segments... (Press Ctrl+C to interrupt)")

        signal.signal(signal.SIGINT, self._signal_handler)
        self._interrupt = False  # Reset interrupt flag before starting analysis

        with open(self._analyze_file_path, "w") as file:
            if old_lines:
                file.writelines(old_lines)
            else:
                file.write(f"{self.SEGMENT_LENGTH_SEC}\n")
                logging.info(self.SEGMENT_LENGTH_SEC)

            segment_path = Path("temp_segment.flac")

            while start_time < total_length:
                end_time = start_time + self.SEGMENT_LENGTH_SEC
                if end_time > total_length:
                    end_time = total_length

                try:
                    self.extract_segment(flac_path, start_time, self.SEGMENT_LENGTH_SEC, segment_path)
                    speech_segment = self.get_speech_segment(segment_path, recognizer)
                    if speech_segment is None:
                        file.write(f"{start_time}\n")
                        logging.info(f"Analysis stopped at {start_time} due to a RequestError.")
                        break
                    elif speech_segment:
                        line = f"{start_time} {speech_segment}"
                        file.write(line + "\n")
                        logging.info(line)
                except sr.RequestError as e:
                    logging.error(f"RequestError at segment starting at {start_time}: {e}")
                    file.write(f"{start_time}\n")
                    break
                finally:
                    if os.path.exists(segment_path):
                        os.remove(segment_path)

                start_time = end_time

                if self._interrupt and end_time < total_length:
                    file.write(f"{end_time}\n")
                    logging.info(f"Analysis interrupted at {end_time}.")
                    break

        os.remove(flac_path)
        logging.info(f"Removed temporary file {flac_path}")
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def _delete_analysis_file_if_exists(self):
        """
        Delete the analysis file if it exists.
        """
        if os.path.isfile(self._analyze_file_path):
            os.remove(self._analyze_file_path)

    def _build_analyze_file_path(self) -> str:
        """
        Build the path for the analysis file based on the audio file path.

        Returns:
            str: Path to the analysis file.
        """
        return str(self._audio_path.with_suffix('.speech'))

    def _get_analyze_type(self) -> AnalysisType:
        """
        Determine the type of analysis to perform based on the status of the analysis file.

        Returns:
            AnalysisType: The type of analysis to perform.
        """
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
        """
        Check the status of the analysis file.

        Returns:
            AnalyzeFileStatus: The status of the analysis file.
        """
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
        """
        Signal handler for interrupt signals.

        Args:
            sig (int): The signal number.
            frame (FrameType): The current stack frame.
        """
        self._interrupt = True

    @staticmethod
    def convert_audio_to_flac(audio_path: Path, flac_path: Path):
        """
        Convert the audio file to FLAC format.

        Args:
            audio_path (Path): Path to the input audio file.
            flac_path (Path): Path to the output FLAC file.
        """
        command = f'ffmpeg -loglevel error -i "{audio_path}" "{flac_path}"'
        result = subprocess.call(command, shell=True)
        if result != 0:
            logging.error(f"Failed to convert {audio_path} to {flac_path}")
            raise RuntimeError(f"ffmpeg conversion failed for {audio_path}")
        logging.info(f"Converted {audio_path} to {flac_path}")

    @staticmethod
    def extract_segment(flac_path: Path, start_time: int, duration: int, segment_path: Path):
        """
        Extract a segment from the FLAC audio file.

        Args:
            flac_path (Path): Path to the input FLAC file.
            start_time (int): Start time of the segment in seconds.
            duration (int): Duration of the segment in seconds.
            segment_path (Path): Path to the output segment file.
        """
        command = f'ffmpeg -loglevel error -ss {start_time} -t {duration} -i "{flac_path}" "{segment_path}"'
        result = subprocess.call(command, shell=True)
        if result != 0:
            logging.error(f"Failed to extract segment from {flac_path}")
            raise RuntimeError(f"ffmpeg segment extraction failed for {flac_path}")

    @staticmethod
    def check_internet_connection(timeout=2):
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

    @staticmethod
    def get_speech_segment(segment_path: Path, recognizer: sr.Recognizer):
        """
        Perform speech recognition on the given audio segment.

        Args:
            segment_path (Path): Path to the audio segment file.
            recognizer (sr.Recognizer): The speech recognizer instance.

        Returns:
            str: The recognized text from the audio segment, or None if a RequestError occurs.
        """
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
    """
    Find the last non-empty line in a list of lines.

    Args:
        lines (List[str]): List of lines to search through.

    Returns:
        str: The last non-empty line, or None if no such line is found.
    """
    for line in reversed(lines):
        if line.strip():  # Checks if the string is not empty or whitespace only
            return line.strip()


def zip_textfile(file_path: str):
    """
    Create a zip file containing the given text file.

    Args:
        file_path (str): Path to the text file to be zipped.
    """
    zip_path = file_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, arcname=Path(file_path).name)


def main():
    """
    Main function to execute the speech analysis process.
    """
    if len(sys.argv) != 2:
        logging.error("Missing audio file")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    if not os.path.isfile(audio_file_path):
        logging.error(f"File not found: {audio_file_path}")
        sys.exit(1)

    SpeechFinder(audio_file_path).find_segments()


if __name__ == "__main__":
    main()
