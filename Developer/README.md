# Video Processing Toolkit

A comprehensive toolkit for video processing, text-to-video conversion, and YouTube automation.

## Features

- Video processing and manipulation
- Text-to-video conversion
- Audio processing
- YouTube upload automation
- Image and GIF processing
- Video merging capabilities

## Project Structure

```
Developer/
├── src/
│   ├── utils/      # Utility functions and helpers
│   ├── video/      # Video processing modules
│   ├── audio/      # Audio processing modules
│   ├── text/       # Text processing modules
│   └── platforms/  # Platform-specific code (YouTube, etc.)
├── config/         # Configuration files
└── tests/          # Test files
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure YouTube API credentials:
   - Place your `google_sec.json` in the root directory
   - Run any YouTube-related script to authenticate

## Usage

### Text to Video Conversion

```bash
python src/text/text_processor.py --name output_name
```

### YouTube Upload

```bash
python src/platforms/youtube.py --video video_name
```

### Video Merging

```bash
python src/video/video_merger.py --input video1.mp4 video2.mp4 --output merged.mp4
```

## Configuration

All configuration settings can be found in `config/config.py`. Modify these settings according to your needs.

## License

This project is proprietary and confidential.
