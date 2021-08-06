# -*- coding: utf-8 -*-
import os
import logging
from src.resnet import select_animal_memes
from src.reddit import download_from_reddit
from src.mail import EmailSender

logging.basicConfig(filename='logging.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def main():
    #init  variables
    SUBREDDIT = os.environ.get("SUBREDDIT")
    PATH = os.environ.get("PATH")
    os.chdir(PATH)

    path_json = PATH + "/imagenet_class_index.json"
    memes_folder = PATH+'/contents/'

    #downloads all the memes from reddit, default 50 img
    download_from_reddit(memes_folder,SUBREDDIT, limit = 50)

    #using ResNet50, it finds the memes containing animals
    selected_memes = select_animal_memes(memes_folder,path_json)

    #sending the mail
    email_sender = EmailSender(path=memes_folder,num_memes=os.environ.get["NUM_MEMES"])
    msg =email_sender.prepare_MIME_text(selected_memes)
    email_sender.send_email(msg) 

    #cleaning up the whole folder (remove if you want to store everything)
    for f in os.listdir(memes_folder):
        os.remove(memes_folder+f)

    os._exit(00)

if __name__=="__main__":
    main()