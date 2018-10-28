from django.db import models

# Create your models here.
class PathsTable(models.Model):
    socialID = models.IntegerField(null=False, blank=False)
    pathID = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.socialID) + "-" + str(self.pathID)
