#!/usr/bin/env python3
"""
Example usage of the YouTube transcript extractor as a module.
"""

from youtube_transcript_extractor import get_youtube_transcript, extract_video_id


def example_usage():
    """
    Example of how to use the transcript extractor functions.
    """
    # Example YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Extract video ID
    video_id = extract_video_id(youtube_url)
    print(f"Video ID: {video_id}")
    
    # Get transcript
    transcript = get_youtube_transcript(youtube_url)
    
    if transcript:
        print(f"Transcript preview (first 200 chars): {transcript[:200]}...")
        print(f"Full transcript length: {len(transcript)} characters")
        
        # You can now process the transcript as needed
        # For example, split into sentences, analyze sentiment, etc.
        
    else:
        print("Could not retrieve transcript")


if __name__ == "__main__":
    example_usage()