from fastmcp import FastMCP
from youtube_transcript import YouTubeTranscriptAPI

# Initialize the YouTube transcript API
youtube_api = YouTubeTranscriptAPI()

# Create MCP server
mcp = FastMCP("YouTube-Transcript")


@mcp.tool()
def get_youtube_transcript(video_id_or_url: str, language: str = "en") -> dict:
    """
    Get the transcript of a YouTube video
    
    Args:
        video_id_or_url: YouTube video ID or URL (e.g., 'dQw4w9WgXcQ' or 'https://youtube.com/watch?v=dQw4w9WgXcQ')
        language: Language code for the transcript (default: 'en' for English)
    
    Returns:
        Dict containing transcript data with video_id, language, transcript segments, and status
    """
    return youtube_api.get_transcript(video_id_or_url, language)


@mcp.tool()
def get_youtube_transcript_text(video_id_or_url: str, language: str = "en") -> str:
    """
    Get the transcript of a YouTube video as plain text
    
    Args:
        video_id_or_url: YouTube video ID or URL
        language: Language code for the transcript (default: 'en')
    
    Returns:
        Formatted transcript text without timestamps
    """
    return youtube_api.get_formatted_transcript(video_id_or_url, language)


@mcp.tool()
def get_youtube_transcript_with_timestamps(video_id_or_url: str, language: str = "en") -> list:
    """
    Get the transcript of a YouTube video with timestamps
    
    Args:
        video_id_or_url: YouTube video ID or URL
        language: Language code for the transcript (default: 'en')
    
    Returns:
        List of transcript segments, each containing text, start time, and duration
    """
    return youtube_api.get_transcript_with_timestamps(video_id_or_url, language)


# Keep the original Twitter function if needed, or comment it out
# from twitter_crawler import TwitterCrawler
# twitter_crawler = TwitterCrawler()

# @mcp.tool()
# def get_user_recent_tweets(username: str) -> list:
#     data = twitter_crawler.get_timeline(username)
#     new_tweets = twitter_crawler.clean_tweet_data(
#         data['timeline'],
#         data.get('prev_cursor'),
#         data.get('next_cursor')
#     )
#     return new_tweets


if __name__ == "__main__":
    # Run the server
    mcp.run()
