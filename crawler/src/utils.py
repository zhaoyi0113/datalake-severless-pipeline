import praw
import numpy as np
import pandas as pd
import os
from io import StringIO
import boto3
from datetime import datetime

def createReddit():
    reddit = praw.Reddit(client_id=os.environ['praw_client_id'],
                         client_secret=os.environ['praw_client_secret'],
                         user_agent='lambda')
    return reddit

def createDataframeFromSub(subs):
    topics = []
    for submission in subs:
        row = np.array([submission.id, submission.name, submission.num_comments,
                        submission.score, submission.title, submission.url])
        topics.append(row)
    np_info = np.array(topics)
    columns = ['id', 'name', 'num_comments', 'vote', 'title', 'url']
    df = pd.DataFrame(np_info, columns=columns)
    return df

def upload_to_s3(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    file_name = 'bestof-' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.csv'
    s3_resource.Object('jzhao-datalake-test', 'netflix/' +
                       file_name).put(Body=csv_buffer.getvalue())
    print('upload file ' + file_name + ' to s3')