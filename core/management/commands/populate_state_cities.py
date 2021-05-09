import requests
from django.core.management.base import BaseCommand, CommandError


from core.models import City, State


SOURCE_URL = "https://raw.githubusercontent.com/thatisuday/indian-cities-database/master/cities.json"

class Command(BaseCommand):
    help = 'Populate state and city'

    def handle(self, *args, **options):
        res = requests.get(SOURCE_URL)
        json_data = res.json()
        for data in json_data:
            state_name, city_name = data.get('state'), data.get('city')
            state, created = State.objects.get_or_create(name=state_name)
            city = City.objects.get_or_create(name=city_name, state=state)
        self.stdout.write(self.style.SUCCESS('Successfully created "%s" city' % len(json_data[0])))
