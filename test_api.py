#!/usr/bin/env python3
"""
Test script for YouTube Transcript API
"""

import os
import sys
from youtube_transcript import YouTubeTranscriptAPI

def test_youtube_transcript():
    """Test the YouTube Transcript API with various inputs"""
    
    # Test video URL
    test_url = "https://www.youtube.com/watch?v=3mAeVIA94n0"
    
    # Check if API key is set
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("❌ Error: RAPIDAPI_KEY environment variable not set")
        print("Please set it with: export RAPIDAPI_KEY='your-key-here'")
        return
    
    print(f"✅ API Key found (length: {len(api_key)})")
    
    try:
        # Initialize API client
        api = YouTubeTranscriptAPI(api_key)
        print("✅ API client initialized")
        
        # Test 1: Get structured transcript
        print(f"\n📝 Test 1: Getting structured transcript for {test_url}")
        result = api.get_transcript(test_url, lang='en', flat_text=False)
        
        if result.get('status') == 'success':
            print("✅ Successfully fetched structured transcript")
            print(f"   Video ID: {result.get('video_id')}")
            print(f"   Language: {result.get('language')}")
            transcript = result.get('transcript', [])
            if isinstance(transcript, list) and transcript:
                print(f"   Segments: {len(transcript)}")
                print(f"   First segment: {transcript[0] if transcript else 'N/A'}")
        else:
            print(f"❌ Error: {result.get('error')}")
        
        # Test 2: Get flat text transcript
        print(f"\n📝 Test 2: Getting flat text transcript")
        text_result = api.get_formatted_transcript(test_url, lang='en')
        
        if isinstance(text_result, str) and not text_result.startswith("Error:"):
            print("✅ Successfully fetched flat text transcript")
            print(f"   Text length: {len(text_result)} characters")
            print(f"   Preview: {text_result[:200]}...")
        else:
            print(f"❌ Error: {text_result}")
        
        # Test 3: Test with video ID only
        video_id = "3mAeVIA94n0"
        print(f"\n📝 Test 3: Testing with video ID only: {video_id}")
        id_result = api.get_transcript(video_id, lang='en', flat_text=True)
        
        if id_result.get('status') == 'success':
            print("✅ Successfully fetched transcript using video ID")
        else:
            print(f"❌ Error: {id_result.get('error')}")
        
        # Test 4: Test video ID extraction
        print("\n📝 Test 4: Testing video ID extraction")
        test_urls = [
            "https://www.youtube.com/watch?v=3mAeVIA94n0",
            "https://youtu.be/3mAeVIA94n0",
            "https://youtube.com/embed/3mAeVIA94n0",
            "3mAeVIA94n0"
        ]
        
        for url in test_urls:
            extracted_id = api.extract_video_id(url)
            print(f"   {url} → {extracted_id} {'✅' if extracted_id == '3mAeVIA94n0' else '❌'}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎬 YouTube Transcript API Test Suite")
    print("=" * 50)
    test_youtube_transcript()
    print("\n✨ Test complete!")
