#! /usr/bin/env python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

from boto3 import Session


class Emailer:
    def __init__(self, sender: str, recipients: list, title: str, text: str):
        boto3_ses_client = Session(
            aws_access_key_id=environ.get('ACCESS_KEY'),
            aws_secret_access_key=environ.get('SECRET_KEY'),
        ).client('ses', region_name=environ.get('REGION'))

        response_ = self.send_mail(boto3_ses_client, sender, recipients, title, text)
        print(response_)

    @staticmethod
    def create_multipart_message(sender: str, recipients: list, title: str, text: str) -> MIMEMultipart:
        multipart_content_subtype = 'alternative' if text else 'mixed'
        msg = MIMEMultipart(multipart_content_subtype)
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        if text:
            part = MIMEText(text, 'plain')
            msg.attach(part)
        return msg

    def send_mail(self, boto3, sender: str, recipients: list, title: str, text: str) -> dict:
        print("Sending email...")
        msg = self.create_multipart_message(sender, recipients, title, text)
        ses_client = boto3
        return ses_client.send_raw_email(
            Source=sender,
            Destinations=recipients,
            RawMessage={'Data': msg.as_string()}
        )

# # This was used for testing
# if __name__ == '__main__':
#     s = 'xxx@yyy.com'
#     r = ['yyy@xxx.com']
#     ti = "Test"
#     te = "This is the test text"
#     b = "This is the body of the test email"
#     Emailer(s, r, ti, te, b)
