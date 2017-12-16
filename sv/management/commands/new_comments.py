from django.core.management.base import BaseCommand, CommandError
from sv.models import Latest, Trainer, TSV
from . import cmd_helper
from svexdb.settings import REDDIT
from prawcore.exceptions import RequestException
import praw
import requests
import sys
import time
import unicodedata2


class Command(BaseCommand):
    help = 'Crawls latest comments to update last seen data'
    r_praw = praw.Reddit(client_id=REDDIT['client_id'],
                         client_secret=REDDIT['client_secret'],
                         refresh_token=REDDIT['refresh_token'],
                         user_agent=REDDIT['user-agent'],)

    def handle(self, *args, **options):
        stopping_id = Latest.objects.get_latest_comment_id()
        done = False
        while not done:
            try:
                new_stopping_id = self.process_latest_comments(stopping_id)
                Latest.objects.set_latest_comment_id(new_stopping_id)
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

    def process_latest_comments(self, stopping_id):
        new_stopping_id = stopping_id
        COMMENTS_LIMIT = 100  # intended for a cron job every 15 minutes
        comments = self.r_praw.subreddit('SVExchange').comments(limit=COMMENTS_LIMIT)
        user_tsv_set = set([])  # stores user/tsv combo to avoid duplicates
        user_set = set()  # stores users to avoid duplicates
        for i, c in enumerate(comments):
            if i == 0:
                new_stopping_id = c.id

            link_title_ascii = unicodedata2.normalize('NFKD', c.link_title).encode('ascii', 'ignore').decode('ascii')
            self.stdout.write("%s %s %s" % (c.id, c.link_author.ljust(24), link_title_ascii))
            if c.id <= stopping_id:
                from datetime import datetime
                self.stdout.write("new_comments [Stop] " + str(datetime.utcnow()))
                break
            op = c.link_author
            commenter = c.author.name
            if c.is_submitter and cmd_helper.is_from_tsv_thread(c.link_title):
                user_tsv_tuple = (op, c.link_title)
                tsv = int(c.link_title)
                ts = c.created_utc
                if user_tsv_tuple in user_tsv_set:
                    self.stdout.write("\tRepeat")
                elif TSV.objects.check_if_exists(op, tsv):
                    self.stdout.write("\tUpdating")
                    new_sub_id = cmd_helper.get_id_from_full_url(c.link_url)
                    # comment lacks gen info that's found in submission flair
                    gen = cmd_helper.get_gen_from_comment(op, tsv, new_sub_id, self.r_praw)
                    user_tsv = TSV.objects.get_user_tsv(op, tsv, gen)
                    # check if submission id should be updated, in case db doesn't have user's latest thread
                    old_sub_id = user_tsv.sub_id

                    if new_sub_id > old_sub_id:
                        user_tsv.sub_id = new_sub_id
                        user_tsv.save()

                    cmd_helper.scrape_user_tsv(user_tsv, self.r_praw, ts)
                else:
                    self.stdout.write("\tAdding?")
                    sub_id = cmd_helper.get_id_from_full_url(c.link_url)
                    subm = self.r_praw.submission(id=sub_id)
                    if not subm.over_18:
                        self.stdout.write("\tAdd")
                        gen = cmd_helper.get_gen_from_flair_class(subm.link_flair_css_class)
                        TSV.objects.update_or_create_user_tsv(op, subm.author_flair_text, subm.author_flair_css_class,
                                              tsv, gen, sub_id, False, False,
                                              subm.created_utc, ts, None)
                user_tsv_set.add(user_tsv_tuple)
            else:
                if commenter not in user_set:
                    user_set.add(commenter)
                    tr = Trainer.objects.get_user(commenter)
                    if tr:
                        tr.set_activity(c.created_utc)

        return new_stopping_id
