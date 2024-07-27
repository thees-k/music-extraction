import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr


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


def analyze_audio_segments(wav_path, segment_length_sec=20):
    recognizer = sr.Recognizer()
    segments = []
    music_segments = []

    total_length = AudioSegment.from_wav(wav_path).duration_seconds
    total_length_display = seconds_to_min_sec(int(total_length))
    start_time = 0

    is_music = True

    while start_time < total_length:
        end_time = start_time + segment_length_sec
        if end_time > total_length:
            end_time = total_length

        segment_path = "temp_segment.wav"
        if start_time % 60 == 0:
            print(f"Timestamp {seconds_to_min_sec(start_time)} (of {total_length_display})...")
        extract_segment(wav_path, start_time, segment_length_sec, segment_path)

        speech_segment = get_speech_segment(segment_path, recognizer)
        if speech_segment:
            if is_music:
                is_music = False
                print(f"-> Music stop between {seconds_to_min_sec(start_time)} and {seconds_to_min_sec(end_time)} :"
                      f" \"{speech_segment}\"")
        else:
            segments.append((start_time, end_time))
            if not is_music:
                is_music = True
                print(f"-> Music START between {seconds_to_min_sec(start_time)} and {seconds_to_min_sec(end_time)}")

        os.remove(segment_path)

        start_time = end_time

    if not segments:
        return music_segments

    music_start = segments[0][0]
    for i in range(1, len(segments)):
        if segments[i][0] != segments[i - 1][1]:
            music_end = segments[i - 1][1]
            music_segments.append((music_start, music_end))
            music_start = segments[i][0]
    music_segments.append((music_start, segments[-1][1]))

    return music_segments


def seconds_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02}"


def print_music_segments(segments):
    print("\nMusic segments:")
    for start, end in segments:
        start = int(start)
        end = int(end)
        length = end - start
        print(f"Music from {seconds_to_min_sec(start)} to {seconds_to_min_sec(end)} -> {seconds_to_min_sec(length)}")


def main():
    mp3_path = "./test/integration/fixtures/2024-07-24_ARD Nachtkonzert (BR-Klassik-Rip)_04-02-01.mp3"
    wav_path = "temp_audio.wav"
    convert_mp3_to_wav(mp3_path, wav_path)

    segments = analyze_audio_segments(wav_path)
    print_music_segments(segments)

    os.remove(wav_path)
    print(f"Removed temporary file {wav_path}")


if __name__ == "__main__":
    main()
