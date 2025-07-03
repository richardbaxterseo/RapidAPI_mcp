import os
import re
import requests
from typing import Dict, Optional, List, Union
import logging
from urllib.parse import quote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class YouTubeTranscriptAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize YouTube Transcript API client"""
        self.api_host = 'youtube-transcript3.p.rapidapi.com'
        self.api_key = api_key or os.getenv('RAPIDAPI_KEY', '')
        
        if not self.api_key:
            raise ValueError("RapidAPI key is required. Set RAPIDAPI_KEY environment variable or pass it to constructor.")
        
        self.headers = {
            'x-rapidapi-host': self.api_host,
            'x-rapidapi-key': self.api_key
        }
    
    def extract_video_id(self, url_or_id: str) -> Optional[str]:
        """Extract YouTube video ID from URL or return the ID if already provided"""
        # If it's already a video ID (11 characters)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
            return url_or_id
        
        # Try to extract from various YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*&v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)
        
        return None
    
    def build_youtube_url(self, video_id_or_url: str) -> str:
        """Convert video ID to full YouTube URL or return URL if already provided"""
        # If it's already a URL, return it
        if video_id_or_url.startswith(('http://', 'https://')):
            return video_id_or_url
        
        # If it's a video ID, build the URL
        video_id = self.extract_video_id(video_id_or_url)
        if video_id:
            return f'https://www.youtube.com/watch?v={video_id}'
        
        # If we can't identify it, assume it's a video ID
        return f'https://www.youtube.com/watch?v={video_id_or_url}'
    
    def get_transcript(self, video_id_or_url: str, lang: str = 'en', flat_text: bool = False) -> Dict:
        """
        Fetch transcript for a YouTube video
        
        Args:
            video_id_or_url: YouTube video ID or URL
            lang: Language code for the transcript (default: 'en')
            flat_text: If True, returns plain text. If False, returns structured data
        
        Returns:
            Dict containing transcript data or error information
        """
        try:
            # Build the full YouTube URL
            youtube_url = self.build_youtube_url(video_id_or_url)
            
            # Extract video ID for logging
            video_id = self.extract_video_id(video_id_or_url)
            
            logging.info(f"Fetching transcript for URL: {youtube_url}")
            
            # URL encode the YouTube URL
            encoded_url = quote(youtube_url, safe='')
            
            # Build API URL with parameters
            api_url = f'https://{self.api_host}/api/transcript-with-url'
            params = {
                'url': youtube_url,  # The API handles encoding internally
                'lang': lang,
                'flat_text': str(flat_text).lower()
            }
            
            response = requests.get(
                api_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Add metadata to response
            return {
                "video_id": video_id,
                "video_url": youtube_url,
                "language": lang,
                "flat_text": flat_text,
                "transcript": data,
                "status": "success"
            }
                
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('message', str(e))
                except:
                    error_msg = e.response.text or str(e)
            
            return {
                "error": f"API request failed: {error_msg}",
                "video_id": video_id if 'video_id' in locals() else video_id_or_url,
                "status": "error"
            }
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "video_id": video_id if 'video_id' in locals() else video_id_or_url,
                "status": "error"
            }
    
    def get_formatted_transcript(self, video_id_or_url: str, lang: str = 'en') -> str:
        """
        Get transcript as formatted text
        
        Args:
            video_id_or_url: The YouTube video ID or URL
            lang: Language code for the transcript
        
        Returns:
            Formatted transcript text or error message
        """
        # Use flat_text=True to get plain text directly
        result = self.get_transcript(video_id_or_url, lang, flat_text=True)
        
        if result.get('status') == 'error':
            return f"Error: {result.get('error', 'Unknown error')}"
        
        # When flat_text=True, the API returns plain text directly
        transcript = result.get('transcript', '')
        if isinstance(transcript, str):
            return transcript
        elif isinstance(transcript, list):
            # If it's still a list (flat_text=False), format it
            formatted_lines = []
            for segment in transcript:
                if isinstance(segment, dict) and 'text' in segment:
                    formatted_lines.append(segment['text'])
                elif isinstance(segment, str):
                    formatted_lines.append(segment)
            return '\n'.join(formatted_lines)
        
        return "No transcript available"
    
    def get_transcript_with_timestamps(self, video_id_or_url: str, lang: str = 'en') -> Union[List[Dict], Dict]:
        """
        Get transcript with timestamps
        
        Args:
            video_id_or_url: The YouTube video ID or URL
            lang: Language code for the transcript
        
        Returns:
            List of transcript segments with timestamps or error dict
        """
        # Use flat_text=False to get structured data with timestamps
        result = self.get_transcript(video_id_or_url, lang, flat_text=False)
        
        if result.get('status') == 'error':
            return result
        
        transcript = result.get('transcript', [])
        if isinstance(transcript, list):
            return transcript
        
        # If we got a string (shouldn't happen with flat_text=False), return as is
        return {"transcript": transcript, "note": "Timestamps not available in this format"}
