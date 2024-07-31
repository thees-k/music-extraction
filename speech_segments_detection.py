import os
import subprocess
import signal
import sys
from pydub import AudioSegment
import speech_recognition as sr
import zipfile


def signal_handler(sig, frame):
    global interrupt
    interrupt = True


def omit_suffix(path_and_filename):
    path, filename = os.path.split(path_and_filename)
    filename_without_suffix, _ = os.path.splitext(filename)
    return os.path.join(path, filename_without_suffix)


def build_analyse_file_path(path_and_filename):
    return omit_suffix(path_and_filename) + ".speech"


def convert_mp3_to_wav(mp3_path, wav_path):
    command = f'ffmpeg -loglevel error -i "{mp3_path}" "{wav_path}"'
    subprocess.call(command, shell=True)
    print(f"Converted {mp3_path} to {wav_path}")


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


def read_last_line_if_exists(file_path):
    if not os.path.isfile(file_path):
        return ""

    with open(file_path, 'rb') as file:
        file.seek(-2, 2)
        while file.read(1) != b'\n':
            file.seek(-2, 1)
        last_line = file.readline().decode()
    return last_line.strip()


def analyze(mp3_path, segment_length_sec=20):

    wav_path = "temp_audio.wav"
    convert_mp3_to_wav(mp3_path, wav_path)

    recognizer = sr.Recognizer()

    total_length = AudioSegment.from_wav(wav_path).duration_seconds
    start_time = 0

    result_analyse_file_path = build_analyse_file_path(mp3_path)

    print("\nAnalyzing audio segments... (Press Ctrl+C to interrupt)")

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    global interrupt

    with open(result_analyse_file_path, "w") as file:

        segment_length = str(segment_length_sec)
        file.write(segment_length + "\n")
        print(segment_length)

        while start_time < total_length:
            end_time = start_time + segment_length_sec
            if end_time > total_length:
                end_time = total_length

            segment_path = "temp_segment.wav"

            try:
                extract_segment(wav_path, start_time, segment_length_sec, segment_path)
                speech_segment = get_speech_segment(segment_path, recognizer)
                if speech_segment:
                    result = str(start_time) + " " + speech_segment
                    file.write(result + "\n")
                    print(result)
            finally:
                if os.path.exists(segment_path):
                    os.remove(segment_path)

            start_time = end_time

            if interrupt:
                end = str(end_time)
                file.write(end + "\n")
                print(end)
                break

    os.remove(wav_path)

    # Unset signal handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print(f"Removed temporary file {wav_path}")


# Global variable to track if the process should be interrupted
interrupt = False


def main():

    if len(sys.argv) != 2:
        print("missing mp3")
        sys.exit(1)

    mp3_path = sys.argv[1]

    if not os.path.isfile(mp3_path):
        print(f"File not found: {mp3_path}")
        sys.exit(1)

    analyze(mp3_path)


if __name__ == "__main__":
    main()
