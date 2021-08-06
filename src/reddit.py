import praw
import logging
from urllib.request import urlretrieve
import os

def url_retriever_from_reddit(subname= "wholesomememes", limit=50):
   
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_SCRIPT"),
        client_secret=os.environ.get("REDDIT_SECRET"),
        user_agent=os.environ.get("REDDIT_USERAGENT"),
        username=os.environ.get("REDDIT_USERNAME"),  # your username
        password=os.environ.get("REDDIT_PSW"),  # your username
    )
    
    subreddit = reddit.subreddit(subname)
    
    images_url = []
    for submission in subreddit.top(limit=limit):
        if submission.url.endswith(".jpg") or submission.url.endswith(".png"):
            images_url.append(submission.url)

    return images_url

def download_from_reddit(download_folder, subreddit, limit = 50):
    images_url = url_retriever_from_reddit(subreddit,limit)
    cont = 0
    
    for i in images_url:
        urlretrieve(i,download_folder+f"/{cont}.jpg")
        cont+=1

    logging.info(f"Downloaded {cont} images from {subreddit}")