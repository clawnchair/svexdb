from django.core.management.base import BaseCommand, CommandError
import datetime
import praw
import sys
import time
from sv.models import TSV
from svexdb.settings import REDDIT
from .cmd_helper import get_gen_from_flair_class, is_from_tsv_thread


class Command(BaseCommand):
    help = 'Searches subreddit for a specified range of TSV entries to be added'
    r = praw.Reddit(client_id=REDDIT['client_id_alt'],
                    client_secret=REDDIT['client_secret_alt'],
                    refresh_token=REDDIT['refresh_token_alt'],
                    user_agent=REDDIT['user-agent'],)
    users = []

    def handle(self, *args, **options):
        if sys.version_info >= (3, 0):
            start = int(input('Enter start of range: '))
            end = int(input('Enter end of range: '))
        else:  # python 2 support
            start = int(raw_input('Enter start of range: '))
            end = int(raw_input('Enter end of range: '))

        for i in range(start, end):
            self.search_reddit(i)
            self.users = []  # reset
            time.sleep(3)

    def search_reddit(self, sv):
        zero_padded_sv = str(sv).zfill(4)
        query = 'nsfw:no AND title:' + zero_padded_sv
        search_results = self.r.subreddit('SVExchange').search(query, sort='new', time_filter='year')
        for subm in search_results:
            if is_from_tsv_thread(subm.title, subm.link_flair_css_class):
                self.process_search_entry(subm)

    def process_search_entry(self, subm):
        op = subm.author.name
        sv = int(subm.title)
        pair = (op, sv)
        gen = get_gen_from_flair_class(subm.link_flair_css_class)
        self.stdout.write("search result: " + subm.title + " by " + op)
        if TSV.objects.check_if_exists(op, sv, gen):
            self.stdout.write("\tdupe")
        else:
            if subm.archived:
                self.stdout.write("\tarchived")
                return  # reached an archived submission. any submission thereafter is also archived
            elif pair in self.users:
                self.stdout.write("\talready searched and added newer thread")
            else:  # check the thread
                thread = self.r.submission(subm.id)
                thread.comment_limit = 40
                thread.comment_sort = 'new'
                time.sleep(3)
                thread.comments.replace_more(limit=1)
                flattened_comments = thread.comments.list()
                should_add = len(flattened_comments) == 0 or not self.is_too_old(thread.created_utc, 60)  # 2 months
                latest_timestamp = thread.created_utc  # placeholder

                for fc in flattened_comments:
                    if fc.is_submitter:
                        if not self.is_too_old(fc.created_utc, 150):
                            # add if op activity within last 150 days
                            self.stdout.write("\t\tshould_add %s" % should_add)
                            should_add = True
                            if fc.created_utc > latest_timestamp:
                                latest_timestamp = fc.created_utc
                            break

                if should_add:
                    TSV.objects.update_or_create_user_tsv(op, thread.author_flair_text,
                                                          thread.author_flair_css_class, sv,
                                                          gen, thread.id, False, False, thread.created_utc,
                                                          latest_timestamp, None)
                    self.stdout.write("\t\tadding " + str(sv) + " *********************")
        self.users.append(op)

    def is_too_old(self, ts, threshold):
        dt = datetime.datetime.fromtimestamp(ts)
        # dt is a datetime object. threshold is int of days
        dtr = dt.replace(tzinfo=None)
        delta = datetime.datetime.utcnow() - dtr
        self.stdout.write("\t\tis_too_old %s" % str(delta.days > threshold))
        return delta.days > threshold
