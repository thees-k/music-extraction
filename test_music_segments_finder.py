from unittest import TestCase
from music_segments_finder import find, MusicSegment


class TestMusicSegmentsFinder(TestCase):
    def test_find(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "60 at 60"]
        total_length = 80
        expected_segments = [
            MusicSegment(20, "at 20", 80, "at 60")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_nothing_to_find(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60"]
        total_length = 80
        expected_segments = []
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_complete(self):
        lines = ["20"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "...", 80, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_begin(self):
        lines = ["20",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "...", 40, "at 40")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_end(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40"]
        total_length = 80
        expected_segments = [
            MusicSegment(40, "at 40", 80, "...")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_several(self):
        lines = ["20",
                 "0 at 0",
                 "40 at 40",
                 "80 at 80"]
        total_length = 100
        expected_segments = [
            MusicSegment(0, "at 0", 60, "at 40"),
            MusicSegment(40, "at 40", 100, "at 80")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_at_end_with_greater_total_length(self):
        lines = ["20",
                 "0 at 0",
                 "20 at 20",
                 "40 at 40",
                 "60 at 60"]
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
                 "60 at 60"]
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
                 "50 at 50"]
        total_length = 60
        expected_segments = [
            MusicSegment(30, "at 30", 60, "at 50")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_several_and_one_at_begin(self):
        lines = ["20",
                 "20 at 20",
                 "60 at 60"]
        total_length = 80
        expected_segments = [
            MusicSegment(0, "...", 40, "at 20"),
            MusicSegment(20, "at 20", 80, "at 60")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_several_and_one_at_end(self):
        lines = ["20",
                 "0 at 0",
                 "40 at 40"]
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
                 "120 at 120"]
        total_length = 140
        expected_segments = [
            MusicSegment(20, "at 20", 120, "at 100")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))

    def test_find_several_with_longer_speeches(self):
        lines = ["20",
                 "0 hello world!",
                 "40 at this is a very long text that makes no sense",
                 "80 at all. Year. Blabla"]
        total_length = 100
        expected_segments = [
            MusicSegment(0, "hello world!", 60, "at this is a very long text that makes no sense"),
            MusicSegment(40, "at this is a very long text that makes no sense", 100, "at all. Year. Blabla")
        ]
        self.assertEqual(expected_segments, find(lines, total_length))
