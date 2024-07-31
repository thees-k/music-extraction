import os
import subprocess
import signal
import sys
from pydub import AudioSegment
import speech_recognition as sr
import zipfile
from enum import Enum


class AnalyzeFileStatus(Enum):
    NOT_EXISTING = 'not_existing'
    EMPTY = 'empty'
    FIRST_LINE_IS_NO_DIGIT = 'first_line_is_no_digit'
    SEVERAL_LINES_BUT_LAST_LINE_IS_NO_DIGIT = 'several_lines_but_last_line_is_no_digit'
    FILE_OK = 'file_ok'


class AnalysisType(Enum):
    FULL = 'Full Analysis'
    CONTINUE = 'Continue Analysis'
    NOT_NECESSARY = 'Analysis is not necessary'


class SpeechFinder:

    def __init__(self, audio_path):
        self._audio_path = audio_path
        self._analyze_file_path = self._build_analyze_file_path()

    def build(self):
        analyze_type = self._get_analyze_type()

        if analyze_type == AnalysisType.NOT_NECESSARY:
            end_time, lines = self._prepare_analysis_file()
            self._do_analysis(end_time, lines)
        elif analyze_type == AnalysisType.FULL:
            self._delete_analysis_file_if_exists()
            self._do_analysis()
        elif analyze_type == AnalysisType.CONTINUE:
            pass
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
                end_time = int(line)
                lines = lines[:i]
                break

        return end_time, lines

    def _do_analysis(self, start_time=0, old_lines=()):
        segment_length_sec = 20
        wav_path = "temp_audio.wav"
        convert_audio_to_wav(self._audio_path, wav_path)

        recognizer = sr.Recognizer()

        total_length = AudioSegment.from_wav(wav_path).duration_seconds

        print("\nAnalyzing audio segments... (Press Ctrl+C to interrupt)")

        # Register the signal handler
        signal.signal(signal.SIGINT, signal_handler)

        global interrupt

        with open(self._analyze_file_path, "w") as file:

            if old_lines:
                file.writelines(old_lines)
            else:
                segment_length = str(segment_length_sec)
                file.write(segment_length + "\n")
                print(segment_length)

            segment_path = "temp_segment.wav"

            while start_time < total_length:
                end_time = start_time + segment_length_sec
                if end_time > total_length:
                    end_time = total_length

                try:
                    extract_segment(wav_path, start_time, segment_length_sec, segment_path)
                    speech_segment = get_speech_segment(segment_path, recognizer)
                    if speech_segment:
                        line = str(start_time) + " " + speech_segment
                        file.write(line + "\n")
                        print(line)
                finally:
                    if os.path.exists(segment_path):
                        os.remove(segment_path)

                start_time = end_time

                if interrupt and end_time < total_length:
                    end = str(end_time)
                    file.write(end + "\n")
                    print(end)
                    break

        os.remove(wav_path)
        print(f"Removed temporary file {wav_path}")

        # Unset signal handler
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def _delete_analysis_file_if_exists(self):
        if os.path.isfile(self._analyze_file_path):
            os.remove(self._analyze_file_path)

    def _build_analyze_file_path(self):
        path, filename = os.path.split(self._audio_path)
        filename_without_suffix, _ = os.path.splitext(filename)
        return os.path.join(path, filename_without_suffix) + ".speech"

    def _get_analyze_type(self):

        status = self._check_file()

        if (status == AnalyzeFileStatus.NOT_EXISTING or status == AnalyzeFileStatus.EMPTY or
                status == AnalyzeFileStatus.FIRST_LINE_IS_NO_DIGIT):
            return AnalysisType.FULL
        elif status == AnalyzeFileStatus.SEVERAL_LINES_BUT_LAST_LINE_IS_NO_DIGIT:
            return AnalysisType.CONTINUE
        elif status == AnalyzeFileStatus.FILE_OK:
            return AnalysisType.NOT_NECESSARY
        else:
            raise NotImplementedError(f"Not implemented for {status}")

    def _check_file(self):

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
                last_line = lines[-1].strip()
                if last_line.isdigit():
                    return AnalyzeFileStatus.FILE_OK
                return AnalyzeFileStatus.SEVERAL_LINES_BUT_LAST_LINE_IS_NO_DIGIT
            else:
                return AnalyzeFileStatus.FILE_OK


def signal_handler(sig, frame):
    global interrupt
    interrupt = True


def convert_audio_to_wav(audio_path, wav_path):
    command = f'ffmpeg -loglevel error -i "{audio_path}" "{wav_path}"'
    subprocess.call(command, shell=True)
    print(f"Converted {audio_path} to {wav_path}")


def extract_segment(wav_path, start_time, duration, segment_path):
    command = f'ffmpeg -loglevel error -ss {start_time} -t {duration} -i "{wav_path}" "{segment_path}"'
    subprocess.call(command, shell=True)


def get_speech_segment(segment_path, recognizer):
    with sr.AudioFile(segment_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language="de-DE")
        except sr.UnknownValueError:
            return ""


def seconds_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02}"


def zip_textfile(file_path):
    zip_path = file_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, arcname=file_path.split("/")[-1])


# Global variable to track if the process should be interrupted
interrupt = False


def main():

    if len(sys.argv) != 2:
        print("Missing audio file")
        sys.exit(1)

    audio_file_path = sys.argv[1]

    if not os.path.isfile(audio_file_path):
        print(f"File not found: {audio_file_path}")
        sys.exit(1)

    SpeechFinder(audio_file_path).build()


if __name__ == "__main__":
    main()
