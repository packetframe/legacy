import yaml

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)


def send_email(recipient, subject, message):
    msg = MIMEText(message, "plain")
    msg["Subject"] = subject
    msg["From"] = config["email"]["username"]

    server = SMTP(config["email"]["server"])
    server.login(config["email"]["username"], config["email"]["password"])
    server.sendmail(config["email"]["username"], [recipient], msg.as_string())
    server.quit()
