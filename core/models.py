from django.db import models
from django.contrib.auth.models import User
from notifications.models import Notification

from django.db.models.signals import post_save, post_delete


class AdminPost(models.Model):
    """Official posts from admin."""
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
    	return self.content

    def admin_create_post(sender, instance, *args, **kwargs):
        """Add notification if admin created a new post."""
        post = instance
        for user in  User.objects.all():
            if user.username != "admin":
                notify = Notification(post=post, user=user, notification_type=5)
                notify.save()

    def admin_delete_post(sender, instance, *args, **kwargs):
        """Remove notification if admin delete post."""
        post = instance
        for user in  User.objects.all():
            notify = Notification.objects.filter(post=post, user=user, notification_type=5)
            notify.delete()

# Admin Post Notify
post_save.connect(AdminPost.admin_create_post, sender=AdminPost)
post_delete.connect(AdminPost.admin_delete_post, sender=AdminPost)
