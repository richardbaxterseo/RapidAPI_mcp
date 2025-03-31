from fastmcp import FastMCP
from twitter_crawler import TwitterCrawler

twitter_crawler = TwitterCrawler()
mcp = FastMCP("RapidAPI")


@mcp.tool()
def get_user_recent_tweets(username: str) -> list:
    data = twitter_crawler.get_timeline(username)
    new_tweets = twitter_crawler.clean_tweet_data(
        data['timeline'],
        data.get('prev_cursor'),
        data.get('next_cursor')
    )
    return new_tweets
