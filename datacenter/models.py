from django.db import models
from django.utils import timezone


def format_duration(duration):
    hours = duration // 3600
    minutes = duration // 60 % 60
    return '{}ч {}мин'.format(hours, minutes)


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        leaved = timezone.now()
        if self.leaved_at:
            leaved = self.leaved_at
        seconds_in = (leaved - self.entered_at).total_seconds()
        return int(seconds_in)

    def is_visit_long(self):
        return self.get_duration() >= 3600

    @property
    def duration(self):
        return format_duration(self.get_duration())

    @property
    def who_entered(self):
        return self.passcard.owner_name

    @property
    def is_strange(self):
        return self.is_visit_long()

