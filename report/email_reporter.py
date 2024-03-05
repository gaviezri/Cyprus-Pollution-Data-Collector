import json
from pathlib import WindowsPath
from api.timestamp_maker import TimestampMaker
from constants.config import *
from constants.report import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging


class EmailReporter:
    def __init__(self):
        self.report_path: WindowsPath = None
        self.message = None
        with open(CONFIG_PATH, 'r') as config_file:
            config = json.load(config_file)
        self.targets = config[EMAIL_TARGETS]
        with open(CRED_PATH, 'r') as cred_path:
            cred = json.load(cred_path)
        self.username = cred[USER]
        self.password = cred[PASS]

    def send(self):
        message = MIMEMultipart()
        message['Subject'] = f"{SUBJECT}{TimestampMaker.get_prev_month_for_email()}"
        message['From'] = self.username
        message['To'] = ', '.join(self.targets)
        message.attach(MIMEText(self.message, 'plain'))

        with open(self.report_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {self.report_path.stem}.xlsx")
        message.attach(part)

        try:
            # SEE LATER
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, self.targets, message.as_string())
            server.quit()
            logging.info("Email sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
