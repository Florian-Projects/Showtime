from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleApiConnector:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    def __init__(self):
        self.get_auth_token()
        self.calender_service = build('calendar', 'v3', credentials=self.creds)

    def get_auth_link(self):
        pass

    def get_auth_token(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def get_calender_events(self, num_events):
        try:
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 9 events')
            events_result = self.calender_service.events().list(calendarId='primary', timeMin=now,
                                                                maxResults=num_events, singleEvents=True,
                                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 9 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)

    def create_new_calender_event(self, show_name: str, episode_name: str, episode_number: int, date: datetime.datetime):
        event = {
            'summary': f"{show_name} {episode_number} {episode_name}",
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': date.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': (date + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Europe/London',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        event = self.calender_service.events().insert(calendarId='primary', body=event).execute()


if __name__ == "__main__":
    connector = GoogleApiConnector()
    connector.create_new_calender_event("Chainsawman", "cool name", 15, datetime.datetime.utcnow() + datetime.timedelta(hours=2))
