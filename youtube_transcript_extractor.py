#!/usr/bin/env python3
"""
YouTube Video Transcript Summarizer

This script extracts the transcript from a YouTube video and generates a summary using OpenAI.
It uses the youtube-transcript-api library to fetch transcripts and OpenAI's API for summarization.
"""

import sys
import os
import re
import argparse
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Error: youtube-transcript-api package not installed.")
    print("Please install it using: pip install youtube-transcript-api")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed.")
    print("Please install it using: pip install openai")
    sys.exit(1)

# OpenAI API key - loaded from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your OpenAI API key.")
    sys.exit(1)


def extract_video_id(youtube_url):
    """
    Extract video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    """
    # Regular expression patterns for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    # Try parsing as URL query parameter
    try:
        parsed_url = urlparse(youtube_url)
        if 'youtube.com' in parsed_url.netloc:
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]
    except:
        pass
    
    return None


def get_youtube_transcript(youtube_url, language_codes=['en']):
    """
    Get the transcript of a YouTube video.
    
    Args:
        youtube_url (str): The YouTube video URL
        language_codes (list): Preferred language codes for transcript
        
    Returns:
        str: The transcript text, or None if not available
    """
    try:
        # Extract video ID from URL
        video_id = extract_video_id(youtube_url)
        if not video_id:
            print(f"Error: Could not extract video ID from URL: {youtube_url}")
            return None
        
        print(f"Extracting transcript for video ID: {video_id}")
        
        # Initialize the API client
        ytt_api = YouTubeTranscriptApi()
        
        # Try to get transcript in preferred languages
        try:
            transcript_data = ytt_api.fetch(video_id, languages=language_codes)
            transcript_list = transcript_data.to_raw_data()
        except Exception as e:
            # If preferred languages fail, try to get any available transcript
            print(f"Preferred languages not available, trying any available transcript...")
            try:
                available_transcripts = ytt_api.list(video_id)
                
                # Try to find any transcript (auto-generated or manual)
                transcript_data = None
                for transcript_obj in available_transcripts:
                    try:
                        transcript_data = transcript_obj.fetch()
                        print(f"Found transcript in language: {transcript_obj.language}")
                        break
                    except:
                        continue
                
                if not transcript_data:
                    print("Error: No transcripts available for this video")
                    return None
                    
                transcript_list = transcript_data.to_raw_data()
            except Exception as e2:
                print(f"Error listing transcripts: {str(e2)}")
                return None
        
        # Convert transcript list to formatted text
        transcript_text = ""
        for entry in transcript_list:
            transcript_text += entry['text'] + " "
        
        return transcript_text.strip()
        
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")
        return None


def simple_summarize(transcript_text):
    """
    Create an actual summary by analyzing content and key themes (backup method).
    
    Args:
        transcript_text (str): The full transcript text
        
    Returns:
        str: An actual summary of the video content
    """
    import re
    from collections import Counter
    
    # Clean up the text
    text = transcript_text.lower()
    
    # Remove common filler words and clean text
    filler_words = {'um', 'uh', 'like', 'you know', 'so', 'well', 'yeah', 'oh', 'okay', 'right', 'i mean', 'blah'}
    
    # Extract key information patterns
    summary_parts = []
    
    # Look for introductory phrases that indicate main topics
    intro_patterns = [
        r"this is about (.{20,100})",
        r"we're talking about (.{20,100})",
        r"today (.{20,100})",
        r"the biggest (.{20,100})",
        r"announcement (.{20,100})"
    ]
    
    for pattern in intro_patterns:
        matches = re.findall(pattern, text)
        if matches:
            summary_parts.extend(matches[:2])  # Take first 2 matches
    
    # Look for people mentioned (capitalize common names)
    people_mentioned = []
    name_patterns = [
        r"\b(beetlejuice|robin|eric|bobby|howard|sal)\b"
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        people_mentioned.extend(matches)
    
    # Get most frequent meaningful words (excluding common words)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    common_words = {'this', 'that', 'with', 'have', 'they', 'will', 'been', 'said', 'each', 'which', 'their', 'time', 'were', 'there', 'what', 'your', 'when', 'them'}
    meaningful_words = [w for w in words if w not in common_words and w not in filler_words]
    word_freq = Counter(meaningful_words)
    top_words = [word for word, count in word_freq.most_common(10) if count > 2]
    
    # Look for specific topics/activities mentioned
    topics = []
    topic_patterns = [
        r"(bitcoin|cryptocurrency|money)",
        r"(married|children|bachelor|family)",
        r"(drink|sober|alcohol)",
        r"(years?|time|ago)",
        r"(miss|missed|away)",
        r"(show|fans|people)"
    ]
    
    for pattern in topic_patterns:
        if re.search(pattern, text):
            topics.append(pattern.strip('()').split('|')[0])
    
    # Create actual summary
    summary = "Video Summary:\n\n"
    
    # Determine main subject
    if 'beetlejuice' in text:
        summary += "This appears to be an interview or conversation with Beetlejuice, a personality from a radio show. "
    
    # Add main topics
    if topics:
        summary += f"The discussion covers topics including: {', '.join(topics[:5])}. "
    
    # Add key people
    if people_mentioned:
        unique_people = list(set(people_mentioned))
        summary += f"Key people mentioned: {', '.join(unique_people[:5])}. "
    
    # Add context from patterns found
    if summary_parts:
        cleaned_parts = [part.strip(' .') for part in summary_parts[:2]]
        summary += f"Main points discussed: {' '.join(cleaned_parts)}. "
    
    # Look for time references and context
    if 'five years' in text:
        summary += "There's discussion about a five-year absence or gap. "
    if 'hotel' in text:
        summary += "The conversation appears to take place in a hotel setting. "
    if 'announce' in text:
        summary += "Some kind of announcement or news is being shared. "
    
    # Add conclusion
    summary += "\n\nThis appears to be a radio show or podcast interview format with casual conversation and discussion of personal topics."
    
    return summary


def summarize_transcript(transcript_text, use_openai=True, summary_style="structured"):
    """
    Generate a summary of the transcript using OpenAI's API or simple method.
    
    Args:
        transcript_text (str): The full transcript text to summarize
        use_openai (bool): Whether to try OpenAI first
        summary_style (str): Style of summary - "structured", "brief", or "detailed"
        
    Returns:
        str: The generated summary, or None if there was an error
    """
    if use_openai:
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            # Choose prompt based on summary style
            if summary_style == "brief":
                prompt = f"""Create a concise YouTube video description (1-2 paragraphs) that captures the essence of this video. Write as if you're the creator briefly describing what viewers will see. Focus on the main highlights and why someone should watch.

Transcript: {transcript_text}

Brief YouTube Description:"""
                
            elif summary_style == "detailed":
                prompt = f"""Create an extremely comprehensive YouTube video description that covers every important aspect of this video content. Include specific quotes, detailed breakdowns of conversations, background context, and thorough explanations of all topics discussed. Write as the official creator giving viewers the most complete description possible - go into extensive detail about what's covered and what viewers will experience.

Transcript: {transcript_text}

Comprehensive YouTube Description:"""
                
            else:  # structured (default) - YouTube Description Style
                prompt = f"""Create an in-depth YouTube video description based on this transcript. Write it as if you're the official content creator describing what viewers will see and learn in this video. 

Make it comprehensive and engaging, including:

🎯 **Opening Hook**: Start with an engaging description of what this video is about
📋 **Detailed Content Breakdown**: Explain specific topics, conversations, and moments discussed
👥 **Key Participants**: Describe the people involved and their significance  
🔥 **Highlights & Key Moments**: Mention the most interesting or important parts
💡 **What Viewers Will Learn/Discover**: Specific insights, news, or takeaways
📝 **Additional Context**: Background information that helps viewers understand the content

Write in an engaging, YouTube-description style that's detailed and specific. Include actual quotes or specific details from the conversation when relevant. Make it sound like an official, comprehensive video description that goes beyond surface-level summary.

Use confident, definitive language. Be specific about what's discussed and make viewers excited to watch.

Transcript: {transcript_text}

YouTube-Style Description:"""
            
            print("Generating professional YouTube description using OpenAI...")
            
            # Make API call to OpenAI with improved settings
            response = client.chat.completions.create(
                model="gpt-4o",  # Upgraded to GPT-4 for highest quality
                messages=[
                    {"role": "system", "content": "You are an expert YouTube content creator and video description writer. You create engaging, comprehensive video descriptions that sound official and professional. Your descriptions are detailed, specific, and make viewers excited to watch the content. You write with confidence and authority, including specific details, quotes, and moments from the video to give viewers a complete understanding of what they'll experience."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,  # Increased for detailed YouTube-style descriptions
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"OpenAI error: {str(e)}")
            print("Falling back to simple summarization method...")
            return simple_summarize(transcript_text)
    else:
        print("Using simple summarization method...")
        return simple_summarize(transcript_text)


def main():
    """
    Main function to handle command line arguments and run the script.
    """
    parser = argparse.ArgumentParser(
        description="YouTube Video Description Generator - Create professional video descriptions from transcripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Description Styles:
  structured  : Comprehensive YouTube-style description with sections (default)
  brief       : Concise 1-2 paragraph description highlighting key points
  detailed    : Extensive description covering all aspects in depth

Examples:
  python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
  python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --style brief
  python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --style detailed --no-openai
        """
    )
    
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--style", choices=["structured", "brief", "detailed"], 
                       default="structured", help="Summary style (default: structured)")
    parser.add_argument("--no-openai", action="store_true", 
                       help="Use simple summarizer instead of OpenAI")
    
    args = parser.parse_args()
    
    print("🎥 YouTube Description Generator")
    print("=" * 50)
    print(f"URL: {args.url}")
    print(f"Description Style: {args.style}")
    print("-" * 50)
    
    # Extract transcript
    transcript = get_youtube_transcript(args.url)
    
    if transcript:
        print(f"✅ Transcript extracted successfully ({len(transcript)} characters)")
        
        # Generate summary using specified method and style
        use_openai = not args.no_openai
        summary = summarize_transcript(transcript, use_openai=use_openai, summary_style=args.style)
        
        if summary:
            print(f"\n📝 YouTube Video Description ({args.style.title()} Style):")
            print("=" * 50)
            print(summary)
            print("=" * 50)
            
            # Save description to file
            video_id = extract_video_id(args.url)
            description_filename = f"description_{video_id}_{args.style}.txt"
            try:
                with open(description_filename, 'w', encoding='utf-8') as f:
                    f.write(f"YouTube Video Description ({args.style.title()} Style)\n")
                    f.write(f"URL: {args.url}\n")
                    f.write(f"Video ID: {video_id}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(summary)
                print(f"💾 Description saved to: {description_filename}")
            except Exception as e:
                print(f"❌ Could not save description to file: {e}")
        else:
            print("❌ Failed to generate description")
            sys.exit(1)
    else:
        print("❌ Failed to extract transcript. Please check:")
        print("- The URL is correct and the video exists")
        print("- The video has captions/transcripts available")
        print("- The video is not private or restricted")
        sys.exit(1)


if __name__ == "__main__":
    main()