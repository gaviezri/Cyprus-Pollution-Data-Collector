import json
import logging
import traceback

from constants.report import *
from constants.config import USER, PASS
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext


site_url = "https://ctcoeu.sharepoint.com/sites/ITDepartment"
client_id = "1ccc128d-9d63-43c4-b75a-c5501b320098"
client_secret_id = "ef2e34b1-fed5-42f7-b73b-912e1c233ea0"
client_secret_value = "kzt8Q~qnEOwusgG-HL675gYuCsEKlXDz4ViVAdkB"
folder_url = "Shared Documents/Cyprus Pollutants Data"

class SharePointReporter:
    def __init__(self):
        self.report_path = None
        with open(CRED_PATH, 'r') as cred:
            cred = json.load(cred)
        self.username = cred[USER]
        self.password = cred[PASS]
        try:
            client_credentials = UserCredential(self.username,self.password)
            self.ctx = ClientContext(site_url).with_credentials(client_credentials)
            self.folder = self.ctx.web.get_folder_by_server_relative_url(folder_url)
            self.ctx.load(self.folder)
            self.ctx.execute_query()
        except Exception as e:
            logging.critical(f"{e}\n{traceback.format_exc()}")
    def send(self):
        try:
            with open(self.report_path, 'rb') as report:
                report_content = report.read()
            file_name = f"{self.report_path.stem}.xlsx"
            self.folder.upload_file(file_name, report_content).execute_query()
            logging.info(file_name + " was uploaded successfully to sharepoint!")
        except Exception as e:
            logging.critical(f"{e}\n{traceback.format_exc()}")
