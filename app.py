#!/usr/bin/env python3
"""
YouTube Video Summarizer Web Application

A Flask web app that allows users to input YouTube URLs and get AI-generated summaries.
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import re
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# In production, environment variables are set directly by the platform
load_dotenv()  # Only loads if .env file exists, won't override production env vars

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

# Initialize Flask app
app = Flask(__name__)

# OpenAI API key - loaded from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your OpenAI API key.")
    sys.exit(1)


def extract_video_id(youtube_url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
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
    """Get the transcript of a YouTube video."""
    try:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return None, "Could not extract video ID from URL"
        
        ytt_api = YouTubeTranscriptApi()
        
        try:
            transcript_data = ytt_api.fetch(video_id, languages=language_codes)
            transcript_list = transcript_data.to_raw_data()
        except Exception as e:
            try:
                available_transcripts = ytt_api.list(video_id)
                transcript_data = None
                for transcript_obj in available_transcripts:
                    try:
                        transcript_data = transcript_obj.fetch()
                        break
                    except:
                        continue
                
                if not transcript_data:
                    return None, "No transcripts available for this video"
                    
                transcript_list = transcript_data.to_raw_data()
            except Exception as e2:
                return None, f"Error listing transcripts: {str(e2)}"
        
        # Convert transcript list to formatted text
        transcript_text = ""
        for entry in transcript_list:
            transcript_text += entry['text'] + " "
        
        return transcript_text.strip(), None
        
    except Exception as e:
        return None, f"Error fetching transcript: {str(e)}"


def summarize_transcript(transcript_text, summary_style="structured"):
    """Generate a summary using OpenAI."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        if summary_style == "brief":
            prompt = f"""Create a concise summary (1-2 paragraphs) of what happens in this video. Focus on the main content, who is involved, and what topics are discussed. Write in a straightforward, informative style.

Transcript: {transcript_text}

Brief Summary:"""
            
        elif summary_style == "detailed":
            prompt = f"""Create a comprehensive summary that covers all important aspects of this video's content. Include specific details about conversations, topics discussed, people involved, and key information shared. Be thorough but factual - focus on what actually happens and what is said rather than promotional language.

Transcript: {transcript_text}

Detailed Summary:"""
            
        else:  # structured (default)
            prompt = f"""Create a well-structured summary of this video's content. Organize the information clearly and focus on what actually happens in the video.

Structure your summary with these sections:

**Content Overview**: What type of video this is and who is involved
**Main Topics Discussed**: The key subjects and conversations that take place
**Key People**: Who appears in the video and their relevance
**Important Information**: Specific details, announcements, or notable moments
**Key Points**: The main takeaways from the content

Write in a clear, factual tone. Focus on summarizing the actual content rather than using promotional language. Be specific about what is discussed and what information is shared.

Transcript: {transcript_text}

Content Summary:"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert content analyst who creates clear, factual summaries of video content. Your summaries are informative, well-organized, and focus on what actually happens in the video. You write in a straightforward, professional tone that clearly explains the content without promotional language."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip(), None
        
    except Exception as e:
        return None, f"Error generating summary: {str(e)}"


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    """Handle summarization requests."""
    try:
        data = request.get_json()
        youtube_url = data.get('url', '').strip()
        summary_style = data.get('style', 'structured')
        
        if not youtube_url:
            return jsonify({'error': 'Please provide a YouTube URL'})
        
        # Extract transcript
        transcript, error = get_youtube_transcript(youtube_url)
        if error:
            return jsonify({'error': f'Failed to get transcript: {error}'})
        
        if not transcript:
            return jsonify({'error': 'No transcript found for this video'})
        
        # Generate summary
        summary, error = summarize_transcript(transcript, summary_style)
        if error:
            return jsonify({'error': f'Failed to generate summary: {error}'})
        
        if not summary:
            return jsonify({'error': 'Failed to generate summary'})
        
        video_id = extract_video_id(youtube_url)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'video_id': video_id,
            'transcript_length': len(transcript),
            'style': summary_style
        })
        
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'})


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)