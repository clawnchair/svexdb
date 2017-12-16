from django.db import models
from sv import managers
from sv.helpers import fromtimestamp
import sys


# Create your models here.
class Trainer(models.Model):
    username = models.CharField(max_length=24, unique=True)
    flair_class = models.CharField(max_length=50, null=True, blank=True)
    flair_text = models.CharField(max_length=65, null=True, blank=True)
    activity = models.DateTimeField(null=True, default=None, blank=True)

    objects = managers.TrainerManager()

    def set_activity(self, timestamp):
        dt = fromtimestamp(timestamp)
        if not self.activity or self.activity < dt:
            self.activity = dt
            self.save()

    if sys.version_info >= (3, 0):
        def __str__(self):
            return self.username
    else:
        def __unicode__(self):
            return self.username


class TSV(models.Model):
    trainer = models.ForeignKey(Trainer, related_name='trainer_shiny_values', on_delete=models.CASCADE)
    tsv = models.PositiveSmallIntegerField()
    sub_id = models.CharField(max_length=10)
    completed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created = models.DateTimeField()
    last_seen = models.DateTimeField("most recent op comment")
    pending = models.DateTimeField("oldest unreplied comment", default=None, null=True, blank=True)
    GENERATION_CHOICES = (
        ('6', '6'),
        ('7', '7')
    )
    gen = models.CharField(max_length=2, choices=GENERATION_CHOICES)

    objects = managers.TSVManager()

    if sys.version_info >= (3, 0):
        def __str__(self):
            return self.trainer.username + " " + str(self.tsv) + " " + str(self.sub_id)
    else:
        def __unicode__(self):
            return self.trainer.username + " " + str(self.tsv) + " " + str(self.sub_id)


class Nonreddit(models.Model):
    username = models.CharField(max_length=75, default=None, blank=True, null=True)
    tsv = models.CharField(max_length=4)
    fc = models.CharField(max_length=50, default=None, blank=True, null=True)
    ign = models.CharField(max_length=50, default=None, blank=True, null=True)
    url = models.CharField(max_length=150, default=None, blank=True, null=True)
    timestamp = models.CharField(max_length=30, default=None, blank=True, null=True)
    language = models.CharField(max_length=30, default=None, blank=True, null=True)
    other = models.CharField(max_length=300, default=None, blank=True, null=True)
    source = models.CharField(max_length=30, default=None, blank=True, null=True)

    objects = managers.NonredditManager()

    if sys.version_info >= (3, 0):
        def __str__(self):
            return str(self.source) + " " + str(self.tsv) + " " + str(self.url)
    else:
        def __unicode__(self):
            return str(self.source) + " " + str(self.tsv) + " " + str(self.url)


class Report(models.Model):
    submitter_ip = models.GenericIPAddressField(blank=True, null=True)  # not really used anymore
    url = models.URLField()
    ACTIVITY_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
        ('banned', 'Banned')
    )
    status = models.CharField(max_length=8, choices=ACTIVITY_CHOICES)
    info = models.CharField(max_length=100, blank=True, null=True)
    handled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = managers.ReportManager()

    if sys.version_info >= (3, 0):
        def __str__(self):
            return self.url
    else:
        def __unicode__(self):
            return self.url


class Latest(models.Model):
    latest_id = models.CharField(max_length=50)

    objects = managers.LatestManager()
