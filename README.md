# YouTube Video Transcript Extractor

A Python script that extracts transcripts from YouTube videos given their URLs.

## Features

- Extracts transcripts from YouTube videos
- Supports multiple YouTube URL formats
- Handles multiple languages (defaults to English)
- Falls back to auto-generated captions if manual transcripts aren't available
- Saves transcript to a text file
- Comprehensive error handling

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python youtube_transcript_extractor.py <youtube_url>
```

### Example

```bash
python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

## Output

The script will:

1. Display the transcript in the terminal
2. Save the transcript to a file named `transcript_VIDEO_ID.txt`
3. Show transcript statistics (character count)

## Error Handling

The script handles various error scenarios:

- Invalid YouTube URLs
- Videos without available transcripts
- Private or restricted videos
- Network connectivity issues

## Requirements

- Python 3.6+
- youtube-transcript-api

## Notes

- The script prioritizes manual transcripts over auto-generated ones
- If English transcripts aren't available, it will try other available languages
- Some videos may not have transcripts available at all
