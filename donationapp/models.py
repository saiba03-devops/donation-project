from django.db import models
from django.contrib.auth.models import User


class Donation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    fullname = models.CharField(max_length=100, blank=True, null=True)
    dob = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)

    amount = models.IntegerField()
    citizenship = models.CharField(max_length=50, default="Indian Citizen")

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    payment_status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname or "Donation"
    
from django.db import models

class Contact(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    location = models.CharField(max_length=100, blank=True, null=True)

    subject = models.CharField(max_length=200)

    message = models.TextField()

    def __str__(self):
        return self.name