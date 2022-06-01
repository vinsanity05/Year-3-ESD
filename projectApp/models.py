from django.db import models
import string
import random
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
import datetime
from django.contrib.auth.models import AbstractUser, Group
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator, MinLengthValidator, MaxLengthValidator, RegexValidator


# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'account_manager'),
        (2, 'cinema_manager'),
        (3, 'admin'),
        (4, 'student')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)


class StudentClub(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=50)
    landLine = models.CharField(max_length=50)
    address = models.TextField(max_length=50)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)

    def __str__(self):
        return "%s" % (self.name)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def pass_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ClubRepresentative(models.Model):
    club = models.ForeignKey(StudentClub, on_delete=models.CASCADE, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    date_of_birth = models.DateField()

    # userid = models.CharField(max_length=50, null=False, blank=False, unique=True)
    userid = models.CharField(max_length=6, null=True, blank=True, unique=True)
    password = models.CharField(max_length=8, null=True, blank=True, unique=True)

    # password = models.CharField(max_length=32)

    # Sample of an ID generator - could be any string/number generator
    # For a 6-char field, this one yields 2.1 billion unique IDs

    def save(self):
        if not self.userid:
            # Generate ID once, then check the db. If exists, keep trying.
            self.userid = id_generator()
            while ClubRepresentative.objects.filter(userid=self.userid).exists():
                self.userid = id_generator()
        if not self.password:
            # Generate ID once, then check the db. If exists, keep trying.
            self.password = pass_generator()
            while ClubRepresentative.objects.filter(password=self.password).exists():
                self.password = pass_generator()
        super(ClubRepresentative, self).save()

    def __str__(self):
        return "%s" % (self.first_name)


class Cinema(models.Model):

    # Default to False intially
    socialDist = models.BooleanField(default=False)

    class Meta:
        db_table = "projectApp_cinema"

    def __str__(self):
        template = 'UWEFlix'
        return template.format(self) 




class Film(models.Model):
    ratting_choices = (
       ('U', 'U'),
        ('PG', 'PG'),
        ('12A', '12A'),
        ('15+', '15+'),
        ('18+', '18+'),
    )
    title = models.CharField(max_length=50, null=False, blank=False)
    age_rating = models.CharField(blank=False, null=False, max_length=7, choices=ratting_choices, default='string')
    duration = models.DurationField()
    description = models.TextField()

    def __str__(self):
        return "%s" % (self.title)


class Screen(models.Model):
    screen_number = models.IntegerField()
    seats = models.IntegerField()

    def __str__(self):
        return "%s" % (str(self.screen_number))


class Show(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField()
    time = models.TimeField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, null=False, blank=False)
    adult_price = models.FloatField("Adult Price", default=0, validators=[MinValueValidator(0, message=None)])
    student_price = models.FloatField("Student Price", default=0, validators=[MinValueValidator(0, message=None)])
    child_price = models.FloatField("Child Price", default=0, validators=[MinValueValidator(0, message=None)])
    sold_tickets = models.IntegerField(("Tickets Sold"), default=0, null=True, validators=[MinValueValidator(0, message=None)])

    def __str__(self):
        return "%s show" % (self.film)


class Account(models.Model):
    club = models.ForeignKey(StudentClub, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    card_number = CardNumberField()
    expiry_date = CardExpiryField()
    discount_rate = models.FloatField(null=False, blank=False)

    def __str__(self):
        return "%s Account" % (self.club)

class Student(models.Model):
    
    user_name= models.CharField(("user_name"), max_length=30, unique=True, null=True)
    balance = models.FloatField(default=0)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    valid = models.BooleanField(default=False)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "projectApp_student"

    def __str__(self):
        template = '{0.userName}'
        return template.format(self)

class StudentRepresentative(models.Model):
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(("dob"), default=datetime.date.today)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "StudentRepresentative"

    def __str__(self):
        template = '{0.first_name} {0.last_name}'
        return template.format(self)

class Booking(models.Model):
    
    studentQty = models.IntegerField("Student Quantity", default=0, validators=[MinValueValidator(0, message=None)])
    childQty = models.IntegerField("Child Quantity", default=0, validators=[MinValueValidator(0, message=None)])
    adultQty= models.IntegerField("Adult Quantity", default=0, validators=[MinValueValidator(0, message=None)])
    show = models.ForeignKey(Show, on_delete=models.SET_NULL, null=True)
    cancelRqst = models.BooleanField(default=False)

    class Meta:
        db_table = "projectApp_booking"

class CardDetails(models.Model):

    name = models.CharField(("Cardholder Name"), max_length=30, validators=[MinLengthValidator(4, message=None), MaxLengthValidator(30, message=None)])
    card_number = models.CharField(("Card Number"), max_length=16, validators=[MinLengthValidator(16, message=None), MaxLengthValidator(16, message=None)])
    expiry_date = models.CharField(("Card Expiry Date"), max_length=5, validators=[MinLengthValidator(5, message=None), MaxLengthValidator(5, message=None)])
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "projectApp_card"


class Transaction(models.Model):

    amount = models.FloatField("Amount")
    date = models.DateField(null=True)
    representative = models.ForeignKey(ClubRepresentative, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "projectApp_transaction"
