import os
import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.tools.base import BaseTool

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = "token.json"


class GmailTool(BaseTool):

    def name(self):
        return "gmail"

    def authenticate(self):
        creds = None

        # ✅ Load existing token
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # ❗ If no token → login
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

            # ✅ Save token
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def run(self, input: dict):

        service = self.authenticate()

        message = MIMEText(input["body"])
        message['to'] = input["to"]
        message['subject'] = input["subject"]

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        message = {'raw': raw}

        sent = service.users().messages().send(
            userId="me",
            body=message
        ).execute()

        return f"✅ Email sent! ID: {sent['id']}"
        
        
        