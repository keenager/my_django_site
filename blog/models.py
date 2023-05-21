from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField(default=timezone.now)
    tag = models.CharField(max_length=50)
    content = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
