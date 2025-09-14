from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom user manager for handling user creation with extra fields"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password"""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):  # MUST HAVE THIS EXACT LINE
    """Custom user model with additional fields"""
    
    # Remove username field, use email instead
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields as required - MUST HAVE THESE EXACT FIELD NAMES
    date_of_birth = models.DateField(null=True, blank=True)  # MUST HAVE
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # MUST HAVE
    
    # Set email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove 'username' from REQUIRED_FIELDS
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
