from .models import Like
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        liked_user = instance.liked_user.name.capitalize()
        receiver_id = instance.post.user.id
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        message = {
            "type": "notification_message",
            "receiver_id": receiver_id,
            "message": f"{liked_user} liked your post.",
        }
        async_to_sync(channel_layer.group_send)("notifications_group", message)
