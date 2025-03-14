from django.db import models

# Create your models here.
class Gender(models.Model):
    gender = models.CharField(max_length=7)

    def __str__(self):
        return self.gender

class STATE(models.Model):
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.state

class Account(models.Model):
    name = models.CharField(max_length=32)
    mobile = models.PositiveBigIntegerField()
    Account_number = models.PositiveBigIntegerField()
    email = models.EmailField(unique=True)
    aadhar = models.PositiveBigIntegerField()
    father_name = models.CharField(max_length=32)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    state = models.ForeignKey(STATE,default=None,on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_pics")
    pin = models.IntegerField(blank=True,default=0000)
    balance = models.IntegerField(default=500)

    def save(self,*args,**kwargs):
        if not self.Account_number:
            last_account = Account.objects.order_by('-Account_number').first()
            if last_account:
                self.Account_number = last_account.Account_number + 1
            else:
                self.Account_number = 1234567890
        super().save(*args,**kwargs)