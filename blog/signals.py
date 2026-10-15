import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Post

@receiver(pre_delete, sender=Post)
def delete_cover_image(sender, instance, **kwargs):
    if instance.cover_image and os.path.isfile(instance.cover_image.path):
        os.remove(instance.cover_image.path)