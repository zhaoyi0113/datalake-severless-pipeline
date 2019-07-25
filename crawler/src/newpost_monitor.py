import praw
import numpy as np
import pandas as pd
from utils import createReddit, createDataframeFromSub, upload_subs_to_s3, query_submission_id
import time

LIMIT = 1000

def handler(event, context):
    reddit = createReddit()
    topic = 'movies'
    if 'topic' in event:
        topic = event['topic']
    check_new_posts(reddit, topic)

def check_new_posts(reddit, topic):
    new_posts = []
    for post in reddit.subreddit(topic).new(limit=LIMIT):
        if post.name not in seen_posts:
            seen_posts.append(post.name)
            new_posts.append(post)
    print('saved seen posts id:', seen_posts)
    print('check new posts:', len(new_posts))
    if len(new_posts) > 0:
        notify(new_posts, topic)

def notify(subs, topic):
    filtered = [x for x in subs if query_submission_id(x.name) == 0]
    print('filtered:', filtered)
    print('send notify for ', len(subs), ' submissions')
    upload_subs_to_s3(subs, topic)

seen_posts = []

if __name__ == '__main__':
    while True:
        handler({'topic': 'news'}, None)
        time.sleep(5)
