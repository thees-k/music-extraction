# Music Extraction

Music Extraction is a Python-based command line tool designed to extract the parts of an audio file that contain music only.

It uses **Vosk speech recognition** and **Silero VAD** (voice activity detector). 

So far it has been tested for multiple audio formats including MP3, FLAC, and AAC.

## Description

An audio file is analyzed in 20-second segments with the help of **Vosk Speech Recognition**. Speech is searched for in the individual 20-second segments. Any speech found (transcription) is saved in the analysis (text) file that is created for each audio file (`.speech` extension).

The analysis of a one-hour audio file takes about 2 minutes.

Execute the script with:
```bash
$ python3 music_extraction.py <audio_file>
```

**Phase 1**: Analysis

```bash
$ python3 music_extraction.py MyRadioRecording.mp3

Full analysis
Create analysable audio file...
Analysing audio segments... (Press Ctrl+C to interrupt)
0:00 bin grad unter mittwoch viel sonne zwölf bis neun zehn grad es ist elf uhr vier ndr kultur das konzert
0:20 dazu begrüße heute rallye zar nikolaus schönen guten morgen von hildesheim und hannover aus in die welt die dirigenten johanna mai witz achtunddreißig jahre ist sie jung als chefin des konzerthauses berlin sorgt sie für viel aufsehen im herbst vergangenen jahres gastierte sie zum ersten mal beim ndr
0:40 die philharmonie orchester und war auch im gespräch zu erleben bei uns da sagte sie ein gutes programm ist eine mischung aus dramaturgisch umdenken und bauchgefühl wenn es gut geht entsteht ein flow auf der bühne wie im publikum dieser flow entstand mit rachmaninow legendärem drittem
1:00 wir konzert mit anna wie netz karriere im zentrum und was packt man zu diesem mount everest der klavierkonzert literatur das wollte natürlich gut überlegt sein sagt johanna mal witz und hat sich für zwei werke von sultan corday als rahmen entschieden sultan wer werden sich leid
1:20 einige fragen und daher es genau möchte die dirigentin mit dem ndr elbphilharmonie orchester ändern ihre leidenschaft für diese musik weitergeben mit der haare janosch street einer märchen erzählung zum abschluss und mit den tänzen aus galant h zu begehen wir erfahren nachher was in uns
1:40 jahren ein niesen vor beginn einer erzählung bedeutet erlernen johanna mal witz näher kennen im gespräch mit stefan sturm und wir erfahren was für sie hollywood für symphonieorchester bedeutet jetzt die tänze aus galanter von sultan corday ein gutes beispiel für seine klang sprache neunzehnhundertdreiunddreißig
2:00 ich entstanden in erinnerung an seine kindheit im vorwort zur partitur schreibt er galanter ist ein kleiner ungarischer marktflecken an der alten bahnstrecke wien budapest sieben jahre hatte dort verbracht als kind und die auftritte der dortigen musiker beeindruckten in
2:20 tief in seinen tänzen werden wir hin und her geworfen zwischen melancholie und humor die kontraste charakterisieren diese musik das nr älpler orchester spielt unter leitung von johanna mal letz
3:00 (of 116:02)...
4:00 (of 116:02)...
5:00 (of 116:02)...
6:00 (of 116:02)...
7:00 (of 116:02)...
8:00 (of 116:02)...
9:00 (of 116:02)...
10:00 (of 116:02)...
11:00 (of 116:02)...
12:00 (of 116:02)...
13:00 (of 116:02)...
14:00 (of 116:02)...
15:00 (of 116:02)...
16:00 (of 116:02)...
17:00 (of 116:02)...
18:00 (of 116:02)...
19:00 die tänze aus galanter von sultan corday der um jubelte einstand der dirigentin johanna mal witz beim ndr elbphilharmonie orchester am ersten oktober zweitausenddrei und
19:20 ich im großen saal der elbphilharmonie in hamburg solistin wadi pianistin anna wie netz ca ja sie hat aus anlass des hundert fünfzigsten geburtstag ihres landsmanns rachmaninow im vergangenen jahr alle vier konzerte gespielt mit dem ndr elf harmonie orchester am ersten oktober war das dritte dran
19:40 und johanna mal witz spricht beim rasch drei von einem der monströsesten klavierkonzerte die es überhaupt gibt das spielen zu können sei schon viel aber anna wie netz kein schaffe es bei allem noch eine leichtigkeit und eine natürlichkeit und eine gesang lichkeit zu haben bei diesem
20:00 mount everest unter den klavierkonzerten und sie weist daraufhin dass das konzert sehr symphonisch komponiert ist der solo part sehr verwoben mit dem orchester da passiert unheimlich viel unterschiedliches mit sehr viel material auch für das orchester sei es eine herausforderung falls
20:20 denn nicht nur begleitet und anna wie netz geier natürlich fire braucht man ganz viel energie bei solche konzerte vor allem weil es einfach schon am zeitliche liegenden geht das als ist es dann nicht normalerweise man gewöhnt sich am dreißig fünfunddreißig minuten da muss man hier lenker spiel
20:40 aber ich würde sagen so viele noten die da komponiert hat sie gar nicht so wichtig also diesen oft sehr atmosphärisch oft nur für die farbe da und das große melodie linie muss man natürlich behalten mit sinken mitfühlen und dann ist es ja
21:00 da eigentlich mans spürt dieser ganz im norden nicht sie sind einfach dafür da die melodien zu helfen sergei rachmaninow hat auf der überfahrt nach new york stumm geübt ohne klavier geht das überhaupt so ein konzerts stumm zu üben mit meiner war so daten recht dass die ganz erreicht
21:20 dessen vielen gewahren als heutzutage er hat immer nicht nur für drittes reich meine wach hat immer seine stumme klaviatur mit sich grabt um zu üben weil die am anfang an seine karriere seinem technik war nicht so gut ausgeprägt ihm hat es nicht so gut gefallen oder technische fähigkeiten
21:40 weil bei ihm war nicht so perfekt fahrende er und an hat er angefangen sich zu verbessern technisch und deswegen diese ganze stimme klaviatur und dass er dann wie verrückter in einer so zeit wo er ziemlich jungfer geübt hat und die ergebnisse kann man sich bis heute anhören was die interpretation angeht kann man sich auf man
22:00 und selbst berufen der hat alle konzerte aufgenommen und dass es für mich vorbild wie man rasch meiner spielen muss natürlich ich kapieren dass es auch unmöglich sein art seine interpretationen zu kopieren aber man spürt wenn man seine aufnahme ich ort in welche richtung er geht also mein sein
22:20 die musik das eigentlich diese ganz er rabatt hier und auch die tempel unterschiede sind kaum zu merken seine musik ist im rahmen der so ziemlich rhythmisch aber in diese rahmen basiert soviel drosseln an sich dass es säße klassisch komponiert anna wie netz geier unter
22:40 des ndr elbphilharmonie orchester spielen unter leitung von johanna mal witz das klavierkonzert nummer drei von das hergé rachmaninow es steht in d moll und die besteigung des mount everest beginnt mit einer denkbar schlichten melodie
23:00 (of 116:02)...
24:00 (of 116:02)...
25:00 (of 116:02)...
26:00 (of 116:02)...
27:00 (of 116:02)...
...
```

**Phase 2**: The results are presented to the user on the console. The user can combine and select segments.

```bash
Music segments:
1)
2:20 tief in seinen tänzen werden wir hin und her geworfen zwischen melancholie und humor die kontraste charakterisieren diese musik das nr älpler orchester spielt unter leitung von johanna mal letz
19:20 die tänze aus galanter von sultan corday der um jubelte einstand der dirigentin johanna mal witz beim ndr elbphilharmonie orchester am ersten oktober zweitausenddrei und
17:00

2)
22:40 des ndr elbphilharmonie orchester spielen unter leitung von johanna mal witz das klavierkonzert nummer drei von das hergé rachmaninow es steht in d moll und die besteigung des mount everest beginnt mit einer denkbar schlichten melodie
63:20 analytiker und das ndr elbphilharmonie orchester dirigiert von johanna mal witz mit dem klavierkonzert nummer drei d moll von fake fachmann noch sie hören das konzert auf ndr kultur heute eine aufnahme aus der elbphilharmonie in hamburg vom er
40:40

3)
63:40 du gabe aus den e typ tableau opus neununddreißig von rachmaninow das fünfte in es moll
69:00 die zugabe von einer wie netz geier in der hamburger elbphilharmonie am ersten oktober zweitausend dreiundzwanzig e typ tableau es neue von säge rachmaninow auf aus seinem opus neununddreißig johanna mal witz ist eine viel beachtete dirigent
5:20

4)
77:40 dusche seine wahre natur ist nachdenklich gehören die haare janosch suite von sollte an call a in der aufnahme vom ersten oktober vergangenen jahres in der elbphilharmonie johanna mal witz am puls des ndr elbphilharmonie orchesters
102:20 das war die haare janus fühlt von sollten corday gespielt vom ende her elbphilharmonie orchester unter der leitung von johanna mal wilds eine aufnahme vom ersten oktober zweitausenddrei uns fand sich hier auf ndr kultur im konzert und
24:40

5)
102:40 das begleitet von jenny yang jun grau mit dem ersten satz der r p g ohne sonate von franz schubert
111:00 der erste satz der betone sonate von franz schubert mit christopher franziskus und jäh nie ja nun gar o meiner mistral liter nikolaus ich wünsche ihnen noch einen sehr schönen sonntag mit brahms
8:20

6)
110:40 der erste satz der betone sonate von franz schubert mit christopher franziskus und jäh nie ja nun gar o meiner mistral liter nikolaus ich wünsche ihnen noch einen sehr schönen sonntag mit brahms
116:02.233 ...
5:22.233

Enter the segments to keep (e.g., 1,2-3,6) or press the Enter key to keep all: 
```
Several of these segments can be combined. This is useful because some pieces of music also contain speech (e.g. opera arias) and because Vosk Speech Recognition sometimes incorrectly detects speech (false positives).

**Phase 3**: Extraction & Fine-Tuning

After the user set the name for extractions, the script will extract the segments and do fine-tuning and, if the audio file is MP3, execute `mp3gain`.

Here I entered "Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz" as the name:

```bash
Selected segments okay? (Y/n): Y
Specify a name for the extraction segments or press the Enter key for default naming ("extraction"): Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz
Exported 01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3 from ~2:20 to ~19:20 (16:33.949)
01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3
Applying mp3 gain change of 4 to 01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3...
01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3
Applying mp3 gain change of 4 to 01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3...
Exported 02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3 from ~22:40 to ~63:20 (40:06.932)
02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3
Applying mp3 gain change of 4 to 02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3...
02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3
Applying mp3 gain change of 4 to 02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3...
Exported 03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3 from ~63:40 to ~69:00 (4:54.138)
03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3
Applying mp3 gain change of 4 to 03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3...
03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3
Applying mp3 gain change of 4 to 03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3...
Exported 04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3 from ~77:40 to ~102:20 (24:06.836)
04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3
Applying mp3 gain change of 4 to 04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3...
04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3
Applying mp3 gain change of 4 to 04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3...
Exported 05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3 from ~102:40 to ~111:00 (7:51.364)
05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3
Applying mp3 gain change of 5 to 05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3...
05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3
Applying mp3 gain change of 4 to 05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3...
Exported 06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3 from ~110:40 to ~116:02.233 (5:04.917)
06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3
Applying mp3 gain change of 3 to 06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3...
06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3
Applying mp3 gain change of 3 to 06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3...
```
The selected segments are  extracted from the audio file via `ffmepg` **without re-encoding/loss of quality**!

**Fine-Tuning**: The voice at the beginning and end of the selected segments are removed using **Silero VAD**.

For MP3s, the volume is normalized at the end using `mp3gain`.

**Results:**

```bash
$ ls -lha

total 703M
drwxrwxr-x  2 thees thees 4,0K Nov  6 12:25  .
drwxrwxr-x 13 thees thees 4,0K Okt 29 09:02  ..
-rw-rw-r--  1 thees thees  28M Nov  6 12:24 '01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3'
-rw-rw-r--  1 thees thees  29M Nov  6 12:24 '01_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3'
-rw-rw-r--  1 thees thees  66M Nov  6 12:24 '02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3'
-rw-rw-r--  1 thees thees  67M Nov  6 12:24 '02_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3'
-rw-rw-r--  1 thees thees 8,0M Nov  6 12:24 '03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3'
-rw-rw-r--  1 thees thees 8,6M Nov  6 12:24 '03_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3'
-rw-rw-r--  1 thees thees  41M Nov  6 12:24 '04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3'
-rw-rw-r--  1 thees thees  41M Nov  6 12:24 '04_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3'
-rw-rw-r--  1 thees thees  13M Nov  6 12:24 '05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3'
-rw-rw-r--  1 thees thees  14M Nov  6 12:24 '05_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3'
-rw-rw-r--  1 thees thees 8,1M Nov  6 12:25 '06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz.mp3'
-rw-rw-r--  1 thees thees 8,4M Nov  6 12:25 '06_Konzert Vinnitskaya, NDR Elbphilharmonie, Johanna Mallwitz_with_speech.mp3'
-rw-rw-r--  1 thees thees 188M Nov  6 12:10  MyRadioRecording.mp3
-rw-rw-r--  1 thees thees  16K Nov  6 12:15  MyRadioRecording.speech
```

 The .speech file (here MyRadioRecording.speech) contains the audio analysis. It can be reuse for later re-extractions.

**The new audio files are the results of the extraction process.** They are numbered. For each file a file that ends with "_with_speech" exists. That are the extracted files without fine-tuning. They usually contain speech at the beginning and at the end. Sometimes it is necessary to have them and therefore they are not deleted. 


## Installation

### Prerequisites

- Python 3.12 or higher
- `ffmpeg` installed on your system (required for audio processing)
- `mp3gain` in case you want to extract from MP3s

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
   python3 music_extraction.py <audio_file> [-a|--analyse] [-b LESS_SILENCE_BEGINNING] [-e LESS_SILENCE_END] [-h]
   ```
* <audio_file>: Path to the audio file to be analyzed.

* -a or --analyse: Flag to perform analysis only, without extracting segments. Creates the .speech file only.
* -b LESS_SILENCE_BEGINNING Less silence at the beginning of the trimmed audio file in seconds
* -e LESS_SILENCE_END Less silence at the end of the trimmed audio file in seconds
* -h, --help shows help message and exit


### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

* **Vosk Speech Recognition**: This project uses the Vosk library, licensed under the Apache License 2.0. See the LICENSE-APACHE file for details.
* **Silero VAD**: MIT license
* Special thanks to the contributors of the open-source libraries and tools that made this project possible.
 
