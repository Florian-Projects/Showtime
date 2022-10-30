import datetime

from django.core.management import BaseCommand

from showtime.apps.google.google_connector import GoogleApiConnector


class Command(BaseCommand):
    def handle(self, *args, **options):
        connector = GoogleApiConnector()
        start_time = datetime.datetime(day=31, month=10, year=2022, hour=20, minute=30)
        exists = connector.check_if_event_exist("Chainsawman", "cool name", 15, start_time)
        if exists:
            print("event already exists")
        else:
            print("Creating event")
            connector.create_new_calender_event("Chainsawman", "cool name", 15, start_time)
