from django.core.management.base import BaseCommand
from app_home.emailAlerts import check_weather_alerts

class Command(BaseCommand):
    help = 'Check weather alerts and send notifications'

    def handle(self, *args, **kwargs):
        try:
            check_weather_alerts()
            self.stdout.write(self.style.SUCCESS('Weather alerts processed successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error processing weather alerts: {e}'))
