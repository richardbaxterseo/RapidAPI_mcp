import csv
import json
import os
import time
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime

# # 配置日志
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('twitter_crawler.log'),
#         logging.StreamHandler()
#     ]
# )


class TwitterCrawler:
    def __init__(self):
        self.api_host = 'twitter-api45.p.rapidapi.com'
        self.api_key = '66dc774248msh5470cb9692d299cp1ac178jsn3f1836abf93f'
        self.headers = {
            'x-rapidapi-host': self.api_host,
            'x-rapidapi-key': self.api_key
        }
        # self.data_dir = 'data'
        # if not os.path.exists(self.data_dir):
        #     os.makedirs(self.data_dir)

    def read_kols(self, limit: int = 3) -> List[Dict]:
        """读取KOL信息"""
        kols = []
        try:
            with open('kols.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= limit:
                        break
                    kols.append({
                        'Username': row['Username'],
                        'TwitterUserURL': row['TwitterUserURL']
                    })
            # logging.info(f'成功读取{len(kols)}条KOL信息')
            return kols
        except Exception as e:
            # logging.error(f'读取KOL信息失败: {str(e)}')
            return []

    def get_timeline(self, username: str, cursor: Optional[str] = None) -> Dict:
        """获取用户时间线数据"""
        # logging.info(f'getTimeline params: {username} {cursor}')

        try:
            params = {'screenname': username}
            if cursor:
                params['cursor'] = cursor

            response = requests.get(
                'https://twitter-api45.p.rapidapi.com/timeline.php',
                headers=self.headers,
                params=params
            )
            data = response.json()

            if data.get('timeline'):
                timeline_info = 'empty array' if not data['timeline'] else \
                    [tweet.get('tweet_id') for tweet in data['timeline']]
                # logging.info(f'接口返回结果: {timeline_info}')

            return data
        except Exception as e:
            logging.error(f'获取{username}时间线数据失败: {str(e)}')
            return {}

    def clean_tweet_data(self, timeline_data: List[Dict], prev_cursor: str, next_cursor: str) -> List[Dict]:
        """清理推文数据，提取所需字段"""
        return [{
            'tweet_id': tweet.get('tweet_id', ''),
            'created_at': tweet.get('created_at', ''),
            'favorites': tweet.get('favorites', 0),
            'bookmarks': tweet.get('bookmarks', 0),
            'text': tweet.get('text', ''),
            'views': tweet.get('views', '0'),
            'quotes': tweet.get('quotes', 0),
            'prev_cursor': prev_cursor,
            'next_cursor': next_cursor
        } for tweet in timeline_data]

    def save_to_csv(self, username: str, data: List[Dict], mode: str = 'w') -> None:
        """保存数据到CSV文件"""
        file_path = os.path.join(self.data_dir, f'{username}.csv')
        try:
            if not data:
                return

            write_header = mode == 'w' or not os.path.exists(file_path)
            with open(file_path, mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
                if write_header:
                    writer.writeheader()
                writer.writerows(data)

            logging.info(f'成功保存{len(data)}条数据到{file_path}')
        except Exception as e:
            logging.error(f'保存数据到CSV失败: {str(e)}')

    def get_base_tweet(self, username: str) -> Optional[Dict]:
        """获取基准推文数据"""
        file_path = os.path.join(self.data_dir, f'{username}.csv')
        try:
            if not os.path.exists(file_path):
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return next(reader, None)
        except Exception as e:
            logging.error(f'读取基准推文数据失败: {str(e)}')
            return None

    def filter_duplicate_data(self, existing_data: List[Dict], new_data: List[Dict]) -> List[Dict]:
        """过滤重复的推文数据"""
        existing_ids = set(tweet['tweet_id'] for tweet in existing_data)
        return [tweet for tweet in new_data if tweet['tweet_id'] not in existing_ids]

    def crawl_user_timeline(self, username: str, mode: str = 'init') -> None:
        """抓取用户时间线数据"""
        all_tweets = []
        base_tweet = None
        next_cursor = None

        # 如果是更新模式，获取基准推文
        if mode == 'update':
            base_tweet = self.get_base_tweet(username)
            if not base_tweet:
                logging.error(f'无法获取{username}的基准推文数据')
                return

        while True:
            data = None
            new_tweets = []

            if mode == 'init':
                data = self.get_timeline(username, next_cursor)

                if not data or not data.get('timeline'):
                    logging.info(f'没有更多数据可获取，停止抓取{username}的时间线数据')
                    break

                # 清理推文数据
                new_tweets = self.clean_tweet_data(
                    data['timeline'],
                    data.get('prev_cursor'),
                    data.get('next_cursor')
                )

                all_tweets.extend(new_tweets)

                # 保存数据
                self.save_to_csv(
                    username,
                    new_tweets,
                    'w' if len(all_tweets) == len(new_tweets) else 'a'
                )

                if len(all_tweets) >= 100:
                    break

            if mode == 'update':
                data = self.get_timeline(username, base_tweet['prev_cursor'])

                if not data or not data.get('timeline'):
                    logging.info(f'没有更多数据可获取，停止抓取{username}的时间线数据')
                    break

                # 清理推文数据
                new_tweets = self.clean_tweet_data(
                    data['timeline'],
                    data.get('prev_cursor'),
                    data.get('next_cursor')
                )

                # 过滤重复数据
                existing_data = [self.get_base_tweet(
                    username)] if self.get_base_tweet(username) else []
                unique_tweets = self.filter_duplicate_data(
                    existing_data, new_tweets)
                if unique_tweets:
                    self.save_to_csv(username, unique_tweets, 'a')

            # 更新游标
            next_cursor = data.get('next_cursor')

            # 添加延迟避免频繁请求
            time.sleep(1)

        logging.info(f'完成{username}的时间线数据处理')

    def run(self) -> None:
        """运行爬虫"""
        # 获取kol信息
        kols = self.read_kols(1)
        if not kols:
            logging.error('没有找到KOL信息')
            return

        for kol in kols:
            username = kol['Username']
            logging.info(f'******处理kol {username} 信息******')

            # 判断模式
            mode = 'update' if self.get_base_tweet(username) else 'init'
            logging.info(f'采用{mode}模式')

            # 开始爬取
            self.crawl_user_timeline(username, mode)
            time.sleep(2)  # 处理下一个KOL前暂停
