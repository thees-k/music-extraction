# Music Extraction

Music Extraction is a Python-based tool designed to extract the segments of an audio file that contains music only.

The basic idea is that if a part of an audio file does not contain any speech (if it's not detectable with **Vosk speech recognition**), it must contain music.

Audio files are at first analyzed, then you can select the segments with no speech (= the segments with music!) and extract them. For extraction **ffmpeg** is used and so there will be no reencoding / quality loss.

Please note that this tool does not work perfect. The start and end the extracted music segments usually contain some spoken words: Maximum 20 seconds of speech at the beginning and end of an extracted music segment.

It has been tested for multiple audio formats including MP3, FLAC, and AAC.
## Features

- **Speech Detection**: Identify and analyze speech segments within audio recordings using the Vosk speech recognition library.
- **Music Segmentation**: Automatically find and extract music segments from audio files.
- **Multi-Format Support**: Process audio files in MP3, FLAC, and AAC formats.
- **Interactive User Interface**: Command-line interface for selecting and confirming music segments to extract.

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system (required for audio processing)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/music-extraction.git
   cd music-extraction
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download and Setup Speech Model**

 
   * Download a speech model that is compatible with Vosk-API (source is https://alphacephei.com/vosk/models)
     * You should download a **small** model for better speed (e.g. `vosk-model-small-de-0.15` for German)!

   * Unpack it in your local directory `~/.local/models/`


### Usage

To analyze an audio file and extract music segments, run the following command:

   ```bash
   python3 music_extraction.py <audio_file> [-a|--analyse]
   ```
* <audio_file>: Path to the audio file to be analyzed.

* -a or --analyse: Optional flag to perform analysis only, without extracting segments.


#### Example

   ```bash
   python3 music_extraction.py test.mp3
   ```
Follow the on-screen prompts to select segments for extraction and specify names for the output files.


### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

* **Vosk Speech Recognition**: This project uses the Vosk library, licensed under the Apache License 2.0. See the LICENSE-APACHE file for details.
* Special thanks to the contributors of the open-source libraries and tools that made this project possible.

### Contact

For any questions or inquiries, please contact yourname.
