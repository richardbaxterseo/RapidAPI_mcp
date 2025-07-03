import os
import re
import requests
from typing import Dict, Optional, List
import logging

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
    
    def get_transcript(self, video_id: str, lang: str = 'en') -> Dict:
        """
        Fetch transcript for a YouTube video
        
        Args:
            video_id: The YouTube video ID
            lang: Language code for the transcript (default: 'en')
        
        Returns:
            Dict containing transcript data or error information
        """
        try:
            # Ensure we have a valid video ID
            clean_video_id = self.extract_video_id(video_id)
            if not clean_video_id:
                return {
                    "error": "Invalid YouTube video ID or URL",
                    "provided_input": video_id
                }
            
            logging.info(f"Fetching transcript for video ID: {clean_video_id}")
            
            response = requests.get(
                f'https://{self.api_host}/api/transcript',
                headers=self.headers,
                params={
                    'videoId': clean_video_id,
                    'lang': lang
                },
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Add metadata
            if isinstance(data, list) and data:
                return {
                    "video_id": clean_video_id,
                    "language": lang,
                    "transcript": data,
                    "status": "success"
                }
            else:
                return data
                
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            return {
                "error": f"API request failed: {str(e)}",
                "video_id": video_id,
                "status": "error"
            }
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "video_id": video_id,
                "status": "error"
            }
    
    def get_formatted_transcript(self, video_id: str, lang: str = 'en') -> str:
        """
        Get transcript as formatted text
        
        Args:
            video_id: The YouTube video ID or URL
            lang: Language code for the transcript
        
        Returns:
            Formatted transcript text or error message
        """
        result = self.get_transcript(video_id, lang)
        
        if result.get('status') == 'error':
            return f"Error: {result.get('error', 'Unknown error')}"
        
        if 'transcript' in result and isinstance(result['transcript'], list):
            # Format transcript segments into readable text
            formatted_lines = []
            for segment in result['transcript']:
                if isinstance(segment, dict) and 'text' in segment:
                    formatted_lines.append(segment['text'])
            
            return '\n'.join(formatted_lines)
        
        return "No transcript available"
    
    def get_transcript_with_timestamps(self, video_id: str, lang: str = 'en') -> List[Dict]:
        """
        Get transcript with timestamps
        
        Args:
            video_id: The YouTube video ID or URL
            lang: Language code for the transcript
        
        Returns:
            List of transcript segments with timestamps
        """
        result = self.get_transcript(video_id, lang)
        
        if result.get('status') == 'error':
            return [{"error": result.get('error', 'Unknown error')}]
        
        if 'transcript' in result and isinstance(result['transcript'], list):
            return result['transcript']
        
        return []
