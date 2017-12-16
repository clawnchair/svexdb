from django.core.management.base import BaseCommand, CommandError
from sv.models import Latest


class Command(BaseCommand):
    help = 'Initalizes entries in Latest model for use by comment_scrape and new_submissions'

    def add_arguments(self, parser):
        parser.add_argument('subm_id')
        parser.add_argument('comment_id')

    def handle(self, *args, **options):
        s, x = Latest.objects.get_or_create(id=1)
        c, x = Latest.objects.get_or_create(id=2)
        if options['subm_id']:
            s.latest_id = options['subm_id']
        else:
            s.latest_id = '700000'

        if options['comment_id']:
            c.latest_id = options['comment_id']
        else:
            c.latest_id = 'ddddddd'

        s.save()
        c.save()

        if len(Latest.objects.all()) == 2:
            print("Success")
        else:
            print("Failed")
