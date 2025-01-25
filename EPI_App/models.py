from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    referral_code = models.CharField(max_length=8, unique=True, blank=True, null=True)
    referred_by =models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals')
    kyc_document = models.FileField(upload_to='kyc_documents/', blank=True, null=True)
    kyc_document_type = models.CharField(max_length=50, blank=True, null=True)
    pan_card = models.FileField(upload_to='pan_cards/', blank=True, null=True)
    bank_passbook = models.FileField(upload_to='bank_passbooks/', blank=True, null=True)
    referrals_made = models.IntegerField(default=0)
    rewards_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
    # Automatically generate a unique referral code if not already set
        if not self.referral_code:
            self.referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Referral(models.Model):
    referred_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referral_by')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_user')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral by {self.referred_by.user.username} to {self.referred_user.username}"
    

class Services(models.Model):
    product_id = models.CharField(max_length=100, unique=True, null=True)
    title=models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    img=models.ImageField(upload_to="pics")
    desc=models.CharField(max_length=500 , null=True)
    def __str__(self):
        return self.title
    
class ProductScheme(models.Model):
    product_id = models.CharField(max_length=100 , null=True)
    investment = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2 , null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.IntegerField()

    def __str__(self):
        return f"{self.product_id} - {self.investment}"
         

class Payment(models.Model):
    product_scheme = models.ForeignKey(ProductScheme, on_delete=models.CASCADE,null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.product_scheme.product_id}"
    
class pay_his(models.Model):
    product_id = models.CharField(max_length=100, unique=True, null=True)
    title = models.CharField(max_length=200,unique=True,null=True)
    investments = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    backcount = models.IntegerField(default=0,null=True)
    def make_payment(self, amount): 
        if amount <= self.balance: 
            self.balance -= amount 
            self.backcount -= 1
            self.last_payment_date = timezone.now() 
            self.save() 
            def __str__(self): 
                return f"{self.title} - Balance: {self.balance}, Backcount: {self.backcount}"