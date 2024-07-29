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
    user_input = input("Enter the segments to keep (e.g., 1,2-3,6) or press the Enter key to keep all: ")
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


def split_mp3(mp3_path, segments):
    for i, (start, end, _) in enumerate(segments, start=1):
        output_path = f"output_segment_{i}.mp3"
        command = f'ffmpeg -loglevel error -ss {start} -to {end} -i "{mp3_path}" -c copy "{output_path}"'
        subprocess.call(command, shell=True)
        print(f"Exported segment {i} from {seconds_to_min_sec(start)} to {seconds_to_min_sec(end)} to {output_path}")


def main():
    mp3_path = "./test/integration/fixtures/2024-07-24_ARD Nachtkonzert (BR-Klassik-Rip)_04-02-01.mp3"
    # wav_path = "temp_audio.wav"
    # convert_mp3_to_wav(mp3_path, wav_path)
    #
    # segments = analyze_audio_segments(wav_path)
    #
    # os.remove(wav_path)
    # print(f"Removed temporary file {wav_path}")

    segments = list()
    segments.append((80, 880, "das war Johann Sebastian Bachs Orgel Passacaglia in c-Moll Werke Verzeichnis 582 in einer Version mit dem Philadelphia Orchestra unter"))
    segments.append((880, 1680, "yaara Tal und Andreas Grothusen interpretierten die Suite für 2 Klaviere Opus 6 von Schalke klar hier im ARD Nachtkonzert und es geht"))
    segments.append((1680, 1760, "+ 400 € tschüss"))
    segments.append((1740, 1820, "Julie Ute tschüss tschüss"))
    segments.append((1800, 2600, "Knoxville summer of nineteen fifteen eine Szene für Sopran und Orchester von Samuel Barber mit Kathleen Battle und dem Orchester andre preven wie versprochen Wiener Klassik am Ende der Stunde"))
    segments.append((2600, 3280, "ok Google"))
    segments.append((3260, 3360, "das war die Sinfonie in G-Dur von Wolfgang Amadeus Mozart Köchelverzeichnis 124 zum Besten gegeben vom English Chamber Orchestra geleitet von Jeffrey Tate"))
    segments.append((3360, 3500, "ARD Nachtkonzert es ist 5 Uhr vom Bayerischen Rundfunk hören Sie Nachrichten im Studio Sissi Förster in den USA ist die demokratische Präsidentschaftsbewerber Harris angriffslustig in den Wahlkampf startet vor jubelnden"))
    segments.append((3580, 3600, ""))

    print_music_segments(segments)

    user_input = get_user_input()
    if user_input == "":
        combined_segments = segments
    else:
        segments_to_keep = parse_user_input(user_input)
        combined_segments = combine_segments(segments, segments_to_keep)

    print_music_segments(combined_segments)

    if not input("Do you want to split the MP3 based on these segments? (Y/n): ").lower() == 'n':
        split_mp3(mp3_path, combined_segments)


if __name__ == "__main__":
    main()
