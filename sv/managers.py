from django.db import models
from sv.helpers import fromtimestamp


class TrainerManager(models.Manager):
    def user_search(self, username):
        return self.filter(username__iexact=username)

    def check_if_exists(self, username):
        return self.filter(username=username).exists()

    def get_user(self, username):
        return self.filter(username=username).first()


class TSVManager(models.Manager):
    def get_user_tsv(self, username, tsv, gen=None):
        if gen:
            return self.filter(trainer__username=username, tsv=tsv, gen=gen).first()
        else:
            return self.filter(trainer__username=username, tsv=tsv).first()

    def update_or_create_user_tsv(self, username, flair_text, flair_class, sv,
                                  gen, sub_id, completed, archived, created, last_seen, pending):
        from sv.models import Trainer
        trainer, tr_created = Trainer.objects.get_or_create(username=username,
                                                            defaults={'flair_text': flair_text,
                                                                      'flair_class': flair_class})
        # Update TSV through new submissions crawler
        created_dt = fromtimestamp(created) if created else None
        last_seen_dt = fromtimestamp(last_seen) if last_seen else None
        pending_dt = fromtimestamp(pending) if pending else None
        trainer.set_activity(last_seen_dt)

        tsv, tsv_created = self.update_or_create(trainer=trainer,
                                                 tsv=sv,
                                                 gen=gen,
                                                 defaults={
                                                    'sub_id': sub_id,
                                                    'completed': completed,
                                                    'archived': archived,
                                                    'created': created_dt,
                                                    'last_seen': last_seen_dt,
                                                    'pending': pending_dt})

    def update_user_tsv_scrape(self, username, sv, gen, recent_ts, pending_ts, flair_text, flair_class, created_ts):
        # recent_ts, pending_ts are float timestamps
        from sv.models import Trainer
        tr = Trainer.objects.get_user(username)
        tr.flair_text = flair_text
        tr.flair_class = flair_class
        tr.save()
        tr.set_activity(recent_ts)

        t = self.get_user_tsv(username, sv, gen)
        t.last_seen = fromtimestamp(recent_ts)
        t.pending = fromtimestamp(pending_ts) if pending_ts else None
        t.created = fromtimestamp(created_ts)
        t.save()

    def set_archived(self, username, sv, gen, info=''):
        t = self.get_user_tsv(username, sv, gen)
        t.archived = True
        t.completed = True
        t.save()
        from sv.models import Report
        Report.objects.create_automated_report(t.sub_id, info)

    def set_completed(self, username, sv, gen, completed, info=''):
        t = self.get_user_tsv(username, sv, gen)
        t.completed = completed
        t.save()
        from sv.models import Report
        Report.objects.create_automated_report(t.sub_id, info)

    def set_pending(self, username, sv, gen, timestamp_int):
        t = self.get_user_tsv(username, sv, gen)
        if t:
            t.pending = fromtimestamp(timestamp_int)
            t.save()

    def delete_user_tsv(self, username, sv, gen, info=''):
        t = self.get_user_tsv(username, sv, gen)
        from sv.models import Report
        Report.objects.create_automated_report(t.sub_id, info)
        t.delete()

    def tsv_search(self, sv, gen):
        if not isinstance(sv, int):  # tsv is stored as int in Trainer model
            sv = int(sv)
        return self.filter(tsv=sv, gen=gen).order_by('trainer__username')

    def check_if_exists(self, username, sv, gen=None):
        if gen:
            return self.filter(trainer__username=username, tsv=sv, gen=gen).exists()
        else:  # for comment scrape, which cannot directly know sv gen from only comment properties
            return self.filter(trainer__username=username, tsv=sv).exists()

    def tsv_is_not_found(self, sv, gen):
        return not self.filter(tsv=sv, gen=gen).exists()

    def get_unique_count(self, gen):
        return len(self.filter(gen=gen).order_by('tsv').distinct('tsv'))


class NonredditManager(models.Manager):
    def tsv_search(self, sv):
        if not isinstance(sv, str):  # tsv is stored as str in Nonreddit model
            sv = str(sv)
        return self.filter(tsv=sv).order_by('source').values()


class LatestManager(models.Manager):
    def get_latest_tsv_thread_id(self):
        return self.get(id=1).latest_id

    def set_latest_tsv_thread_id(self, sub_id):
        latest = self.get(id=1)
        latest.latest_id = sub_id
        latest.save()

    def get_latest_comment_id(self):
        # kind of hacky: comment id is stored in 2nd row of Latest model
        return self.get(id=2).latest_id

    def set_latest_comment_id(self, sub_id):
        latest = self.get(id=2)
        latest.latest_id = sub_id
        latest.save()


class ReportManager(models.Manager):
    def create_automated_report(self, sub_id, info):
        if info.startswith("Deleted"):
            status = 'deleted'
        elif info.startswith("Banned"):
            status = 'banned'
        elif info.startswith("Creating"):
            status = 'active'
        else:
            status = 'inactive'
        r, r_created = self.update_or_create(submitter_ip='0.0.0.0',
                                             url='reddit.com/'+sub_id,
                                             status=status,
                                             info=info)
