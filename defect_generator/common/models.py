from django.db import models


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True