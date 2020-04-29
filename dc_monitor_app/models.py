from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Clint(models.Model):
    # CASCADE means when user deleted delete that relation
    # todo add time to modify last seen
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    second_name = models.CharField(max_length=60)
    email = models.CharField(max_length=150, null=True)
    prof_image = models.ImageField(null=True, blank=True, default="default-profile.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    # smart_meter_SER = models.ForeignKey(SmartMeters, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s %s" % (self.first_name, self.second_name)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.second_name)


class Bill(models.Model):
    # "auto_now_add" when first create obj django will initialize time
    # "auto_now when" updating the obj django will update the time
    # todo add timing to the previous conception to do analysis

    categ = [1, 2, 3, 4, 5, 6, 7]
    categories = (
        (categ[0], '1'), (categ[1], '2'), (categ[2], '3'),
        (categ[3], '4'), (categ[4], '5'), (categ[5], '6'), (categ[6], '7'),
    )

    user = models.ForeignKey(Clint, on_delete=models.CASCADE)
    consumption = models.FloatField(default=0.0)
    bill = models.FloatField(default=0.0)
    conception_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    # date = models.DateTimeField(auto_now_add=True, auto_now=True, null=True)
    price_category = models.PositiveSmallIntegerField(
        choices=categories,
        default=categ[0],
    )

    class Meta:
        ordering = ['consumption']

    def __str__(self):
        return "%s bill" % self.user.first_name


class SmartMeters(models.Model):
    # to track data in real time times
    status = (
        (1, "working"),
        (0, "not_working")
    )
    user = models.ForeignKey(Clint, on_delete=models.CASCADE, null=True)
    SER = models.CharField(max_length=10, unique=True, primary_key=True)
    device_status = models.PositiveSmallIntegerField(
        choices=status,
        default=0
    )

    # type
    # location
    # conception = models.FloatField(default=0.0)
    # balance = models.FloatField(default=0.0)
    # conception_cost = models.FloatField(default=0.0)
    # electrical_load = models.FloatField(default=0.0)
    # price_category = models.IntegerField(default=1, validators=[MinValueValidator(1),
    #                                                             MaxValueValidator(7)])

    def __str__(self):
        return "NO. %s" % self.SER
