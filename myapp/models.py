from django.db import models
from PIL import Image  # Import Pillow's Image module
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinLengthValidator, RegexValidator
import qrcode
import uuid
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERUSER = "SUPERUSER", 'Superuser'
        DEV = "DEV", 'Dev'
        ADMIN = "ADMIN", 'Admin'
        CUSTOMER = "CUSTOMER", 'Customer'

    base_role = Role.SUPERUSER

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            if self.role in [self.Role.ADMIN, self.Role.DEV, self.Role.CUSTOMER]:
                self.is_staff = True
        return super().save(*args, **kwargs)
        
class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.CUSTOMER)
    
class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.ADMIN)
    
class DevManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.DEV)
        
class Customer(User):

    base_role = User.Role.CUSTOMER

    customer = CustomerManager()
 
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Customer"
    
class Admin(User):

    base_role = User.Role.ADMIN

    admin = AdminManager()
 
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Admin"
    
class Dev(User):

    base_role = User.Role.DEV

    dev = DevManager()
 
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Developer"
    
class Booking(models.Model):

    TICKET_STATUS_CHOICES = [
        ("Notdone","Notdone"),
        ("Confirm","Confirm"),
    ]

    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length = 7, choices = TICKET_STATUS_CHOICES, default = "Notdone")

    def __str__(self):
        return str(self.id)+" "+str(self.user)+" "+str(self.date)

class Concert(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    datetime = models.CharField(max_length=100)
    genre = models.TextChoices("Rock","Indie","Pop","Hip-Hop","Classical","Jazz","Country","EDM","Soul","Reggea","Blues")
    description = models.TextField()
    location = models.TextField()
    agerestriction = models.CharField(max_length=50, null=True, blank=True)
    organizer = models.CharField(max_length=50)
    artists = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        img = Image.open(self.image)

        # Resize the image if height exceeds 500 pixels
        max_height = 500

        height_ratio = max_height / float(img.height)
        new_width = int(float(img.width) * height_ratio)
        img = img.resize((new_width, max_height), Image.Resampling.LANCZOS)  # Updated line

        # Save resized image to memory
        output = BytesIO()
        img.save(output, format='JPEG', quality=90)
        output.seek(0)

        # Update the image file
        self.image = InMemoryUploadedFile(
            output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],
            'image/jpeg', output.tell(), None
        )
        super(Concert, self).save(*args, **kwargs)
      
class Ticket(models.Model):

    TICKET_STATUS_CHOICES = [
        ("Available","Available"),
        ("Selected","Selected"),
        ("Unvailable","Unvailable")
    ]

    seat = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default="Available")

    def __str__(self):
        return str(self.concert) +" - seat:"+ self.seat +" - "+ self.status
    
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
    netamout = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.booking)
    
class Feedback(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content
    
class Message_with_Dev(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content
    
class Message_with_Admin(models.Model):
    user = models.ForeignKey(Dev, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content