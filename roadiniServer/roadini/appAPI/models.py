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

class UserAuth(models.Model):
    userId = models.IntegerField(null=False, blank=False)
    cookie = models.TextField(null=False, blank=False)
    image = models.TextField(null=False, blank=False)

    class Meta:
        unique_together = (("userId",))
        db_table = 'UserAuth'

    def __str__(self):
        return str(self.userId) + "-" + str(self.cookie)

class PostFeed(models.Model):
    userId = models.IntegerField(null=False, blank=False)
    urlStatic = models.TextField(null=False, blank=False)
    authId = models.IntegerField(null=False, blank=False)
    localsIds = models.TextField(null=False, blank=False)
    post_time = models.DateTimeField(blank=False, null=False)

    class Meta:
        unique_together = (("userId","authId"))
        db_table = 'PostFeed'

    def __str__(self):
        return str(self.userId) + "-" + str(self.authId)
