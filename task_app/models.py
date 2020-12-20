from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.validators import RegexValidator
from django.db import models

alphabetic = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alpha-numeric characters are allowed.')


# Create your models here.
class Tasks(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, validators=[alphabetic])
    description = models.CharField(max_length=255, blank=False, null=False)
    done = models.BooleanField(default=False)

    class Meta:
        db_table = 'tasks'  # define your custom name

    def save(self, *args, **kwargs):
        super(Tasks, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.name
