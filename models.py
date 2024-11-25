from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.test import TestCase


def get_default_user():
    return User.objects.get_or_create(username='default_user')[0].id


class Litigant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Unknown")
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Judge(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, unique=False, blank=True, null=True)
    name = models.CharField(max_length=255)
    court = models.CharField(max_length=255)
    email = models.EmailField(unique=False,null=True,blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    appointment_date = models.DateField()
    cases_assigned = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_case_count(self):
        """Update case count assigned to this judge"""
        self.cases_assigned = Case.objects.filter(judge=self).count()
        self.save()


class Case(models.Model):
    CASE_STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ]

    case_number = models.CharField(max_length=50, unique=True)
    litigants = models.ManyToManyField(Litigant, related_name='cases')
    judge = models.ForeignKey(Judge, on_delete=models.SET_NULL, null=True, related_name='cases')
    status = models.CharField(max_length=10, choices=CASE_STATUS_CHOICES, default='Pending')
    date_filed = models.DateField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"Case {self.case_number} - Status: {self.status}"

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=255)
    def __str__(self):
        return self.user.username
    
class Admin(models.Model):
    ROLE_CHOICES = [
        ('Clerk', 'Clerk'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=False,null=True,blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)  # Manually set default to current time

    def __str__(self):
        return f"{self.name} ({self.role})"
    
class ModelTestCase(TestCase):

    def setUp(self):
        self.judge = Judge.objects.create(name="Judge Dredd")
        self.litigant = Litigant.objects.create(name="John Doe")
        self.case = Case.objects.create(case_number="CASE123", judge=self.judge, status="Pending")

    def test_case_creation(self):
        self.case.litigants.add(self.litigant)
        self.assertEqual(self.case.case_number, "CASE123")
        self.assertEqual(self.case.judge.name, "Judge Dredd")
        self.assertIn(self.litigant, self.case.litigants.all())

    def test_unique_case_number(self):
        with self.assertRaises(IntegrityError):
            Case.objects.create(case_number="CASE123", judge=self.judge, status="Pending")