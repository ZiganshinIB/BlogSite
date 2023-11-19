from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset.filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", 'Draft'
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish') # slug будет настроен как /year/month/day/slug_name
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="blog_post")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    # objects = models.Manager() # for Example
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    # Возврат URL
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
