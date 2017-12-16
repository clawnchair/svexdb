from sv.models import TSV
from sv.helpers import fromtimestamp
import datetime
import praw
import re
import sys
import time


def scrape_user_tsv(user_tsv, r_praw, timestamp=None):
    if user_tsv.archived:  # known to be archived. no need to check
        return

    username = user_tsv.trainer.username
    tsv = user_tsv.tsv
    gen = user_tsv.gen
    sub_id = user_tsv.sub_id

    subm = r_praw.submission(id=sub_id)
    subm.comment_sort = 'new'
    subm.comments.replace_more(limit=1)

    if subm.author is None:  # or subm.author == "[deleted]":  # deleted by user
        TSV.objects.delete_user_tsv(username, tsv, gen, "Deleted by OP %s %s" % (username, tsv))
    elif subm.selftext == '':
        TSV.objects.delete_user_tsv(username, tsv, gen, "Deleted by mods %s %s" % (username, tsv))
    elif subm.link_flair_css_class == "banned":
        TSV.objects.delete_user_tsv(username, tsv, gen, "Banned by mods %s %s" % (username, tsv))
    else:  # thread hasn't been deleted
        if user_tsv.completed != subm.over_18 and not subm.archived:
            blah = "Marked completed" if subm.over_18 else "Re-opened"
            TSV.objects.set_completed(username, tsv, gen, subm.over_18, blah + " %s %s" % (username, tsv))
        if user_tsv.archived != subm.archived:
            TSV.objects.set_archived(username, tsv, gen, "Archived %s %s" % (username, tsv))

        cf = subm.comments  # root level comment forest

        sys.stdout.write("* scraping %s by %s\n" % (subm.id, str(subm.author)))
        pending_ts = oldest_unreplied_root_comment(cf)

        # get time of latest hatch
        flattened_comments = flatten_and_sort_new(cf)

        if timestamp:
            # latest (int) timestamp was passed in from realtime scraper
            most_recent_ts = timestamp
        else:
            # latest needs to be found
            most_recent_ts = user_tsv.last_seen.timestamp()

            for fc in flattened_comments:
                # find op's most recent comment in thread
                if fc.is_submitter:
                    comment_ts = fc.created_utc
                    if comment_ts > most_recent_ts:
                        most_recent_ts = comment_ts

        # for debug purposes only
        most_rec_dt = fromtimestamp(most_recent_ts)  # convert timestamp to datetime
        previous_time_dt = user_tsv.last_seen
        if most_rec_dt > previous_time_dt:
            delta = fromtimestamp(datetime.datetime.utcnow()) - most_rec_dt
            between = most_rec_dt - previous_time_dt
            sys.stdout.write("\t* %s %s\t%s\t%s\n" % (username.ljust(24), str(tsv).zfill(4), str(delta), str(between)))

        TSV.objects.update_user_tsv_scrape(username,
                                           tsv,
                                           gen,
                                           most_recent_ts,
                                           pending_ts,
                                           subm.author_flair_text,
                                           subm.author_flair_css_class,
                                           subm.created_utc)
    time.sleep(5)


def oldest_unreplied_root_comment(comment_forest):
    if len(comment_forest) == 0:
        return None

    oldest_timestamp = None

    for i, root in enumerate(comment_forest):
        if comment_exists(root) and not root.is_submitter and not comment_should_be_ignored(root):
            replies_forest = root.replies
            replies_forest.replace_more(limit=1)  # consume any 'continue this thread -->'
            sorted_replies = flatten_and_sort_new(replies_forest)

            replied_to = False
            for f in sorted_replies:
                if f.is_submitter:
                    replied_to = True
                    sys.stdout.write("\t* root %s\treplied_to %s\tby %s\n" % (root.id, str(replied_to), f.id))
                    break

            if not replied_to:
                oldest_timestamp = root.created_utc  # found older unreplied root comment
                sys.stdout.write("\t* root %s\treplied_to %s\n" % (root.id, replied_to))
            else:
                if i == 0:  # Most recent comment has been replied to. No need to look further.
                    return None
                break

    return oldest_timestamp


def comment_exists(comment):
    return (isinstance(comment, praw.models.Comment) and
           comment.author is not None)


def comment_should_be_ignored(comment):
    ignored_users = ['AutoModerator', 'FlairHQ', 'Porygon-Bot']
    return (comment.body.lower().find('giveaway') > -1 or
            comment.body.lower().find('claim') > -1 or
            comment.author.name in ignored_users or
            comment.author_flair_css_class == "banned")


def flatten_and_sort_new(comment_forest):
    flatten = comment_forest.list()
    return sorted(flatten, key=lambda x: x.created_utc, reverse=True)


def get_id(url):
    # extracts submission id from reddit shortlink (PRAW's get_submission does not support shortlinks)
    sub_re = re.compile(r"http://redd.it/(?P<sub_id>\w+)+")
    m = sub_re.search(url)
    if m:
        return m.group('sub_id')
    else:
        return None


def get_id_from_full_url(long_url):
    sub_re = re.compile(r"comments/(?P<sub_id>\w+)+/\d\d\d\d")
    m = sub_re.search(long_url)
    if m:
        return m.group('sub_id')
    else:
        return None


def is_from_tsv_thread(title, flair="sv7"):
    if re.search('\d\d\d\d', title):
        return len(title) == 4 and (flair == "sv6" or flair == "sv7")
    else:
        return False


def get_gen_from_flair_class(flair):
    if flair == "sv6":
        return "6"
    elif flair == "sv7":
        return "7"
    else:
        return "7"


def get_gen_from_comment(op, tsv, sub_id, r_praw):
    if (TSV.objects.check_if_exists(op, tsv, '6') and TSV.objects.check_if_exists(op, tsv, '7')):
        # rare case where a Trainer has the same TSV for both gens -> retrieve gen from submission id
        subm = r_praw.submission(id=sub_id)
        return get_gen_from_flair_class(subm.link_flair_css_class)
    else:
        return TSV.objects.get_user_tsv(op, tsv).gen


def delete_if_inactive(user_tsv):
    pending = user_tsv.pending
    if pending:
        now = fromtimestamp(datetime.datetime.utcnow())
        delta1 = now - user_tsv.trainer.activity  # last seen in subreddit
        delta2 = now - pending
        threshold = 30  # days
        if delta1.days > threshold and delta2.days > threshold:
            username = user_tsv.trainer.username
            TSV.objects.delete_user_tsv(username,
                                        user_tsv.tsv,
                                        user_tsv.gen,
                                        "Purged from db for inactivity - %s %s" % (username, user_tsv.tsv))
            return
    if user_tsv.archived:
        now = fromtimestamp(datetime.datetime.utcnow())
        delta = now - user_tsv.created
        threshold = 215  # archived has been for 30+ days
        if delta.days > threshold:
            username = user_tsv.trainer.username
            TSV.objects.delete_user_tsv(username,
                                        user_tsv.tsv,
                                        user_tsv.gen,
                                        "Purged from db for nonrenewal - %s %s" % (username, user_tsv.tsv))
