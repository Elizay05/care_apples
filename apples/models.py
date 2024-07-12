from django.db import models
import random
import string
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Models of Care-Apples

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='User', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)  # Usa email como username
        user = self.model(email=email, role=role,**extra_fields)
        user.set_password(password)  # Hashea la contraseña antes de guardarla
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, role='Admin', **extra_fields)

class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=30, default='User')
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Women(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    identification_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    direction = models.CharField(max_length=100)
    ocupation = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    apple = models.ForeignKey('Apple', on_delete=models.CASCADE)
    apple_service = models.ForeignKey('AppleService', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.id

class Municipality(models.Model):
    name = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="municipalities/", default="municipalities/default.jpg", blank=True)

    def __str__(self):
        return self.name


class Establishment(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=250)
    responsible = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    image = models.ImageField(upload_to='establishments/', default="establishments/default.png", blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.digits, k=10))
            if not Establishment.objects.filter(code=code).exists():
                break
        return code

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='categories/', default='categories/default.png', blank=True)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    establishment = models.ForeignKey('Establishment', on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='services/', default='services/default.png', blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.digits, k=10))
            if not Establishment.objects.filter(code=code).exists():
                break
        return code
    

class Apple(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)
    name = models.CharField(max_length=250)
    direction = models.CharField(max_length=250)
    municipality = models.ForeignKey('Municipality', on_delete=models.CASCADE)
    services = models.ManyToManyField('Service', through='AppleService', related_name='apples')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
    
    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.digits, k=10))
            if not Apple.objects.filter(code=code).exists():
                break
        return code
    
    def list_services(self):
        return ", ".join(service.name for service in self.services.all())

    list_services.short_description = 'Services'


class AppleService(models.Model):
    apple = models.ForeignKey('Apple', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)