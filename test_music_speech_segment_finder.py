from unittest import TestCase
from music_speech_segments_finder import find, MusicSegment

class TestMusicSpeechSegmentsFinder(TestCase):

    def test_find_one_segment(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "60 at 60",
                 "80 at 80",
                 "end"]
        total_length = 100
        expected_segments = [
            MusicSegment(20, "at 20", 100, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_two_segments(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "60 at 60",
                 "80 at 80",
                 "end"]
        total_length = 120
        expected_segments = [
            MusicSegment(20, "at 20", 100, "at 80"),
            MusicSegment(80, "at 80", 120, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_no_segment(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60",
                 "end"]
        total_length = 80
        expected_segments = []
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_three_segments(self):
        lines = ["20",
                 "20 at 20",
                 "60 at 60",
                 "80 at 80",
                 "end"]
        total_length = 120
        expected_segments = [
            MusicSegment(0, "...", 40, "at 20"),
            MusicSegment(20, "at 20", 100, "at 80"),
            MusicSegment(80, "at 80", 120, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_no_speech_at_all(self):
        lines = ["20",
                 "end"]
        total_length = 120
        expected_segments = [
            MusicSegment(0, "...", 120, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_no_music_at_all(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "end"]
        total_length = 60
        expected_segments = []
        self.assertEqual(expected_segments, find(lines, total_length))
