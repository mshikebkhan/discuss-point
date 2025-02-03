from django.db import models
from django.contrib.auth.models import User
from notifications.models import Notification

from django.db.models.signals import post_save, post_delete

class Category(models.Model):
    """Category to which discussions are connected."""
    title = models.CharField(max_length=100, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    followers = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"

    def discussions_count(self):
        discussions = Discussion.objects.filter(category=self).count()
        return discussions

    def __str__(self):
    	return self.title


#category_choices
category_choices = Category.objects.values_list('title', 'title')

class Discussion(models.Model):
    """Discussion"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300, choices=category_choices)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=150, null=True, blank=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    closed = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)

    followers = models.ManyToManyField(User, blank=True, related_name="discussion_followers")

    def threads_count(self):
        threads = Thread.objects.filter(discussion=self).count()
        return threads

    def __str__(self):
    	return self.title


class Thread(models.Model):
    """Threads on Discussions"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    content = models.TextField(max_length=300, null=True, blank=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    likes = models.PositiveIntegerField(default=0)

    reported = models.BooleanField(default=False)


    def user_submit_thread(sender, instance, *args, **kwargs):
        """Add notification if user submit thread in current user's discussion."""
        thread = instance
        discussion = thread.discussion

        if thread.user != discussion.user:
            preview = thread.content[:70]
            sender = thread.user
            notify = Notification(thread=thread, discussion=discussion,  sender=sender, user=discussion.user, preview=preview ,notification_type=3)
            notify.save()
            for follower in thread.discussion.followers.all():
                if follower != thread.user:
                    notify = Notification(thread=thread, discussion=discussion,  sender=sender, user=follower, preview=preview ,notification_type=4)
                    notify.save()

    def user_del_submit_thread(sender, instance, *args, **kwargs):
        """Remove notification if user removes thread."""
        thread = instance
        discussion = thread.discussion
        sender =thread.user
        notify = Notification.objects.filter(thread=thread, sender=sender, notification_type=3)
        notify.delete()
        for follower in thread.discussion.followers.all():
            notify = Notification.objects.filter(thread=thread, discussion=discussion,  sender=sender, user=follower, preview=preview ,notification_type=4)
            notify.delete()

    def __str__(self):
    	return self.content[:90]

#Thread notfy.
post_save.connect(Thread.user_submit_thread, sender=Thread)
post_delete.connect(Thread.user_del_submit_thread, sender=Thread)
