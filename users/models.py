from django.db import models
from django.contrib.auth.models import User
from discussion.models import Discussion, Category, Thread
 
#Gender options
gender_choices = (
    ('Male','Male'),
    ('Female', 'Female'),
    )

class Profile(models.Model):
    """User Profile"""
    # User Information
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, choices=gender_choices)
    age = models.PositiveIntegerField(blank=True, null=True)

    # Profile Information
    bio = models.TextField(max_length=300, blank=True, null=True)
    hometown = models.CharField(max_length=100, blank=True, null=True)

    # Social Connections
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)

    # Status
    verified = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)

    # Connected to user profile.
    liked_threads = models.ManyToManyField(Thread, blank=True, related_name="liked_threads")
    saved_threads = models.ManyToManyField(Thread, blank=True, related_name="saved_threads")
    saved_discussions = models.ManyToManyField(Discussion, blank=True, related_name="saved_discussions")
    liked_discussions = models.ManyToManyField(Discussion, blank=True, related_name="liked_discussions")
    followed_categories = models.ManyToManyField(Category, blank=True, related_name="followed_categories")
    followed_discussions = models.ManyToManyField(Discussion, blank=True, related_name="followed_discussions")

    def discussions_count(self):
        discussions = Discussion.objects.filter(user=self.user).count()
        return discussions

    def threads_count(self):
        threads = Thread.objects.filter(user=self.user).count()
        return threads

    def __str__(self):
        return str(self.user)
