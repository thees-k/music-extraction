from unittest import TestCase
from music_segments_finder import find, MusicSegment


class TestMusicSegmentsFinder(TestCase):
    def test_find_segment_in_middle(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "60 at 60",
                 "end"]
        total_length = 80
        expected_segments = [
            MusicSegment(20, "at 20", 80, "at 60")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_no_segments(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60",
                 "end"]
        total_length = 80
        expected_segments = []
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_largest_possible_segment(self):
        lines = ["20",
                 "end"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "...", 80, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_segment_at_begin(self):
        lines = ["20",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60",
                 "end"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "...", 40, "at 20")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_segment_at_end(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "end"]
        total_length = 80
        expected_segments = [
            MusicSegment(40, "at 40", 80, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_several_segments_in_the_middle(self):
        lines = ["20",
                 "0 at 0",
                 "40 at 40",
                 "80 at 80",
                 "end"]
        total_length = 100
        expected_segments = [
            MusicSegment(0, "at 0", 60, "at 40"),
            MusicSegment(40, "at 40", 100, "at 80")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_segment_with_greater_total_length(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60",
                 "end"]
        total_length = 90
        expected_segments = [
            MusicSegment(60, "at 60", 90, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_end_with_slightly_greater_total_length(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60",
                 "end"]
        total_length = 80.1
        expected_segments = [
            MusicSegment(60, "at 60", 80.1, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_with_smaller_segment_length(self):
        lines = ["10",
                 "0 at 0",
                 "10 at 10",
                 "20 at 20",
                 "30 at 30",
                 "50 at 50",
                 "end"]
        total_length = 60
        expected_segments = [
            MusicSegment(30, "at 30", 60, "at 50")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_begin_and_in_the_middle(self):
        lines = ["20",
                 "20 at 20",
                 "60 at 60",
                 "end"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "...", 40, "at 20"),
            MusicSegment(20, "at 20", 80, "at 60")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_in_the_middle_and_at_end(self):
        lines = ["20",
                 "0 at 0",
                 "40 at 40",
                 "end"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "at 0", 60, "at 40"),
            MusicSegment(40, "at 40", 80, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_greater_segment(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "100 at 100",
                 "120 at 120",
                 "end"]
        total_length = 140
        expected_segments = [
            MusicSegment(20, "at 20", 120, "at 100")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_several_segments_with_longer_speeches(self):
        lines = ["20",
                 "0 hello world!",
                 "40 at this is a very long text that makes no sense",
                 "80 at all. Year. Blabla",
                 "end"]
        total_length = 100
        expected_segments = [
            MusicSegment(0, "hello world!", 60, "at this is a very long text that makes no sense"),
            MusicSegment(40, "at this is a very long text that makes no sense", 100, "at all. Year. Blabla")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_begin_in_middle_and_with_greater_total_length(self):
        lines = ["20",
                 "20 at 20",
                 "40 at 40",
                 "100 at 100",
                 "end"]
        total_length = 130
        expected_segments = [
            MusicSegment(0, "...", 40, "at 20"),
            MusicSegment(40, "at 40", 120, "at 100"),
            MusicSegment(100, "at 100", 130, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_begin_in_middle_and_with_slightly_greater_total_length(self):
        lines = ["20",
                 "20 at 20",
                 "40 at 40",
                 "100 at 100",
                 "end"]
        total_length = 120.1
        expected_segments = [
            MusicSegment(0, "...", 40, "at 20"),
            MusicSegment(40, "at 40", 120, "at 100"),
            MusicSegment(100, "at 100", 120.1, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_no_segments_with_smaller_total_length(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60",
                 "end"]
        total_length = 70
        expected_segments = []
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_segment_at_end_with_smaller_total_length(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "end"]
        total_length = 70
        expected_segments = [
            MusicSegment(40, "at 40", 70, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_segment_in_middle_with_continue_marker(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "60 at 60",
                 "80"]
        total_length = 120
        expected_segments = [
            MusicSegment(20, "at 20", 80, "at 60"),
            MusicSegment(60, "at 60", 120, "...")
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
