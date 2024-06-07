from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from .utils import otp_generation
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user with the given email, and password.

        Parameters:
        - email (str): The email of the user.
        - password (str): The password of the user.
        - **extra_fields (dict): Additional fields to be included in the user model.

        Returns:
        - CustomUser: The newly created user object.

        Raises:
        - ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError("Please provide an email address")
        else:
            user = self.model( email=email, password=password, **extra_fields)
            password = user.set_password(password)
            user.save(using=self._db)
            return user
        
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.

        Parameters:
        - email (str): The email of the superuser.
        - password (str): The password of the superuser.
        - **extra_fields (dict): Additional fields to be included in the superuser model.

        Returns:
        - CustomUser: The newly created superuser object.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user




class CustomUser(AbstractUser):
    """
    CustomUser class represents a custom user model that extends the AbstractUser class provided by Django.
    It includes additional fields such as date_of_birth, bio, location, otp_field, and otp_created_at for user information and OTP verification.
    The class utilizes a CustomUserManager for user creation and includes methods for generating and validating OTPs.
    Attributes:
        email (EmailField): The unique email address of the user.
        date_of_birth (DateField): The date of birth of the user (nullable).
        bio (CharField): A short bio or description of the user (max length 1000).
        location (CharField): The location of the user (max length 255, nullable).
        otp_field (CharField): The field to store the generated OTP (max length 6, nullable).
        otp_created_at (DateTimeField): The timestamp when the OTP was generated (nullable).
    Methods:
        save_otp(): Generates a new OTP and saves it along with the creation timestamp.
        valid_otp(): Validates the OTP by checking if it was created within the last 10 minutes.
        __str__(): Returns the username of the CustomUser instance for string representation.
    """
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=1000)
    location = models.CharField(max_length=255, blank=True, null=True)
    otp_field = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()    

    def save_otp(self):
        """
        Generates a One-Time Password (OTP) and saves it to the user's otp_field.
        Also sets the otp_created_at field to the current time.

        This method is typically used for generating and storing an OTP for 
        user verification purposes.
        """
        self.otp_field = str(otp_generation())
        self.otp_created_at = timezone.now()
        self.save()
   
    def valid_otp(self):
        """
        Validates the One-Time Password (OTP) by checking if it was created within the last 10 minutes.

        This method is used to ensure that the OTP is still valid and has not expired.

        Returns:
        bool: True if the OTP is valid (i.e., created within the last 10 minutes), False otherwise.
        """
        now = now.timezone()
        if self.otp_created_at and now(now - self.otp_created_at).total_seconds() < 600:
            return True
        return False
    
    def __str__(self):
        """
        Returns a string representation of the CustomUser object.

        This method is used to provide a human-readable representation of the 
        CustomUser instance, typically used in the Django admin interface and 
        other places where a string representation of the user is needed.

        Returns:
        str: The username of the CustomUser instance.
        """
        return self.username