from django.db import models

# Create your models here.
class PathsTable(models.Model):
    socialID = models.IntegerField(null=False, blank=False)
    pathID = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.socialID) + "-" + str(self.pathID)

class ListPostPhoto(models.Model):
    listId = models.IntegerField(null=False, blank=False)
    postId = models.IntegerField(null=False, blank=False)
    imageId = models.TextField(null=False, blank=False)

    class Meta:
        unique_together = (("listId", "postId", "imageId"))
        db_table = 'ListPostPhoto'

    def __str__(self):
        return str(self.listId) + "-" + str(self.postId) + "-" + self.imageId
