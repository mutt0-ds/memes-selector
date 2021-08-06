import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import date
import os
import logging

############INIT VARIABLES#############
class EmailSender:
    """
    class for sending the mail, default num of img attached: 3
    """
    def __init__(self, path, num_memes = 3):
        self.PATH = path

        self.NUM_MEMES = num_memes

        self.gmail_user = os.environ["MAIL_SENDER"]
        self.gmail_password = os.environ["PSW_SENDER"]

        self.strFrom = self.gmail_user 
        self.strTo = os.environ["MAIL_RECEIVER"]

        self.subject = f'😎 Memes Ready - {date.today()} 😎'

        #it picks a random choice in the list for the mail's body, avoiding being monotone
        self.saluti = ["Hello","Good morning","Here we go"]

    def prepare_MIME_text(self, selected_memes : tuple):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject

        msgRoot['From'] = self.strFrom
        msgRoot['To'] = self.strTo

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgAlternative.attach(MIMEText('Errore'))

        #adding image and confidence score
        loop_for_adding_names=" ".join(["<br><br>Probability for "
                            +selected_memes[i][2].replace("_"," ").capitalize()
                            +": "
                            +selected_memes[i][3]
                            +f'<br><img src="cid:image{i+1}"style="max-height: 500px; max-width: 500px;">'
                            for i in range(self.NUM_MEMES)])

        msgText = MIMEText(f"""
                        <h2>Bzzt Bzzt!\n</h2>
                        <h3>{random.choice(self.saluti)}\n</h3>
                        {loop_for_adding_names}
                        \n\n\nI hope you liked them!
                        """, 'html')

        msgAlternative.attach(msgText)

        #attaching images
        os.chdir(self.PATH)
        for i in range(self.NUM_MEMES):
            image = selected_memes[i][1]
            
            # This example assumes the image is in the current directory
            try:
                img_data = open(image, 'rb')

                msgImage = MIMEImage(img_data.read())
                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', f'<image{i+1}>')
                msgRoot.attach(msgImage)
                
                img_data.close()

            except Exception as e:
                logging.warning("Attachment error",str(e))

        return msgRoot

    def send_email(self, msgRoot):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.strFrom, self.strTo, msgRoot.as_string())
            server.close()

            logging.info('Email sent!')    

        except:
            logging.critical('Something went wrong with the email!')
