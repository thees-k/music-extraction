import os
import signal
import sys
from enum import Enum
from pathlib import Path
from audio_tools import extract_segment, convert_audio, get_total_length_of_audio
from seconds_formatter import seconds_to_min_sec
from audio_segment_analyser import AudioSegmentAnalyser


class AnalyzeFileStatus(Enum):
    """
    Enumeration to represent the status of the analysis file.
    """
    NOT_EXISTING = 'not_existing'
    EMPTY = 'empty'
    FIRST_LINE_IS_NO_DIGIT = 'first_line_is_no_digit'
    SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT = 'several_lines_and_last_line_is_digit'
    FULLY_ANALYSED = 'fully_analysed'


class NecessaryAnalysis(Enum):
    """
    Enumeration to represent the type of analysis to be performed.
    """
    FULLY = 'Fully'
    CONTINUE = 'Continue'
    NOT_NECESSARY = 'Not necessary'


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
        self._analyze_file_path = str(self._audio_path.with_suffix('.speech'))
        self._interrupt = False
        self._total_length = 0.0

    def find_segments(self):
        self._total_length = get_total_length_of_audio(self._audio_path)
        necessary_analysis = self._get_necessary_analysis()

        if necessary_analysis == NecessaryAnalysis.NOT_NECESSARY:
            pass
        elif necessary_analysis == NecessaryAnalysis.FULLY:
            print("Full analysis")
            self._delete_analysis_file_if_exists()
            self._do_analysis()
        elif necessary_analysis == NecessaryAnalysis.CONTINUE:
            print("Continuing the analysis")
            lines = self._load_lines_of_analysis_file()
            self._do_analysis(lines)
        else:
            raise NotImplementedError(f"Not implemented for {necessary_analysis}")

        return self._load_lines_of_analysis_file(), self._total_length

    def _do_analysis(self, old_lines=()):
        """
        Perform the speech recognition analysis on the audio file, segment by segment.

        Args:
            old_lines (tuple, optional): Existing lines from a previous analysis. Defaults to ().
        """
        print("Convert audio...")
        converted_audio_path = convert_audio(self._audio_path)

        segment_analyser = AudioSegmentAnalyser()
        total_length_display = seconds_to_min_sec(int(self._total_length))
        if old_lines:
            start_time, old_lines = int(old_lines[-1]), old_lines[:-1]
            print(f"Continue analysing audio segments... (Press Ctrl+C to interrupt)")
            if not self.needs_print(start_time):
                print(f"{seconds_to_min_sec(start_time)} (of {total_length_display})...")
        else:
            print("Analysing audio segments... (Press Ctrl+C to interrupt)")
            start_time = 0

        self._interrupt = False  # Reset interrupt flag before starting analysis
        signal.signal(signal.SIGINT, self._signal_handler)

        with open(self._analyze_file_path, "w") as file:
            if old_lines:
                for old_line in old_lines:
                    file.write(old_line + "\n")
            else:
                file.write(f"{self.SEGMENT_LENGTH_SEC}\n")

            while start_time < self._total_length:
                if self.needs_print(start_time):
                    print(f"{seconds_to_min_sec(start_time)} (of {total_length_display})...")

                end_time = start_time + self.SEGMENT_LENGTH_SEC
                if end_time > self._total_length:
                    end_time = self._total_length

                try:
                    segment_path = extract_segment(converted_audio_path, start_time, self.SEGMENT_LENGTH_SEC,
                                                   segment_name=f"tmp_segment_{start_time}.wav")
                    speech_segment = segment_analyser.get_speech(segment_path)
                    if speech_segment:
                        line = f"{start_time} {speech_segment}"
                        file.write(line + "\n")
                        print(f"{seconds_to_min_sec(start_time)} {speech_segment}")
                finally:
                    if os.path.exists(segment_path):
                        os.remove(segment_path)

                start_time = end_time

                if self._interrupt and end_time < self._total_length:
                    file.write(f"{end_time}\n")
                    print(f"User interrupted analysis at {seconds_to_min_sec(end_time)}.")
                    break

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        if os.path.exists(converted_audio_path):
            print("Cleanup converted audio")
            os.remove(converted_audio_path)

    @staticmethod
    def needs_print(start_time):
        return start_time % 60 == 0

    def _delete_analysis_file_if_exists(self):
        """
        Delete the analysis file if it exists.
        """
        if os.path.isfile(self._analyze_file_path):
            os.remove(self._analyze_file_path)

    def _get_necessary_analysis(self) -> NecessaryAnalysis:
        """
        Determine the type of analysis to perform based on the status of the analysis file.

        Returns:
            NecessaryAnalysis: The type of analysis to perform.
        """
        status = self._get_analyze_file_status()
        if status in (AnalyzeFileStatus.NOT_EXISTING,
                      AnalyzeFileStatus.EMPTY,
                      AnalyzeFileStatus.FIRST_LINE_IS_NO_DIGIT):
            return NecessaryAnalysis.FULLY
        elif status == AnalyzeFileStatus.SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT:
            return NecessaryAnalysis.CONTINUE
        elif status == AnalyzeFileStatus.FULLY_ANALYSED:
            return NecessaryAnalysis.NOT_NECESSARY
        else:
            raise NotImplementedError(f"Not implemented for {status}")

    def _get_analyze_file_status(self) -> AnalyzeFileStatus:
        """
        Get the status of the analysis file.

        Returns:
            AnalyzeFileStatus: The status of the analysis file.
        """
        if not os.path.isfile(self._analyze_file_path):
            return AnalyzeFileStatus.NOT_EXISTING
        if os.path.getsize(self._analyze_file_path) == 0:
            return AnalyzeFileStatus.EMPTY

        lines = self._load_lines_of_analysis_file()

        if not lines:
            return AnalyzeFileStatus.EMPTY

        first_line = lines[0]
        if not first_line.isdigit():
            return AnalyzeFileStatus.FIRST_LINE_IS_NO_DIGIT

        if len(lines) > 1:
            last_line = lines[-1]
            if last_line.isdigit():
                return AnalyzeFileStatus.SEVERAL_LINES_AND_LAST_LINE_IS_DIGIT
            return AnalyzeFileStatus.FULLY_ANALYSED
        else:
            return AnalyzeFileStatus.FULLY_ANALYSED

    def _load_lines_of_analysis_file(self):
        lines = []
        with open(self._analyze_file_path, 'r') as analyze_file:
            for line in analyze_file.readlines():
                line_strip = line.strip()
                if line_strip:
                    lines.append(line_strip)
        return lines

    def _signal_handler(self, sig, frame):
        """
        Signal handler for interrupt signals.

        Args:
            sig (int): The signal number.
            frame (FrameType): The current stack frame.
        """
        self._interrupt = True


def main():
    """
    Main function to execute the speech analysis process.
    """
    if len(sys.argv) != 2:
        print("Missing audio file")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    if not os.path.isfile(audio_file_path):
        print(f"File not found: {audio_file_path}")
        sys.exit(1)

    SpeechFinder(audio_file_path).find_segments()


if __name__ == "__main__":
    main()
