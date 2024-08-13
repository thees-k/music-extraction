# Music Extraction

Music Extraction is a Python-based command line tool designed to extract the parts of an audio file that contain music only.

**The basic idea is** that if a part of an audio file does not contain any speech (if there is no speech according to **Vosk speech recognition**), it must contain only music.

Audio files are at first analyzed, then you can select the segments with no speech (= the segments with music!) and extract them. For extraction `ffmpeg` is used and so there will be **no re-encoding / quality loss**.

Please note that this tool does not work perfect. The start and end the extracted music segments usually contain some spoken words (maximum 20 seconds of speech at the beginning and at the end).

So far it has been tested for multiple audio formats including MP3, FLAC, and AAC.

## Description

An audio file is analyzed in 20-second segments. Speech is searched for in the individual 20-second segments. Any speech found (transcription) is saved in the analysis (text) file that is created for each audio file (`.speech` extension).

A 20-second segment without speech is regarded as a segment with music only.

The analysis of a one-hour audio file takes about 2 minutes.

**Analysis Phase:**
```bash
    $ python3 ~/bin/music_extraction/music_extraction.py MyRadioRecording.mp3
    Full analysis
    Create analysable audio file...
    Analysing audio segments... (Press Ctrl+C to interrupt)
    0:00 nach zeitweise klare in der zweiten nacht hilfe von westen her schnee tiefstwerte null bis minus acht grad und die weiteren aussichten morgen erst schnee dann von westen her regen sonntag und montag weiter bewölkt und örtlich etwas schnee nächtliche tiefstwerte plus zwei bis minus zwei und tages höchstwerte null bis acht
    0:20 hat soweit die nachricht dass es zwanzig uhr vier d r klassik konzerte abend herzlich willkommen dazu ich bin clemens nicole schön dass sie an diesem freitag abend mit dabei sind von neunzehnhundert einundsechzig bis neun
    0:40 hunderte neunundsiebzig war rafael kugelig der tschechische schweizer oder der schweizerische tscheche chefdirigent beim sinfonieorchester des bayerischen rundfunks und danach noch bis neunzehnhundertdreiundachtzig ständiger gast dirigent dieses orchesters und aus dieser zeit stammen alle aufnahmen vom heute
    1:00 die konzert abend hier auf bea klassik im programm unter anderem cube links kantate ohne worte er hat ja auch selbst komponiert und zum beispiel auch die lu die symphonie archie von jan no vag der hätte in diesen tagen seinen ein hundertsten geburtstag gefeiert wir beginnen aber mit einer
    1:20 sinfonia von layer jana check anlass dieser komposition war der kongress eines sportvereins im jahr neunzehnhundertsechsundzwanzig da hatte man sich vor allem von fahren musik gewünscht das hat ja natürlich auch natürlich sofort eingelöst und deshalb sind die blechbläser in dieser sind von jette auch
    1:40 sehr gut besetzt hören wir dass symphonie orchester des bayerischen rundfunks unter rafael kuby liegt in einer aufnahme aus dem jahr neunzehnhunderteinundachtzig
    2:00 (of 116:03)...
    3:00 (of 116:03)...
    4:00 (of 116:03)...
    5:00 (of 116:03)...
    6:00 (of 116:03)...
    7:00 (of 116:03)...
    8:00 (of 116:03)...
    9:00 (of 116:03)...
    10:00 (of 116:03)...
    11:00 (of 116:03)...
    12:00 (of 116:03)...
    13:00 (of 116:03)...
    14:00 (of 116:03)...
    15:00 (of 116:03)...
    16:00 (of 116:03)...
    17:00 (of 116:03)...
    18:00 (of 116:03)...
    19:00 (of 116:03)...
    20:00 (of 116:03)...
    21:00 (of 116:03)...
    22:00 (of 116:03)...
    23:00 (of 116:03)...
    24:00 (of 116:03)...
    25:00 applaus für die sinfonie etat von lausche jana check
    25:20 denn aufnahme mit dem orchester des bayerischen rundfunks unter der leitung von rafael q beleg vom sechzehnte oktober neunzehnhunderteinundachtzig im münchner herkules saal der residenz gleich zwanzig dreißig hier es der konzert abend auf br klassik an diesem freitag abend und wir machen weiter mit aufnahmen
    25:40 von sinfonieorchester des b rund rafael kugelig dem ehemaligen chefdirigenten und haben jetzt für sie eine fantasia konzertante eigentlich ein klavierkonzert in b dur von boshaft martino wir herrn als solistin die pianistin margaret weber
    26:00 (of 116:03)...
    27:00 (of 116:03)...
    28:00 (of 116:03)...
    29:00 (of 116:03)...
    30:00 (of 116:03)...
    ...
```

Once the audio file has been analyzed, the music segments found are listed. The music segments found consist of several consecutive 20-second segments of the audio file.

As a rule, a found music segment begins with a 20-second segment in which speech was found, followed by one or more 20-second segments in which no speech was found (i.e. which only contain music), and at the end there is another 20-second segment in which speech was found.
**Explanation:** In the first segment in which speech was found, the speaker has usually stopped speaking at some point and the music has started. Since the beginning of the music should not be cut off, this segment must be included. As the music should not be cut off at the end either, the end of a found music segment must also be a 20-second segment in which speech was found. 

It is quite possible that speech is found in a 20-second segment even though there is none (false positive), e.g. especially in music with vocals.

The user can therefore combine several music segments after the analysis phase.

**Selecting and Combining Found Music Segments:**
```bash
    Music segments:
    1)
    1:40 sehr gut besetzt hören wir dass symphonie orchester des bayerischen rundfunks unter rafael kuby liegt in einer aufnahme aus dem jahr neunzehnhunderteinundachtzig
    25:20 applaus für die sinfonie etat von lausche jana check
    23:40
    
    2)
    25:40 von sinfonieorchester des b rund rafael kugelig dem ehemaligen chefdirigenten und haben jetzt für sie eine fantasia konzertante eigentlich ein klavierkonzert in b dur von boshaft martino wir herrn als solistin die pianistin margaret weber
    48:00 die pianistin market weber zusammen mit dem symphonie orchester des bayerischen rundfunks unter der leitung von rafael kugelig mit der fantasia konzertante einem klavierkonzert in b dur von
    22:20
    
    3)
    49:00 melodien und motiven dieses werkes herausführen kann hier nochmal das sinfonieorchester des bayerischen rundfunks unter rafael q beleg mit tv schatz wassermann
    53:40 die modetrends ressort mit wurde der nähe
    4:40
    
    4)
    53:20 die modetrends ressort mit wurde der nähe
    65:40 der wassermann eine sinfonische dichtung von antonin war jacques in einer aufnahme mit dem symphonieorchester des bayerischen rundfunks unter seinem chefdirigenten beziehungsweise ehemaligen chefdirigenten rafael kugelig hier im konzert abend auf br
    12:20
    
    Enter the segments to keep (e.g., 1,2-3,6) or press the Enter key to keep all: 1,2,3-4
```

The user can then assign a name for the music segments to be extracted and the music segments can be extracted without re-encoding/loss of quality:

```bash
    Music segments:
    1)
    1:40 sehr gut besetzt hören wir dass symphonie orchester des bayerischen rundfunks unter rafael kuby liegt in einer aufnahme aus dem jahr neunzehnhunderteinundachtzig
    25:20 applaus für die sinfonie etat von lausche jana check
    23:40
    
    2)
    25:40 von sinfonieorchester des b rund rafael kugelig dem ehemaligen chefdirigenten und haben jetzt für sie eine fantasia konzertante eigentlich ein klavierkonzert in b dur von boshaft martino wir herrn als solistin die pianistin margaret weber
    48:00 die pianistin market weber zusammen mit dem symphonie orchester des bayerischen rundfunks unter der leitung von rafael kugelig mit der fantasia konzertante einem klavierkonzert in b dur von
    22:20
    
    3)
    49:00 melodien und motiven dieses werkes herausführen kann hier nochmal das sinfonieorchester des bayerischen rundfunks unter rafael q beleg mit tv schatz wassermann
    65:40 der wassermann eine sinfonische dichtung von antonin war jacques in einer aufnahme mit dem symphonieorchester des bayerischen rundfunks unter seinem chefdirigenten beziehungsweise ehemaligen chefdirigenten rafael kugelig hier im konzert abend auf br
    16:40
    
    Selected segments okay? (Y/n): 
    Specify a name for the extraction segments or press the Enter key for default naming ("extraction"): BRSO+Kubelik
    Exported 01_BRSO+Kubelik.mp3 from 1:40 to 25:20 (23:40)
    Exported 02_BRSO+Kubelik.mp3 from 25:40 to 48:00 (22:20)
    Exported 03_BRSO+Kubelik.mp3 from 49:00 to 65:40 (16:40)
```








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
   pip3 install -r requirements.txt
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
