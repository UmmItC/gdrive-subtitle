# gdrive-subtitle

A Python tool for embedding subtitles from Google Drive video captions (JSON format) into video files.

## Description

This tool converts Google Drive JSON subtitle format into SRT format and embeds them into video files using ffmpeg.

## Academic Use Disclaimer

This tool is intended for academic and educational purposes only. It should be used solely for:
- Educational content processing
- Academic research
- Learning purposes

Any other use may be subject to different terms and conditions.

### Requirement

1. Video Share link you can access
2. The video have subtitle
3. You need to manually the the subtitle json file

## Features

- Converts Google Drive JSON subtitle format to SRT
- Handles subtitle timing and synchronization

## Prerequisites

- Python 3.x
- ffmpeg

## Installation

1. Clone the repository:

```bash
git clone https://github.com/UmmItC/gdrive-subtitle.git
cd gdrive-subtitle
```

2. Ensure ffmpeg is installed on your system.

```bash
paru -S ffmpeg
```

## Usage
o
```bash
python embed_subtitles.py --source <video_file> --json <json_file> --output <output_file>
```

Example:
```bash
python embed_subtitles.py --source lecture.mp4 --json timedtext.json --output lecture_with_subtitles.mp4
```

The script will:

1. Convert the specified JSON subtitle file to SRT format
2. Embed the subtitles into your video
3. Save the output with the specified filename

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3) - see the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.