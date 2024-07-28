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

    total_length = AudioSegment.from_wav(wav_path).duration_seconds
    total_length_display = seconds_to_min_sec(int(total_length))
    start_time = 0

    is_music_running = False
    music_begin = 0

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
            if is_music_running:
                segments.append((music_begin, end_time, speech_segment))
                is_music_running = False
                print(f"-> Music stop between {seconds_to_min_sec(start_time)} and {seconds_to_min_sec(end_time)} :"
                      f" \"{speech_segment}\"")
        else:
            if not is_music_running:
                music_begin = max(start_time - segment_length_sec, 0)
                is_music_running = True
                print(f"-> Music START between {seconds_to_min_sec(start_time)} and {seconds_to_min_sec(end_time)}")

        os.remove(segment_path)

        start_time = end_time

    if is_music_running:
        segments.append((music_begin, total_length, ""))

    return segments


def seconds_to_min_sec(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02}"


def print_music_segments(segments):
    print("\nMusic segments:")
    for no, segment in enumerate(segments, start=1):
        start, end, speech = segment
        start = int(start)
        end = int(end)
        length = end - start
        print(f"{no}) {seconds_to_min_sec(start)} to {seconds_to_min_sec(end)} -> {seconds_to_min_sec(length)} ({speech})")
        print()


def merge_segments(segments, from_no, to_no):
    return segments[from_no - 1][0], segments[to_no - 1][1], segments[to_no - 1][2]


def get_user_input():
    user_input = input("Enter the segments to keep (e.g., 1,2-3,6): ")
    return "".join(user_input.split())


def parse_user_input(user_input):
    segments_to_keep = []
    parts = user_input.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            segments_to_keep.append((start, end))
        else:
            segments_to_keep.append((int(part), int(part)))
    return segments_to_keep


def combine_segments(segments, segments_to_keep):
    combined_segments = []
    for start, end in segments_to_keep:
        combined_segment = merge_segments(segments, start, end)
        combined_segments.append(combined_segment)
    return combined_segments


def main():
    mp3_path = "./test/integration/fixtures/2024-07-24_ARD Nachtkonzert (BR-Klassik-Rip)_04-02-01.mp3"
    wav_path = "temp_audio.wav"
    convert_mp3_to_wav(mp3_path, wav_path)

    segments = analyze_audio_segments(wav_path)

    os.remove(wav_path)
    print(f"Removed temporary file {wav_path}")

    print_music_segments(segments)

    user_input = get_user_input()
    segments_to_keep = parse_user_input(user_input)
    combined_segments = combine_segments(segments, segments_to_keep)

    print_music_segments(combined_segments)


if __name__ == "__main__":
    main()
