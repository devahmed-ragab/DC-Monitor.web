from django.db.models.signals import post_save
from .models import Clint, User
from django.contrib.auth.models import Group
from django.dispatch import receiver


# connect receiver 'function' to sender  'model'
# EX:
#   After User.save tiger  'create_user_signal'
#   post_save.connect(create_user_signal, User)


@receiver(post_save, sender=User)
def create_user_signal(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='user')
        instance.groups.add(group)
        Clint.objects.create(user=instance)





