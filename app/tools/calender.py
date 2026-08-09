import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.tools.base import BaseTool

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_FILE = "token_calendar.json"


class CalendarTool(BaseTool):

    def name(self):
        return "calendar"

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

        return build('calendar', 'v3', credentials=creds)

    def run(self, input: dict):

        service = self.authenticate()

        start_time = datetime.utcnow().isoformat() + 'Z'
        end_time = (datetime.utcnow() + timedelta(hours=1)).isoformat() + 'Z'

        event = {
            'summary': input.get("title"),
            'start': {'dateTime': start_time},
            'end': {'dateTime': end_time},
        }

        event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        return f"📅 Event created: {event.get('htmlLink')}"