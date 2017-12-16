from django.core.management.base import BaseCommand, CommandError
import praw
import requests
import sys
import time
from . import cmd_helper
from prawcore.exceptions import RequestException
from sv.models import TSV
from svexdb.settings import REDDIT


class Command(BaseCommand):
    help = 'Searches range of TSV entries to scrape info and/or delete'
    r_praw = praw.Reddit(client_id=REDDIT['client_id_alt'],
                         client_secret=REDDIT['client_secret_alt'],
                         refresh_token=REDDIT['refresh_token_alt'],
                         user_agent=REDDIT['user-agent'],)

    def add_arguments(self, parser):
        parser.add_argument('gen')
        parser.add_argument('start_value')
        parser.add_argument('end_value')

    def handle(self, *args, **options):
        try:
            gen = int(options['gen'])
        except ValueError:
            gen = 7  # default
        try:
            start = int(options['start_value'])
        except ValueError:
            start = 0  # default
        try:
            end = int(options['end_value'])
        except ValueError:
            end = 4096  # default

        for i in range(start, end):
            print("scraping gen", gen, "tsv", i)
            self.scrape_tsv(i, gen)

    def scrape_tsv(self, sv, gen):
        sv_list = TSV.objects.tsv_search(sv, gen)
        for tr in sv_list:
            done = False
            while not done:
                try:
                    cmd_helper.scrape_user_tsv(tr, self.r_praw)
                    done = True
                except(RequestException,
                       praw.exceptions.APIException,
                       praw.exceptions.ClientException,
                       requests.exceptions.ConnectionError,
                       requests.exceptions.HTTPError,
                       requests.exceptions.ReadTimeout,
                       requests.packages.urllib3.exceptions.ReadTimeoutError):
                    err = sys.exc_info()[:2]
                    print(err)
                    time.sleep(45)
            time.sleep(5)

        sv_list_reloaded = TSV.objects.tsv_search(sv, gen)  # has changes resulting from previous loop
        for tr in sv_list_reloaded:
            cmd_helper.delete_if_inactive(tr)


