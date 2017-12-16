from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from .cmd_helper import is_from_tsv_thread
from .cmd_helper import get_gen_from_flair_class
from sv.models import Latest, TSV, Report
from svexdb.settings import REDDIT
from prawcore import RequestException
import praw
import requests
import sys
import time


class Command(BaseCommand):
    help = 'Gets latest submissions and adds/updates new TSV threads'
    r = praw.Reddit(client_id=REDDIT['client_id'],
                    client_secret=REDDIT['client_secret'],
                    refresh_token=REDDIT['refresh_token'],
                    user_agent=REDDIT['user-agent'],)

    def handle(self, *args, **options):
        done = False
        while not done:
            try:
                self.new_submissions()
                done = True
            except(RequestException,
                   praw.exceptions.APIException,
                   praw.exceptions.ClientException,
                   requests.exceptions.ConnectionError,
                   requests.exceptions.HTTPError,
                   requests.exceptions.ReadTimeout,
                   requests.packages.urllib3.exceptions.ReadTimeoutError):
                err = sys.exc_info()[:2]
                self.stderr.write(str(err))
                time.sleep(45)

    def new_submissions(self):
        stop_id = Latest.objects.get_latest_tsv_thread_id()
        generator = self.r.subreddit('SVExchange').new(limit=50)

        for i, sub in enumerate(generator):
            if i == 0:
                Latest.objects.set_latest_tsv_thread_id(sub.id)

            if sub.id <= stop_id:
                from datetime import datetime
                self.stdout.write("new_submissions [Stop] " + str(datetime.utcnow()))
                break
            elif is_from_tsv_thread(sub.title, sub.link_flair_css_class):
                op = sub.author.name
                sv = int(sub.title)
                gen = get_gen_from_flair_class(sub.link_flair_css_class)
                info_str = "%s %s %s %s" % (op, sub.title, gen, sub.id)

                should_update = True
                if TSV.objects.check_if_exists(op, sv, gen):  # update existing TSV entry
                    self.stdout.write("Updated? " + info_str)
                    existing = TSV.objects.get_user_tsv(op, sv, gen)
                    from sv.helpers import fromtimestamp
                    dt_new = fromtimestamp(sub.created_utc)
                    delta = dt_new - existing.created
                    if sub.id > existing.sub_id and delta.days < 60:
                        should_update = False
                        x = "Creating new threads too soon? u/%s - old thread: %s" % (op, existing.sub_id)
                        Report.objects.create_automated_report(sub.id, x)
                else:
                    uniq_str = " *UNIQUE*" if len(TSV.objects.tsv_search(sv, gen)) == 0 else ""
                    self.stdout.write("Added " + info_str + uniq_str)

                if should_update:
                    TSV.objects.update_or_create_user_tsv(op, sub.author_flair_text, sub.author_flair_css_class, sv,
                                                          gen, sub.id, False, False, sub.created_utc, sub.created_utc,
                                                          None)
        mult = 60 + 5  # minutes until cache invalidates. assuming hourly cron job
        cache.set('u6', TSV.objects.get_unique_count('6'), 60 * mult)
        cache.set('u7', TSV.objects.get_unique_count('7'), 60 * mult)
