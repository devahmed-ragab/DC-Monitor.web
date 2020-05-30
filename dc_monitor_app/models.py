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
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    location = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.IntegerField(null=True, unique=True, blank=True)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.second_name)

    def __str__(self):
        return "%s %s" % (self.first_name, self.second_name)


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
        (0, "OFF"),
        (1, "ON")
    )
    user = models.ForeignKey(Clint, on_delete=models.CASCADE, null=True, blank=True)
    SER = models.CharField(max_length=10, unique=True, primary_key=True)
    device_status = models.PositiveSmallIntegerField(
        choices=status,
        default=0
    )

    def get_status(self):
        return self.status[self.device_status][1]

    def __str__(self):
        return "NO. %s" % self.SER


class ApplianceCategory(models.Model):
    categ_name = [
        ('Home Products Services', 'Home Products Services'),
        ('Air Conditioning', 'Air Conditioning'),
        ('Electronic Pest Control', 'Electronic Pest Control'),
        ('Home Air Cleaners', 'Home Air Cleaners'),
        ('Household Cleaning Equipment', 'Household Cleaning Equipment'),
        ('Laundry Appliances', 'Laundry Appliances'),
        ('Small Home Appliances', 'Small Home Appliances'),
        ('Space Heaters', 'Space Heaters'),
        ('Water Heaters', 'Water Heaters'),
        ('Cooking Appliances', 'Cooking Appliances'),
        ('Dishwashers & Dryers', 'Dishwashers & Dryers'),
        ('Electric Coffee Makers', 'Electric Coffee Makers'),
        ('Electric Kettles & Boiling Appliances', 'Electric Kettles & Boiling Appliances'),
        ('Food Preparation Appliances', 'Food Preparation Appliances'),
        ('Fridges & Freezers', 'Fridges & Freezers'),
        ('Kitchen Ovens', 'Kitchen Ovens'),
        ('Kitchen Stoves, Tops & Hoods', 'Kitchen Stoves, Tops & Hoods'),
        ('Small Kitchen Appliances', 'Small Kitchen Appliances'),
        ('Water Treatment Appliances', 'Water Treatment Appliances'),
        ('Others', 'Others')
    ]
    category = models.CharField(max_length=40, null=True, choices=categ_name)

    def __str__(self):
        return self.category


class Seller(models.Model):
    # todo add branches table
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return "%s " % self.name


class Factory(models.Model):
    name = models.CharField(max_length=100, null=False)

    @property
    def getFactoryNames(self):
        names = self.objects.all()
        return names

    def __str__(self):
        return "%s factory" % self.name


class Appliances(models.Model):
    consumption_labels = [
        (1, 'A+++'), (2, 'A++'), (3, 'A+'),
        (4, 'A'), (5, 'B'), (6, 'C'),
    ]
    sub_category = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=200, blank=False, null=False)
    name = models.CharField(max_length=400, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    warranty = models.FloatField(blank=True)

    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True)
    consumption_label = models.PositiveSmallIntegerField(blank=True, choices=consumption_labels)
    production_Year = models.PositiveSmallIntegerField(null=True, blank=True,
                                                       validators=[MinValueValidator(1999), MaxValueValidator(2100)])
    wattage = models.FloatField(blank=True)

    wight = models.FloatField(blank=True)
    height = models.FloatField(blank=True)
    depth = models.FloatField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=False)

    seller = models.ManyToManyField(Seller, blank=True)
    appliance_category = models.ForeignKey(ApplianceCategory, null=True, on_delete=models.SET_NULL)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, blank=True )

    class Meta:
        ordering = ['appliance_category']

    def __str__(self):
        return "%s" % self.name
