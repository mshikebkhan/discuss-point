from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """Display notifications."""
    NOTIFICATION_TYPES = ((1,'Like Discussion'),(2,'Like Thread'), (3,'Submit Thread'), (4,'Submit Thread In Follows'), (5, 'New Admin Post'))

    discussion = models.ForeignKey('discussion.Discussion', on_delete=models.CASCADE, related_name="noti_discussion", blank=True, null=True)
    thread = models.ForeignKey('discussion.Thread', on_delete=models.CASCADE, related_name="noti_thread", blank=True, null=True)
    post = models.ForeignKey('core.AdminPost', on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    preview = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
