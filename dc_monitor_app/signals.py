from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.utils.datetime_safe import datetime

from dc_monitor_app.monitor_calculations import calc_price_categ
from .models import Clint, User, SmartMeters, Bill
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


# connect receiver 'function' to sender  'model'
# EX:
#   After User.save tiger  'create_user_signal'
#   post_save.connect(create_user_signal, User)


@receiver(post_save, sender=User)
def create_clint_signal(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='user')
        instance.groups.add(group)
        Clint.objects.create(user=instance)


@receiver(post_save, sender=SmartMeters)
def create_bill_signals(sender, instance, created, **kwargs):
    user = instance.user
    if user:
        all_meters = SmartMeters.objects.filter(user=user).aggregate(Sum('consumption'), Sum('conception_cost'))
        all_meters_consum = all_meters['consumption__sum']
        all_meters_cost = all_meters['conception_cost__sum']
        print(f"bill_signals: all_meters_consum = {all_meters_consum} km, \n all_meters_cost = {all_meters_cost}")
        print(f"create_bill_signals : ")
        Bill.objects.update_or_create(user=user,
                                      defaults={
                                          'consumption': f"{all_meters_consum}",
                                          'price_category': f"{calc_price_categ(all_meters_consum)}",
                                          'conception_date': timezone.now(),
                                          'bill': all_meters_cost
                                      })


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
