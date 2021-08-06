# Using a Neural Network to select memes for my girlfriend

Well, my GF's tastes in memes are simple: she loves wholesome memes and, most importantly, **she loves animals**.

That's why I created a fun little project that:
1. Surfs [r/wholesomemes](https://www.reddit.com/r/wholesomememes/)
2. Downloads a few of the hottest memes in the contents folder
3. Initializes a ResNet50 model that recognizes the ones containing any animal
4. Sends them via mail to my GF (greeted by plenty of positive feedbacks)

### Final email (3 memes by default)
![finalmail](https://github.com/mutt0-ds/memes-selector/blob/main/media/result.png)


### Reddit

I'm using the praw library for downloading memes, it requires a Reddit Bot enabled.
Use [this guide](https://yojji.io/blog/how-to-make-a-reddit-bot) for creating one, it's a quick process.

### ResNet50

ResNet50 ([more info here](https://keras.io/api/applications/resnet/)) is an Image Recognition model that outputs a probability score (which I'm ignoring at the moment) and one of the 1000 labels available. The labels are mapped in the imagenet_class_index, and the first 397 are about animals (mostly cats and dogs). 
So, if the model's predicted label is in that sublist, we can classify the meme as "containing animals".

![example](https://github.com/mutt0-ds/memes-selector/blob/main/media/example.png)

### Email

I'm using smtplib for sending the email, so it just requires the email and password of the sender and the email of the receiver.

### Use

Be free to have fun with the memes selector, it can be tweaked to select only a certain type of memes, change subreddit, etc...
I would love to send the message via Whatsapp but the only alternative (by Twilio) is not simple to adapt.
